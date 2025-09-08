import argparse
from typing import Dict, List, Tuple

import numpy as np
from tqdm import tqdm

from serve.utils_llm import get_llm_output


class GPTEvaluator:
    """
    Ask GPT if the hypothesis is true or false.
    """

    prompt = """I am a machine learning reseracher summarizing differences in groups of images. The goal is to find a concept that is more true for Group A than Group B.

Given a description of Group A and Group B, output whether a given prediction aligns with the description of Group A. Answer with a 2 (fully aligned), 1 (somewhat aligned), or 0 (not aligned). a score of 1 should be given if the prediction is more true for A than B, but is a superset or a subset of the most correct difference.

For example, if Group A is \"images of dogs in the snow\" and Group B is \"images of dogs next to cats\":
    - predictions like \"dogs in the snow\" or \"dogs in winter time\" should be given a 2
    - predictions like \"golden retrivers on a ski slope\" or \"animals in the snow\" should be given a 1

Here is the descriptions
Group A: {gt_a} and Group B: {gt_b}. Prediction: {hypothesis}

Again, output either a 2, 1, or 0. Response:"""

    prompt1 = """You are an expert visual-language evaluator. Your task is to judge whether a given hypothesis (caption or description) is a good summary of the **differences** between Group A and Group B.

You are given:
- A textual description of **Group A**
- A textual description of **Group B**
- A **prediction** (a hypothesis caption)
Your goal is to determine if the prediction aligns strongly with Group A, and is unlikely to apply to Group B.

Please answer with one of the following scores:
- 2 = Strong match: The prediction is very specific and highly consistent with Group A only. It clearly reflects a unique or distinctive element that separates A from B.
- 1 = Partial match: The prediction is **more true** for A than B, but either too broad, too generic, or only partially captures the correct difference (e.g., it's a subset or superset).
- 0 = No match: The prediction is vague, too general, common to both groups, or could equally apply to B.

Guidelines:
- Focus on **semantic specificity**. Prefer phrases that include distinct words, text, or structure found only in Group A.
- If a hypothesis uses vague or general language (e.g., "yoga poses" or "outdoor scenes"), it is likely a 0 or 1.
- If a hypothesis mentions a **unique term, structure, or label** that only appears in Group A, it is likely a 2.
- Ignore superficial features like color unless explicitly mentioned as different in the descriptions.

Here are example cases:

Example 1:
- Group A: dogs in the snow  
- Group B: dogs next to cats  
- Prediction: "dogs in the snow" → **2**  
- Prediction: "golden retrievers on a ski slope" → **1**  
- Prediction: "animals in the snow" → **1**  
- Prediction: "dogs with animals" → **0**

Example 2:
- Group A: yoga diagrams showing the Sun Salutation sequence with pose labels  
- Group B: photos of people performing Tree Pose outdoors  
- Prediction: "step-by-step diagram of Sun Salutation with arrows" → **2**  
- Prediction: "yoga poses with labels" → **1**  
- Prediction: "outdoor yoga practice" → **0**

Now evaluate the following input:

Group A: {gt_a}  
Group B: {gt_b}  
Prediction: {hypothesis}

What is the best score (0, 1, or 2)? Please answer with a single number only."""

    def __init__(self, args: Dict):
        self.args = args

    def evaluate(
        self, hypotheses: List[str], gt_a: str, gt_b: str
    ) -> Tuple[Dict, List[Dict]]:
        # varify that the hypothesis is true or false
        scores = []
        evaluated_hypotheses = []
        for hypothesis in tqdm(hypotheses[: self.args["n_hypotheses"]]):
            prompt = self.prompt.format(hypothesis=hypothesis, gt_a=gt_a, gt_b=gt_b)
            answer = get_llm_output(prompt, self.args["model"])
            try:
                scores.append(int(answer))
            except ValueError:
                scores.append(0)

            evaluated_hypotheses.append(
                {"hypothesis": hypothesis, "score": scores[-1], "response": answer}
            )
        print("Scores:", scores)
        metrics = {
            "acc@1": scores[0] / 2,
            "acc@5": np.max(scores[:5]) / 2,
            "acc@N": np.max(scores[: self.args["n_hypotheses"]]) / 2,
        }
        return scores, metrics, evaluated_hypotheses


class NullEvaluator:
    def __init__(self, args: Dict):
        self.args = args

    def evaluate(
        self, hypotheses: List[str], gt_a: str, gt_b: str
    ) -> Tuple[Dict, List[Dict]]:
        return {}, [{}]


def test_evaluator():
    args = {
        "model": "gpt-4",
        "n_hypotheses": 20,
    }
    evaluator = GPTEvaluator(args)
    hypotheses = [
        "dogs in the snow",
        "golden retrivers on a ski slope",
        "animals in the snow",
        "dogs in winter time",
    ]
    gt_a = "images of dogs in the snow"
    gt_b = "images of dogs next to cats"
    metrics, evaluated_hypotheses = evaluator.evaluate(hypotheses, gt_a, gt_b)
    print(metrics)
    print(evaluated_hypotheses)


if __name__ == "__main__":
    test_evaluator()
