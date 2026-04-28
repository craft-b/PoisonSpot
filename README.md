# PoisonSpot — Facial Emotion Recognition (Narcissus Attack)

**Course:** CIS 582 — Trustworthy AI, Winter 2026
**Student:** Bobby Craft
**Dataset:** [Emotion Recognition Dataset](https://www.kaggle.com/datasets/sujaykapadnis/emotion-recognition-dataset) (Kaggle)

## Overview

Extension of the [PoisonSpot](https://github.com/Philenku/PoisonSpot) clean-label backdoor detection framework to the Facial Emotion Recognition (FER) dataset using the Narcissus attack.

**Pipeline:**
1. Generate Narcissus backdoor trigger (surrogate ResNet18, 5 epochs, 200 PGD steps)
2. Train poisoned ResNet18 victim (30 epochs, 10% target-class poison rate)
3. Batch-level provenance detection
4. Sample-level provenance detection
5. Score and remove flagged samples
6. Retrain from scratch on filtered dataset

## Key Results

| Metric | Value |
|---|---|
| Clean Accuracy (poisoned model) | 79.88% |
| Attack Success Rate (ASR) | 85.47% |
| TPR — KMeans | 98.75% |
| FPR — KMeans | 0.00% |
| TPR — Gaussian | 99.38% |
| FPR — Gaussian | 0.93% |
| Retrain ACC | 79.65% |
| Retrain ASR | 72.86% |
| ΔASR (mitigation) | −12.61 pp |

## Setup

Run the notebook on Kaggle with the `sujaykapadnis/emotion-recognition-dataset` dataset attached.

**Environment:** PyTorch 2.6.0, CUDA 12.4, T4 GPU

## Files

- `poisonspot_emotion_kaggle.ipynb` — full pipeline notebook (all patched source files embedded)
- `outputs/results/` — results CSV, config, and detection visualizations
- `outputs/provenance/` — flagged feature dimensions from batch-level provenance
