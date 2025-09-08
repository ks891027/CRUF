# CURF: Improving Reasoning About Differences in Image Sets in Vision-Language Models via Chain-of-Thought Prompting

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)

This repo provides the PyTorch source code of my paper: Improving Reasoning About Differences in Image Sets in Vision-Language Models via Chain-of-Thought Prompting.

## 🔮 Abstract

How do two sets of images differ? Discerning set-level differences is essential for understanding dataset properties and model behaviors, yet existing methods like **VisDiff** rely on a two-stage pipeline (proposal + ranking), which is inefficient and prone to error propagation.

In this work, we propose **CURF**, a **Chain-of-Thought (CoT) based unified reasoning framework** for the task of **Set Difference Captioning (SDC)**. Instead of separating proposal and ranking, CURF leverages CoT prompting to integrate both steps into a single forward pass. Given two sets of images $\mathcal{D}_A$ and $\mathcal{D}_B$, CURF outputs a ranked list of natural language hypotheses that are more often true in $\mathcal{D}_A$ than in $\mathcal{D}_B$.

We evaluate CURF on **VisDiffBench** and demonstrate three key advantages:

- ✅ **Accuracy**: better identification of fine-grained semantic differences (e.g., *“dark vs. milk chocolate”*).  
- ⚡ **Efficiency**: single-pass inference reduces computation by over **20×** compared to VisDiff.  
- 🔍 **Interpretability**: explicit reasoning steps reveal how hypotheses are generated, prioritized, and ranked.  

Beyond reproducing VisDiff baselines, we further test CURF with **Qwen2.5-VL** as backbone and explore **image grid enhancements** that highlight subtle differences, pushing the frontier of set-level visual reasoning.


<img src="data/ISDC.png"></img>

## 🚀 Getting Started

Here we provide a minimal example to describe the differences between two sets of images, where [set A](./data/examples/set_a/) are images showing `people practicing yoga in a mountainous setting` and [set B](./data/examples/set_b/) are images showing `people meditating in a mountainous setting`.

1. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

2. Describe differences:
  ```bash
  python main.py
  ```



## 💼 Customized Usage

This section explains how to run CURF on custom datasets by preparing CSV files, starting model servers, and executing the main script.