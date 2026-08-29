# Relationship to the upstream PoisonSpot project

This repository is **not** a copy or a fork of the PoisonSpot framework. It
contains an extension of it to the Facial Emotion Recognition dataset, and it
holds only the parts that are mine.

**Upstream:** [`Philenku/PoisonSpot`](https://github.com/Philenku/PoisonSpot),
pinned at commit `fe5590228124f98d4abb2032aefc1f78075a1b87`.

## What is in this repository

| | |
|---|---|
| `patches/fer-narcissus.patch` | my modifications to the upstream sources, as a unified diff against the pinned commit |
| `smoke/` | a CPU-sized config and synthetic dataset generator, written for this project |
| `poisonspot_emotion_kaggle.ipynb` | the runner that assembles the two |
| `outputs/` | results and figures from the reported run |

## What is not, and why

No upstream source file is redistributed here. The extension touches six files,
three of which are more than 90% upstream code, so shipping them whole would
mean redistributing someone else's work. A patch carries my changes and only a
few lines of surrounding context, which is both the smaller footprint and the
more useful artefact — it shows exactly what was changed rather than burying it
in a file that mostly is not mine.

To reproduce, the notebook clones upstream at the pinned commit and applies the
patch. You obtain upstream from its author, not from me.

## Licensing status — unresolved

The upstream repository carries no LICENSE file. Absent one, the default is that
no permission to copy, modify or redistribute is granted, so the licensing of
work derived from it is genuinely unclear rather than merely unstated. That is
the reason this repository ships a patch instead of files, and the reason it
does not yet declare a license of its own: putting a permissive licence over a
derivative of an unlicensed work would be asserting something I am not in a
position to assert.

This is being raised with the upstream author. Until it is settled, treat the
contents as "source available for review" — read it, assess it, but do not
assume rights to reuse it.
