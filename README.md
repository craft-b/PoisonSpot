# PoisonSpot — FER extension (Narcissus clean-label backdoor)

Extending a clean-label backdoor detection framework to a dataset it was never
built for, and reporting what the detector actually recovered.

The [PoisonSpot](https://github.com/Philenku/PoisonSpot) framework detects
clean-label backdoors by tracing training-time provenance: which samples moved
the model, and how anomalously. It ships with CIFAR-10 and Caltech-256 support.
This work extends it to a **Facial Emotion Recognition** dataset under the
**Narcissus** attack, and measures how much of the attack the detector removes
once flagged samples are dropped and the model is retrained from scratch.

## What is mine, and what is not

This distinction matters more than usual here, because the repository name
matches the upstream project.

| | |
|---|---|
| **Upstream** | the detection framework itself — batch- and sample-level provenance, scoring, the Narcissus attack implementation |
| **Mine** | the FER dataset adapter, a rewritten training loop, the scenario wiring, and a CPU smoke harness |

Measured against the pinned upstream commit, the extension is **989 inserted and
420 deleted lines across six files**:

| File | Upstream | After patch | Shared with upstream |
|---|---:|---:|---:|
| `src/helpers/data.py` | 2.7 KB | 25.3 KB | 8% — effectively new |
| `src/helpers/train.py` | 7.1 KB | 3.0 KB | 2% — rewritten |
| `src/__init__.py` | 2.3 KB | 1.6 KB | 65% |
| `src/helpers/scoring.py` | 27.9 KB | 29.3 KB | 93% |
| `src/helpers/provenance.py` | 41.0 KB | 43.1 KB | 94% |
| `main.py` | 39.2 KB | 41.5 KB | 96% |

The whole of it is readable in [`patches/fer-narcissus.patch`](patches/fer-narcissus.patch).
No upstream file is redistributed here — see [NOTICE.md](NOTICE.md) for why that
matters and for the unresolved licensing question.

## Results

One run: `emotion_narcissus_eps16_tgt10_seed42`, ResNet18, ε=16, target class 3,
10% target-class poison rate, 30 epochs, seed 42, T4.

**Committed evidence** — in [`outputs/results/.../results.csv`](outputs/results/emotion_narcissus_eps16_tgt10_seed42/results.csv):

| Metric | Value |
|---|---:|
| Poisoned-model clean accuracy | 79.04% |
| Attack success rate | 85.05% |
| Batch-level flagged feature dimensions | 5,060 |

**Reported from the run console, not committed** — these were recorded from
stdout during the run and no artefact in this repository substantiates them:

| Metric | Value |
|---|---:|
| TPR / FPR — KMeans threshold | 98.75% / 0.00% |
| TPR / FPR — Gaussian threshold | 99.38% / 0.93% |
| Retrained accuracy | 79.65% |
| Retrained ASR | 72.86% |

### What this does and does not establish

The detector separates poisoned from clean samples very well on this dataset —
98.75% TPR at zero false positives is a strong separation, and the provenance
approach clearly transfers to FER.

Removing those samples does **not** remove the backdoor. Retraining from scratch
on the filtered set leaves ASR at roughly 73%, against 85% before. **Detection
near-perfect, mitigation partial** — around twelve points of attack success
recovered. That gap is the interesting result and the reason to report the
retrain numbers at all: a detector scored only on TPR would look like a solved
problem here, and it is not.

An earlier version of this README reported 79.88% accuracy and 85.47% ASR. Those
figures do not match the committed results file and their provenance could not be
established, so the committed numbers are used above. The unsubstantiated block
is marked as such rather than deleted; the honest position is that it needs one
re-run with the artefacts saved.

The two figures in `outputs/results/` are raw diagnostic scatter plots from the
scoring stage, unlabelled and without axes. They are kept as run artefacts and
deliberately not presented as results.

## Reproducing

The pipeline needs a GPU and several hours; it is written to run on Kaggle with
the [Emotion Recognition Dataset](https://www.kaggle.com/datasets/sujaykapadnis/emotion-recognition-dataset)
attached.

1. Open `poisonspot_emotion_kaggle.ipynb` on Kaggle, attach the dataset, select a T4.
2. Run it. The notebook clones upstream **at a pinned commit**
   (`fe5590228`), applies `patches/fer-narcissus.patch`, verifies it applied, and
   runs the pipeline end to end.

The pin is the point. An unpinned `--depth 1` clone would apply this patch to
whatever upstream HEAD happened to be that day.

### Without a GPU

`smoke/` holds a CPU-sized config and a generator for a small synthetic dataset,
so the pipeline can be exercised end to end without the real data or a GPU:

```bash
python smoke/smoke_data_gen.py          # writes smoke_data/, 5 classes
python main.py -c smoke/config_smoke_cpu.yaml
```

This validates wiring, not results.

**Environment:** PyTorch 2.6.0 / CUDA 12.4 on Kaggle's T4 image. Dependencies are
whatever that image provides plus `pyyaml`, `tqdm` and `captum`; they are not
pinned, which is a real reproducibility gap and the next thing to fix.

## Repository contents

```
patches/fer-narcissus.patch   the extension, as a diff against pinned upstream
smoke/                        CPU config + synthetic dataset generator
poisonspot_emotion_kaggle.ipynb   runner: clone, patch, execute
outputs/results/              config, results CSV, diagnostic plots
outputs/provenance/           flagged feature dimensions, batch-level stage
NOTICE.md                     upstream relationship and licensing status
```

Model checkpoints are not committed. Two 45 MB pickles were, which made a clone
89 MB for a repository whose source is a patch and a notebook.

## Known gaps

- **One run, one seed.** No repeats, so none of the numbers carry an interval.
- **Unpinned dependencies**, beyond the pinned upstream commit.
- **Four reported metrics have no committed artefact.** Re-running with results
  written to disk is the first thing this repository needs.
- **No tests.** The smoke harness checks that the pipeline runs, not that it is right.

---

Built for CIS 582 (Trustworthy AI), Winter 2026 — Bobby Craft.
