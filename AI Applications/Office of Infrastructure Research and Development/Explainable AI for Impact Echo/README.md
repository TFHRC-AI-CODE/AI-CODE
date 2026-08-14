# Explainable AI for impact Echo

Overview
--------
This repository contains reproduced deep learning models for classifying Impact Echo (IE) signals collected from lab-fabricated concrete slabs. The implementation reproduces and extends the methodology from the paper:

"Classification of Impact Echo Signals Using Explainable Deep Learning and Transfer Learning Approaches" — Rahul Torlapati, Hoda Azari, and Parisa, Transportation Research Record (2023).

The first model classify IE signals into two categories:
- Class 0: Intact concrete structural response.
- Class 1: Presence of delamination, honeycombing, or voids.

The second model classifies IE signals into 5 categories:
- Class 0: Intact concrete structural response.
- Class 1: shallow delamination.
- Class 2: honeycombing.
- Class 3: void.
- Class 4: deep delamination.

Project structure
-----------------

Explainable AI for impact Echo/

- notebooks and scripts
- data

Citation
--------
If you use this code or the reproduced models, please cite the original paper and dataset. See `CITATION.cff` for machine-readable citation metadata.

Contact
-------
For questions about the reproduction, open an issue or contact the contributors listed in `CITATION.cff`.

