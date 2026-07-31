# FLR Model Validation and Alignment Report

## Validation conclusion

**PASS — the five public FLR model artifacts are numerically identical to the
verified original models for raw inference.**

The public repository is technically aligned with the final FLR workflow and
the FLR content reported in the associated paper. It is an inference-focused
release, not a complete reproduction of every paper component.

One intentional public-reporting safeguard is documented: the standard
`flr_percent` output is clipped to [0, 100]. The original notebook router
capped values above 100 but did not replace negative values with zero. The
unchanged raw model output remains available with `--include-raw`.

## Sources reviewed

- Published article:
  `Machine-learning prediction of pavement fatigue life ratio from structural
  inputs and TSDD measurements using physics-guided data generation`
- Final XGBoost development notebook:
  `Str-ML-RSL-XGBOOST-one-model-for-each-binder-use-this-final-in-paper.ipynb`
- Five original binder-specific joblib model files.
- Original FLR development database used to reconstruct the test partition.
- All files in this public repository.

## Model artifact verification

The original joblib artifacts had previously been compared with their original
saved copies and found byte-for-byte identical. Their SHA-256 checksums are
recorded in `src/flr_model/models/model_manifest.json`.

Each verified XGBoost Booster was exported to native UBJ format. A full
prediction comparison was then performed across all 8,837 records in the
paper workflow's held-out 20% synthetic test partition.

| Check | Result |
|---|---:|
| Held-out rows compared | 8,837 |
| Supported binder models compared | 5 |
| Maximum absolute difference, raw predictions | 0.0 |
| Rows with any raw prediction difference | 0 |
| UBJ checksum verification | Passed for all five files |

Therefore, conversion from the verified joblib artifacts to the public UBJ
artifacts did not change model predictions.

## Input and routing alignment

| Item | Validation result |
|---|---|
| Ten slope offsets | Exact match |
| Slope units | µm/m |
| AC thickness | Included in mm |
| Damaged AC modulus | Included at 25 Hz in MPa |
| Numerical feature order | Exact match |
| Binder grades | Exact five-grade match |
| Binder routing | Equivalent source-code implementation |
| Slope reference temperature | Documented as 20°C |

The notebook-defined serialized router was replaced with ordinary Python
routing because the custom notebook class is not portable. This changes the
software packaging, not model selection or raw predictions.

## Hyperparameter alignment

| Binder | Learning rate | Max depth | Estimators | Subsample | Reg. alpha | Reg. lambda | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| PG 46-40 | 0.10 | 10 | 300 | 0.8 | 0 | 5 | Match |
| PG 58-34 | 0.10 | 10 | 300 | 0.8 | 0 | 5 | Match |
| PG 64-28 | 0.10 | 10 | 300 | 0.8 | 0 | 5 | Match |
| PG 70-22 | 0.10 | 10 | 200 | 0.6 | 1 | 5 | Match |
| PG 76-10 | 0.05 | 10 | 300 | 0.6 | 0 | 5 | Match |

These values match the final notebook outputs and Table 4 of the paper.

## Evaluation alignment

Reconstructing the final notebook filters and 80/20 split with
`random_state=42`, then applying the original upper cap at 100, produced:

| Metric | Recalculated value | Notebook value | Paper value |
|---|---:|---:|---:|
| R² | 0.9904224 | 0.990 | 0.99 |
| MAE | 1.504323 | 1.504 | 1.5 |
| RMSE | 3.451734 | 3.452 | 3.45 |

The apparent differences are only the number of displayed decimal places.

The public [0, 100] reporting safeguard changes 14 negative raw predictions in
the 8,837-row test partition to zero. Consequently, the public reported-output
metrics differ trivially from the notebook values:

- R² = 0.9904232
- MAE = 1.503822
- RMSE = 3.451598

This does not alter the trained models. Advanced raw output reproduces the
original model predictions exactly.

## Example alignment

The five example records come from the reconstructed held-out synthetic test
partition, one per binder. For each binder, the selected row is the row nearest
the median reference FLR for that binder's test subset. This is an objective
selection rule and does not select records based on prediction accuracy.

The examples are physics-guided synthetic study cases, not field
measurements.

## Paper and documentation alignment

The README, model card, methodology, limitations, provenance, input data
dictionary, and citation metadata were checked for consistency with the paper
and final notebook. They correctly describe:

- The FLR definition and prediction purpose.
- The 12 numerical inputs and binder routing.
- Physics-guided simulation-based development.
- The 80/20 test split and five-fold tuning procedure.
- Supported binders and selected hyperparameters.
- Reported test performance.
- Required 20°C slope reference condition.
- The role of damaged AC modulus.
- The simulation-domain and field-validation limitations.
- Intended screening use and engineering limitations.

## Intentional exclusions

The following are intentionally not part of this public inference repository:

- Approximately 7 GB Random Forest AC-modulus model.
- Synthetic training database.
- Raw development notebooks.
- Training scripts.
- Consolidated joblib router.
- Publisher-formatted article PDF.

Users can run the FLR models by supplying damaged AC dynamic modulus at 25 Hz
in MPa from an appropriate source.

## Final interpretation

The repository can accurately be described as:

> A public inference release of the five binder-specific FLR models associated
> with the published study, with native model artifacts that reproduce the
> verified originals exactly at the raw-prediction level.

It should not be described as a complete reproduction package for all model
training, synthetic-data generation, or the separate AC-modulus model.
