# Methodology

## Purpose

The framework estimates pavement fatigue life ratio directly from TSDD slope
responses and structural inputs. FLR expresses the ratio of remaining fatigue
life to initial fatigue life as a percentage.

## Physics-guided data generation

The associated study created an analytical database using viscoelastic
pavement simulations. Actual pavement structures were used as structural
templates, and multiple damage levels and five representative binder grades
were evaluated. The simulated responses linked full TSDD slope profiles,
pavement structure, material condition, and calculated fatigue life.

## Model inputs

The final FLR formulation uses:

- Ten TSDD slope measurements.
- AC layer thickness.
- Damaged AC dynamic modulus at 25 Hz.
- Binder grade as a model-routing variable.

The dynamic damaged modulus was an influential input, but the model also uses
the complete slope pattern and AC thickness.

## Binder-specific models

One XGBoost regressor was trained for each supported binder. The filtered
database was randomly split into an 80% development portion and a 20% final
evaluation portion using `random_state=42`. Hyperparameters were selected
using a randomized search over 20 configurations with five-fold
cross-validation. The five binder-specific models were then evaluated through
a consolidated router on the separate, unseen 20% synthetic test set.

The public implementation uses ordinary Python routing rather than serializing
the notebook-defined router class. This avoids the portability problem of
loading a custom class stored under a notebook's `__main__` namespace.

## Public model format

The verified XGBoost estimators were exported from joblib memory snapshots to
XGBoost's native UBJ model format. Conversion tests confirmed zero numerical
difference between predictions from the source Booster objects and reloaded
UBJ artifacts for the verification inputs.

## Inference sequence

1. Validate required columns, units that can be checked numerically, and
   supported binder grade.
2. Arrange the 12 numerical features in the exact training order.
3. Select the XGBoost model associated with the binder.
4. Produce the raw FLR regression output.
5. Report FLR within [0, 100]. Capping above 100 follows the original notebook
   router; clipping negative values to zero is an explicit public-reporting
   safeguard because negative FLR has no physical interpretation.

## Reproducibility boundary

This is an inference release. It preserves model files, parameters, feature
metadata, checksums, and prediction behavior. It does not include the synthetic
training database and therefore does not independently reproduce training or
the reported evaluation statistics.
