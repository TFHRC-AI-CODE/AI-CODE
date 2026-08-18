# Automated Impact Echo using Deep Learning

**Contributor:** Federal Highway Administration (FHWA) Nondestructive Evaluation (NDE) Laboratory  
**Primary Domain:** Infrastructure Inspection & NDE  
**Date Published:** 2026-08-18  
**Repository Link:** [View Code](https://github.com/TFHRC-AI-CODE/AI-CODE/tree/main/AI%20Applications/Office%20of%20Infrastructure%20Research%20and%20Development/Deep%20Learning%20for%20Impact%20Echo)  

---

## 1. Executive Summary
This repository documents a peer-reviewed AI case study, “Classification of Impact Echo Signals Using Explainable Deep Learning and Transfer Learning Approaches,” published in Transportation Research Record. Impact echo (IE) is a widely used nondestructive evaluation technique for detecting subsurface defects, such as delamination, honeycombing, and voids, in concrete structures. This study compares two approaches for automatic IE signal classification: clustering based on expert-crafted features and deep learning (DL) using automatically extracted features, demonstrating DL’s superior analytical performance. Additionally, the research examines the explainability of trained DL models, identifying key attributions significant to IE data classification.

---

## 2. Problem Statement & Objectives
* **Challenge:** Visual inspections of bridge decks require lane closures and subjective visual scoring.
* **Objective:** Automate defect identification to assist asset management and condition assessment.

---

## 3. Data & Model Specifications

### Datasets
| Dataset Name | Format | Count | Access Link |
| :--- | :--- | :--- | :--- |
| **Deck Survey RGB** | `.jpg` (4K) | 2,500 images | [Download Dataset](#) |

### Pre-Trained Models
* **Architecture:** YOLOv8x-Seg
* **Weights:** `bridge_deck_v1.pt`

---

## 4. Setup & Execution

```bash
git clone https://github.com/TFHRC-AI-CODE/AI-CODE.git
cd AI-CODE
pip install -r requirements.txt
python detect.py --weights weights/bridge_deck_v1.pt --source data/test/
```

---

## 5. Results & Field Impact
* Reduced deck inspection analysis time from 3 days to under 4 hours per structure.
* High correlation with follow-up non-destructive evaluation (NDE) testing.

---

## 6. Lessons Learned & Best Practices
* Overcast lighting conditions yielded superior crack segmentation by eliminating harsh shadows.
* Model export to ONNX format enabled real-time edge processing directly on drone hardware.

---

## 7. Contacts & Maintainers
* **Primary Contact:** CODE Project Team (code@dot.gov)
* **Contributing Agency:** Iowa Department of Transportation / FHWA
