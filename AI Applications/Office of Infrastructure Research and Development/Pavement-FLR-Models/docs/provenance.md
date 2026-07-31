# Model Provenance

## Source workflow

The five public models correspond to the final modulus-inclusive workflow in:

```text
Str-ML-RSL-XGBOOST-one-model-for-each-binder-use-this-final-in-paper.ipynb
```

The relevant workflow trains separate models using the ten slopes, AC
thickness, and damaged AC modulus at 25 Hz, then evaluates a consolidated
binder router. Its recorded overall test results are R² = 0.990,
MAE = 1.504 percentage points, and RMSE = 3.452 percentage points, matching
the rounded values reported in the paper.

The notebook also contains exploratory and plotting workflows that are not
part of this public inference implementation.

## Verified source artifacts

The five source joblib files were checked against their original saved copies
before conversion and found to be byte-for-byte identical. Their SHA-256
values are recorded in `model_manifest.json`.

The notebook-defined consolidated router is not distributed because:

- It duplicates the five model objects.
- It depends on a class serialized from the notebook `__main__` environment.
- Its raw array routing is less transparent than an ordinary source module.
- Native XGBoost artifacts are more suitable for model exchange.

## Conversion

Each verified estimator's XGBoost Booster was saved in native UBJ format and
reloaded. Predictions before and after conversion were compared on fixed
verification inputs. The maximum absolute difference was zero for every
model.

## Integrity verification

Run:

```bash
python tools/verify_checksums.py
```

The command checks the public UBJ files against the SHA-256 values in the
manifest.

## Excluded artifacts

- The approximately 7 GB Random Forest modulus model.
- The synthetic model-development database.
- The publisher-formatted article PDF.
- The notebook-defined consolidated joblib router.
- Raw development notebooks.

These exclusions do not prevent FLR inference when the required damaged AC
modulus is supplied by the user.

## Example records

The five records in `examples/example_input.csv` were selected from the
notebook's held-out 20% synthetic test partition after reproducing the stated
filtering and `random_state=42` split. One record was selected per binder using
an objective rule: the row nearest the median reference FLR for that binder's
test subset. The reference targets are stored separately in
`examples/example_reference.csv` and are not passed to the predictor.
