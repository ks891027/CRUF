# 選擇官方 nvidia/cuda 映像版本，可搭配 cudnn8
FROM nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04

# 切換時區、避免安裝時詢問互動
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Taipei

# 更新 apt，並安裝一些基本工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    wget \
    git \
    curl \
    ca-certificates \
    build-essential \
    libssl-dev \
    libgl1 \
    libglib2.0-0 \
    && ln -fs /usr/share/zoneinfo/Asia/Taipei /etc/localtime \  
    && echo "Asia/Taipei" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# 使用通用 Miniforge 安裝方式
RUN curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" \
    && bash Miniforge3-$(uname)-$(uname -m).sh -b -p /opt/conda \
    && rm Miniforge3-$(uname)-$(uname -m).sh

# 為了方便之後直接使用 conda/mamba 指令
ENV PATH=/opt/conda/bin:$PATH

# 建立 conda 環境與安裝套件
RUN conda create -n visdiff python=3.11 -y \
    && conda run -n visdiff pip install pip \
    && conda run -n visdiff pip install salesforce-lavis opencv-python flask \
    && conda clean -afy

# 自動啟動環境
RUN echo "source /opt/conda/etc/profile.d/conda.sh && conda activate visdiff" >> /root/.bashrc

WORKDIR /workspace
COPY serve/ /workspace

CMD ["/bin/bash", "--login"]