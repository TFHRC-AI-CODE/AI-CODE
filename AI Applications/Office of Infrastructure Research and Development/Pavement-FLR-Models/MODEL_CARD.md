# Model Card: Pavement Fatigue Life Ratio Models

## Model summary

This release contains five gradient-boosted tree regression models that
estimate pavement fatigue life ratio (FLR), expressed as a percentage. A
separate model is provided for each supported asphalt binder grade, and the
public predictor selects the appropriate model from the input binder.

| Item | Description |
|---|---|
| Model family | XGBoost regressors |
| Task | Regression |
| Output | Fatigue life ratio (%) |
| Model count | Five binder-specific models |
| Release | 1.0.0 |
| Native format | XGBoost UBJ |
| Reference slope temperature | 20°C |

## Supported binder grades

- PG 46-40
- PG 58-34
- PG 64-28
- PG 70-22
- PG 76-10

The models do not interpolate between binder grades. Users must select the
supported grade that is technically appropriate for their application.

## Inputs

The models use 12 numerical features:

1. TSDD slope at -450 mm (µm/m)
2. TSDD slope at -300 mm (µm/m)
3. TSDD slope at -200 mm (µm/m)
4. TSDD slope at +100 mm (µm/m)
5. TSDD slope at +200 mm (µm/m)
6. TSDD slope at +300 mm (µm/m)
7. TSDD slope at +450 mm (µm/m)
8. TSDD slope at +600 mm (µm/m)
9. TSDD slope at +900 mm (µm/m)
10. TSDD slope at +1500 mm (µm/m)
11. AC thickness (mm)
12. Damaged AC dynamic modulus at 25 Hz (MPa)

Binder grade is a routing variable and is not passed as a numerical model
feature. Exact public column names are listed in
`docs/input_data_dictionary.md`.

## Output

FLR is defined as the remaining fatigue life divided by the initial fatigue
life, multiplied by 100. Higher values indicate a greater proportion of
remaining fatigue life relative to the initial state.

The standard inference output is clipped to the physically meaningful interval
[0, 100]. The original notebook router capped values above 100; this public
interface additionally replaces negative results with zero because negative
FLR has no physical interpretation. The unchanged regression output can be
requested through an advanced option. Clipping does not make an out-of-domain
prediction reliable.

## Development data

The models were developed primarily from a physics-guided database generated
using viscoelastic pavement simulations across:

- Actual pavement structures used as structural templates.
- Multiple damage levels.
- Five representative binder grades.
- TSDD slope responses and structural variables.

The synthetic training database is not distributed with this release.
Consequently, this repository supports inference and model transparency but
does not independently reproduce model training.

## Training approach

The filtered database was randomly split into an 80% development portion and
a 20% final evaluation portion using a fixed random state of 42. A separate
XGBoost model was developed for each binder. Hyperparameter optimization used
a randomized search over 20 sampled configurations with five-fold
cross-validation.

| Binder | Learning rate | Max depth | Estimators | Subsample | Column sample | Reg. alpha | Reg. lambda |
|---|---:|---:|---:|---:|---:|---:|---:|
| PG 46-40 | 0.10 | 10 | 300 | 0.8 | 0.8 | 0 | 5 |
| PG 58-34 | 0.10 | 10 | 300 | 0.8 | 0.8 | 0 | 5 |
| PG 64-28 | 0.10 | 10 | 300 | 0.8 | 0.8 | 0 | 5 |
| PG 70-22 | 0.10 | 10 | 200 | 0.6 | 0.6 | 1 | 5 |
| PG 76-10 | 0.05 | 10 | 300 | 0.6 | 0.8 | 0 | 5 |

## Evaluation

The consolidated binder-routed framework achieved the following performance
on the separate, unseen 20% synthetic test set:

| Metric | Result |
|---|---:|
| R² | 0.990 |
| MAE | 1.504 percentage points |
| RMSE | 3.452 percentage points |

These values match the final development notebook and the rounded results
reported in the paper. They demonstrate strong predictive agreement within
the simulated study domain.

## Intended uses

- Research involving TSDD structural measurements.
- Network-level pavement structural screening.
- Batch analysis of large TSDD datasets using a consistent FLR framework.
- Exploration of FLR as an additional pavement-management indicator.
- Reproduction of inference from the associated study.
- Integration into transparent research workflows with appropriate review.

## Uses requiring caution or outside scope

- Project-level design or rehabilitation selection without additional testing.
- Safety-critical or contractual decisions based solely on model output.
- Inputs with unverified units or temperature correction.
- Binder grades outside the five supported categories.
- Pavement structures or response patterns outside the development domain.
- Treating model output as a direct measurement of remaining service life.
- Using a modulus value that does not represent damaged AC dynamic modulus at
  25 Hz in MPa.

## Known limitations

- Development relied mainly on physics-based simulated data.
- The complete framework was applied to 2020 and 2023 TSD surveys on the
  Roskilde temperature loop, where FLR distributions were directionally
  consistent with gradual deterioration. The paper describes this as an
  initial implementation and partial verification rather than comprehensive
  field validation.
- Training-domain numerical ranges are not enforced in this public release
  because the source database is not distributed.
- The software cannot determine whether slopes were correctly adjusted to
  20°C.
- The nearest supported binder may not adequately represent every mixture.
- Uncertainty intervals are not provided.
- The models may produce raw values outside [0, 100] for unusual inputs.
  The standard reported value is clipped to [0, 100], while the unchanged raw
  output remains available through an advanced option.

## AC modulus dependency

The FLR models do not estimate damaged AC modulus. Users must supply damaged AC
dynamic modulus at 25 Hz in MPa from an appropriate source.

A companion Random Forest modulus model was developed in the study, but its
approximately 7 GB serialized artifact is not included. Researchers may
contact the repository maintainer about possible access.

## Ethical and engineering considerations

Model results should be interpreted together with data quality, local
conditions, uncertainty, and professional engineering judgment. A single
numerical output should not replace inspection, testing, mechanistic analysis,
or an agency's established decision process.

## Provenance and integrity

The five public UBJ artifacts were exported from the verified joblib models
associated with the final development notebook. Checksums and conversion
equivalence records are stored in
`src/flr_model/models/model_manifest.json`.

## Contact

For technical questions, open an issue in the public repository. Questions
about the associated study or possible access to the companion AC-modulus
model may be directed to the corresponding author, Mahdi Nasimifar
(`mnasimifar@agr-us.com`).
