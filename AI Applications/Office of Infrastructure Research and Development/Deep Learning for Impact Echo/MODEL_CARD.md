# Model Card: Impact Echo Classification Models

## Model Details

### Model Types

- **1D Architectures**: 1D Convolutional Neural Network (Custom) & Bidirectional LSTM
- **2D Architectures (STFT Spectrograms)**: AlexNet (Fully Trained & Transfer Learning), GoogLeNet (Transfer Learning), and ResNet-50 (Transfer Learning)

### Base Paper

Dorafshan, S., & Azari, H. (2020). "Deep learning models for bridge deck evaluation using impact echo." *Construction and Building Materials*.

## Intended Use

### Primary Use Cases

Classifying the structural condition (Sound vs. Defected) of concrete slabs using Impact Echo (IE) non-destructive testing signals.

### Out-of-Scope Uses

This model is calibrated strictly for 200kHz sampling rates on concrete structures. It is not intended for general audio classification or medical ultrasound.

## Training Data

### Source

8 Experimental Concrete Slabs containing artificial defects:
- Shallow delamination
- Deep delamination
- Honeycombing
- Voids

### Class Distribution

- **Sound Signals (Class 0)**: 1,504 instances
- **Defected Signals (Class 1)**: 512 instances

### Preprocessing

**1D Models**: DC offset removal and Z-score normalization.

**2D Models**: Short-Time Fourier Transform (STFT) converting waveforms to 224×224×3 (or 227×227×3) spectrograms with ImageNet normalization and zero-centering.

## Evaluation & Reproduction Results

### Testing Methodology

Leave-One-Specimen-Out (LOSO) Cross-Validation. Models are trained on 7 slabs and tested on the remaining unseen slab across 8 folds.

### Optimization Enhancements

- Replaced static unweighted loss with dynamic class weighting and WeightedRandomSampler to handle the ~3:1 class imbalance
- ResNet-50 TL and other 2D models utilize an optimized Learning Rate alongside a ReduceLROnPlateau scheduler to prevent training stagnation

### Performance Metrics (Aggregated across all 8 folds)

| Model | Metric | Mean | COV | Max | Min |
|-------|--------|------|-----|-----|-----|
| **1D CNN** | ACC | 0.90 | 0.01 | 0.91 | 0.87 |
| | TPR | 0.75 | 0.05 | 0.81 | 0.69 |
| | TNR | 0.95 | 0.02 | 0.98 | 0.93 |
| | F1 | 0.79 | 0.03 | 0.82 | 0.74 |
| **biLSTM** | ACC | 0.90 | 0.04 | 0.94 | 0.84 |
| | TPR | 0.81 | 0.05 | 0.84 | 0.73 |
| | TNR | 0.93 | 0.04 | 0.98 | 0.88 |
| | F1 | 0.80 | 0.07 | 0.89 | 0.70 |
| **AlexNet (FT)** | ACC | 0.87 | 0.09 | 0.95 | 0.70 |
| | TPR | 0.86 | 0.09 | 1.00 | 0.77 |
| | TNR | 0.88 | 0.14 | 0.98 | 0.60 |
| | F1 | 0.79 | 0.11 | 0.91 | 0.63 |
| **AlexNet (TL)** | ACC | 0.80 | 0.05 | 0.85 | 0.72 |
| | TPR | 0.66 | 0.12 | 0.73 | 0.48 |
| | TNR | 0.85 | 0.07 | 0.95 | 0.75 |
| | F1 | 0.63 | 0.08 | 0.70 | 0.54 |
| **GoogLeNet (TL)** | ACC | 0.77 | 0.06 | 0.85 | 0.67 |
| | TPR | 0.56 | 0.18 | 0.70 | 0.41 |
| | TNR | 0.84 | 0.09 | 0.97 | 0.69 |
| | F1 | 0.55 | 0.11 | 0.65 | 0.48 |
| **ResNet-50 (TL)** | ACC | 0.88 | 0.01 | 0.89 | 0.86 |
| | TPR | 0.65 | 0.06 | 0.72 | 0.59 |
| | TNR | 0.96 | 0.02 | 0.99 | 0.93 |
| | F1 | 0.73 | 0.03 | 0.77 | 0.70 |

**Legend:**
- **ACC**: Accuracy
- **TPR**: True Positive Rate (Sensitivity)
- **TNR**: True Negative Rate (Specificity)
- **F1**: F1-Score
- **COV**: Coefficient of Variation