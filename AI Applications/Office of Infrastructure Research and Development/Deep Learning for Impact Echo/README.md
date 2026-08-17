# Deep Learning for Impact Echo

## Overview

This repository provides reproduced deep learning models for the autonomous classification of Impact Echo (IE) signals collected from concrete bridge decks. This work is a reproduction and extension of the methodology described in:

> Dorafshan, S., & Azari, H. (2020). "Deep learning models for bridge deck evaluation using impact echo." *Construction and Building Materials*.

The models classify raw, time-domain IE waveforms and Short-Time Fourier Transform (STFT) spectrograms into two structural conditions:

- **Sound (Class 0)**: Intact concrete structural response
- **Defected (Class 1)**: Concrete exhibiting artificial delamination, honeycombing, or voids

This release provides a transparent, runnable implementation of the 1D and 2D models detailed in the study, complete with data loading, preprocessing, optimization fixes, and Leave-One-Specimen-Out (LOSO) cross-validation routines.

## Why This Matters

The conventional approach for analyzing Impact Echo data—the peak frequency method—requires user expertise to define analysis parameters, which can hinder broad field implementation. It often struggles with noisy data or complex defect geometries.

Deep Learning Models (DLMs) provide a robust, automated alternative. By learning hierarchical features directly from raw 1D waveforms or 2D STFT spectrograms, these models minimize user bias and can classify structural conditions much faster. Making these reproduced and optimized training pipelines publicly accessible supports reproducible analysis and further research into automated NDE bridge inspections.

## What This Repository Provides

Our implementation is documented in a series of self-contained Jupyter Notebooks found in the `src_dlmodel/` directory.

### Data Exploration & Background

- **`project_background.ipynb`**: Data loading, exploration, and visualization of the raw IE signals in both the time domain and frequency domain (Fast Fourier Transform)

### 1D Deep Learning Models

- **`1D_CNN_good.ipynb`**: Implementation of the custom 1D Convolutional Neural Network processing raw 2000-point waveforms. Leverages dynamic class weighting
- **`biLSTM_good.ipynb`**: Implementation of the Bidirectional Long Short-Term Memory recurrent network. Optimized with WeightedRandomSampler to enforce balanced class representation during training

### 2D Convolutional Neural Networks (Spectrograms)

- **`alexnet_ft_good.ipynb`**: AlexNet architecture trained from scratch (Fully Trained)
- **`alexnet_tl_good.ipynb`**: AlexNet architecture utilizing Transfer Learning (TL) with frozen ImageNet feature extractors
- **`googlenet_good.ipynb`**: GoogLeNet (Inception v1) architecture utilizing Transfer Learning on 224x224x3 spectrograms
- **`resnet_good.ipynb`**: ResNet-50 architecture utilizing Transfer Learning, enhanced with an optimized learning rate and a ReduceLROnPlateau scheduler

### Analysis & Results

- **`figure_12_reproduction.ipynb`**: Code for reproducing the comparative defect maps (e.g., Figure 12 from the original paper), mapping the probability of defect presence geographically across the tested slabs

## Project Structure

```
Deep Learning for Impact Echo/
├── src_dlmodel/                           # Source code and Jupyter Notebooks
│   ├── 1D_CNN_good.ipynb
│   ├── alexnet_ft_good.ipynb
│   ├── alexnet_tl_good.ipynb
│   ├── biLSTM_good.ipynb
│   ├── figure_12_reproduction.ipynb
│   ├── googlenet_good.ipynb
│   ├── project_background.ipynb
│   ├── resnet_good.ipynb
│   └── *.png                              # Generated accuracy/iteration plots
├── CITATION.cff                           # Citation metadata
├── LICENSE                                # Open source license (MIT)
├── MODEL_CARD.md                          # Model details, data, and performance
├── README.md                              # Project overview
```

## Setup and Installation

### Requirements

- Python 3.8 or newer

### Installation Steps

1. Clone this repository:

```bash
git clone <repository-url>
cd "Deep Learning for Impact Echo"
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```


## Dataset Reference

The models expect raw text files containing time and voltage data. The annotated Impact Echo dataset used for this project (8 laboratory-made concrete slabs) can be accessed via Mendeley Data: [10.17632/44rb96872r.1](https://data.mendeley.com/datasets/44rb96872r/1)

## Citation

If these reproduced models or code contribute to your research, please cite the original study:

```bibtex
@article{Dorafshan2020,
  author = {Dorafshan, S. and Azari, H.},
  title = {Deep learning models for bridge deck evaluation using impact echo},
  journal = {Construction and Building Materials},
  volume = {263},
  pages = {120109},
  year = {2020},
  doi = {10.1016/j.conbuildmat.2020.120109}
}
```

Machine-readable citation metadata is provided in `CITATION.cff`.

## License

The code and documentation in this repository are provided under the MIT License.

## Disclaimer

The models and accompanying materials are provided on an "as-is" basis for research, informational, and NDE screening purposes. No warranty is made regarding accuracy, completeness, suitability, or performance for a particular application. Users are responsible for input quality, engineering interpretation, and independent verification.