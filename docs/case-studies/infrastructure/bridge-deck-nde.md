# Automated Bridge Deck Crack Detection Using UAV Imagery

**Lead Agency / Organization:** Iowa DOT / Federal Highway Administration (FHWA)  
**Primary Domain:** Infrastructure Inspection & NDE  
**Date Published:** 2024-04-15  
**Repository Link:** [View Code](https://github.com/TFHRC-AI-CODE/AI-CODE)  

---

## 1. Executive Summary
Demonstrates the deployment of a computer vision model trained on UAV imagery to automate concrete bridge deck crack identification.

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
