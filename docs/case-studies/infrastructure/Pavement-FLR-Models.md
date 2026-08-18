# Pavement Fatigue Life Ratio Models

**Contributor:** Federal Highway Administration (FHWA)  
**Primary Domain:** Infrastructure Inspection & NDE  
**Date Published:** 2026-08-18  
**Repository Link:** [View Code](https://github.com/TFHRC-AI-CODE/AI-CODE/tree/main/AI%20Applications/Office%20of%20Infrastructure%20Research%20and%20Development/Pavement-FLR-Models) 

Overview
--------

This repository provides the five binder-specific XGBoost models developed in
the associated study to estimate pavement fatigue life ratio (FLR) from
Traffic Speed Deflection Device (TSDD) slope measurements and pavement
structural inputs.

FLR compares the predicted fatigue life of a pavement in its damaged condition
with the predicted fatigue life of the same pavement in its initial,
undamaged condition:

```text
FLR (%) = Nf(damaged) / Nf(initial) x 100
```

Higher FLR indicates that a greater proportion of the initial fatigue capacity
remains. FLR is a normalized structural condition indicator; it is not a
prediction of remaining service life in years.

The release is intended to make the trained FLR models transparent and usable
for research and network-level pavement screening. It is not a substitute for
project-level investigation, testing, design, or professional engineering
judgment.

## Why this matters

TSDDs can collect large volumes of pavement structural-response data at
traffic speed. These models provide a practical way to convert the full TSDD
slope profile, together with AC thickness, damaged AC modulus, and binder
grade, into a consistent fatigue-related structural indicator for many
pavement segments.

The associated study showed that this multi-parameter approach predicts FLR
more effectively than relationships based on a single TSDD index alone.
Making the trained models publicly accessible supports reproducible analysis,
large-scale structural screening, comparison across surveys, and more informed
prioritization of locations that may warrant detailed engineering evaluation.

## What this repository provides

- Five trained XGBoost models, one for each supported binder grade.
- A Python interface that validates inputs and routes each record to the
  appropriate binder-specific model.
- Command-line prediction for CSV files.
- Verified examples drawn from the study's held-out synthetic test partition.
- Model documentation, limitations, provenance, validation results, and
  artifact checksums.
- Automated tests for loading, prediction, routing, and invalid inputs.

This is an **inference release**. It allows users to apply the trained FLR
models, but it does not include the synthetic training database, training
notebooks, or training scripts.

## Required information

Each prediction requires:

| Input | Requirement |
|---|---|
| Binder grade | PG 46-40, PG 58-34, PG 64-28, PG 70-22, or PG 76-10 |
| TSDD slopes | Ten slopes at -450, -300, -200, +100, +200, +300, +450, +600, +900, and +1500 mm |
| Slope unit | Micrometers per meter (&micro;m/m) |
| Slope reference condition | Corrected to 20&deg;C |
| AC thickness | Millimeters (mm) |
| Damaged AC modulus | Dynamic modulus at 25 Hz in MPa |

Binder grade selects the appropriate model and is not used as a numerical
feature. The models do not interpolate between binder grades. Users should
select the supported binder that is technically most representative of the
pavement being evaluated.

See the [input data dictionary](docs/input_data_dictionary.md) for exact CSV
column names and preparation requirements.

> **Important:** The package cannot determine from the input numbers whether
> slope temperature correction, modulus definition, frequency, or units are
> correct. Those checks remain the user's responsibility.

## AC modulus requirement

The FLR models require damaged AC dynamic modulus at 25 Hz as an input; they do
not calculate it. The value may come from laboratory testing, calibrated
pavement analysis, or another technically appropriate source.

The associated study also developed a Random Forest model to estimate AC
modulus from TSDD slopes and layer thicknesses. Its serialized artifact is
approximately 7 GB and is not included in this GitHub release. Researchers
interested in possible access to the companion model may contact the
corresponding author to discuss availability.

## Installation

Python 3.10 or newer is recommended.

```bash
cd Pavement-FLR-GitHub
python -m venv .venv
```

Activate the environment, then install:

```bash
python -m pip install .
```

For development and testing:

```bash
python -m pip install ".[test]"
python -m pytest
```

## Predict from a CSV

The example file contains one verified synthetic test record for each binder:

```bash
predict-flr examples/example_input.csv predictions.csv
```

The standard output contains:

- `flr_percent`: the reported prediction, bounded to the physical interval
  from 0% to 100%.
- `prediction_note`: a note when the raw regression result was clipped.

To include the unchanged XGBoost regression output:

```bash
predict-flr examples/example_input.csv predictions.csv --include-raw
```

This adds `flr_raw_percent`. The original study router capped predictions above
100%. The public interface also reports negative predictions as zero because a
negative FLR has no physical meaning. This reporting safeguard does not alter
the trained models, and it does not make an out-of-domain prediction reliable.

## Use from Python

The following record is an actual synthetic example from the study's held-out
test partition:

```python
from flr_model import FLRPredictor

inputs = {
    "binder_grade": "PG 46-40",
    "slope_m450_um_per_m": -229.156383,
    "slope_m300_um_per_m": -265.020643,
    "slope_m200_um_per_m": -225.252756,
    "slope_p100_um_per_m": 272.803474,
    "slope_p200_um_per_m": 244.560419,
    "slope_p300_um_per_m": 206.941119,
    "slope_p450_um_per_m": 156.716945,
    "slope_p600_um_per_m": 118.268453,
    "slope_p900_um_per_m": 70.080169,
    "slope_p1500_um_per_m": 27.015900,
    "ac_thickness_mm": 233.60,
    "damaged_ac_modulus_25hz_mpa": 1223.072362,
}

flr_percent = FLRPredictor().predict_one(inputs)
print(f"{flr_percent:.3f}%")  # 33.218%
```

The bundled examples are physics-guided synthetic study cases, not field
measurements, calibration targets, or recommended pavement designs. Their
reference FLR values are stored separately in
`examples/example_reference.csv` and are never passed to the predictor.

## Study basis and reported performance

The models were developed using a physics-guided analytical database generated
through viscoelastic pavement simulations using actual pavement structures as
structural templates, five representative binder grades, and multiple damage
levels. The database was randomly divided into 80% for model development and
20% for final evaluation. A separate model was trained for each binder using
randomized hyperparameter search and five-fold cross-validation. The
binder-specific models were then evaluated together on the separate, unseen
20% final test set.

On the unseen 20% synthetic test set, the consolidated binder-routed framework
reported:

| Metric | Result |
|---|---:|
| R-squared | 0.990 |
| RMSE | 3.452 percentage points |
| MAE | 1.504 percentage points |

These results demonstrate strong agreement within the simulated study domain.
They are not evidence of comprehensive validation across field devices,
agencies, climates, pavement systems, or time periods.

The study also applied the complete framework to TSD data collected in 2020
and 2023 on the Roskilde temperature loop in Denmark. The resulting FLR
distributions were directionally consistent with gradual structural
deterioration across the two surveys. The paper describes this field
application as an initial implementation and partial verification; broader
long-term field evaluation remains necessary.

## What is intentionally excluded

- The approximately 7 GB companion Random Forest AC-modulus model.
- The synthetic model-development database.
- Raw development notebooks and training scripts.
- Joblib model snapshots and the notebook-defined consolidated router.
- The publisher-formatted article PDF.

These exclusions do not prevent FLR prediction when the user supplies the
required damaged AC dynamic modulus.

## Documentation and verification

- [Model card](MODEL_CARD.md)
- [Model validation and alignment report](VALIDATION.md)
- [Input data dictionary](docs/input_data_dictionary.md)
- [Methodology](docs/methodology.md)
- [Intended use, limitations, and disclaimer](docs/limitations.md)
- [Model provenance](docs/provenance.md)

The five native UBJ artifacts reproduce the verified source models exactly at
the raw-prediction level across all 8,837 records in the reconstructed
held-out test partition. See [VALIDATION.md](VALIDATION.md) for the evidence
and scope of that statement.

Model-file integrity can be checked with:

```bash
python tools/verify_checksums.py
```

## Citation

If these models contribute to a publication, technical report, or engineering
study, please cite:

> Nasimifar, M., Nadkarni, A., Zabihi, S., and Sivaneswaran, N. (2026).
> "Machine-learning prediction of pavement fatigue life ratio from structural
> inputs and TSDD measurements using physics-guided data generation."
> *Construction and Building Materials*, 538, 147352.
> https://doi.org/10.1016/j.conbuildmat.2026.147352

Machine-readable citation metadata is provided in [CITATION.cff](CITATION.cff).

## License

The code, documentation, and released model artifacts are provided under the
[Apache License 2.0](LICENSE).

## Disclaimer

The models and accompanying materials are provided on an "as is" basis for
research, informational, and pavement-management screening purposes. No
warranty is made regarding accuracy, completeness, suitability, or performance
for a particular application. Users are responsible for input quality,
engineering interpretation, and independent verification.

No FHWA branding, seal, or logo is used. Reference to the associated study,
authors, organizations, or funding source does not imply endorsement of this
repository or of results produced by third parties.

## Contact

For technical questions, open an issue in this repository. Questions about the
associated study or possible access to the companion AC-modulus model may be
directed to the corresponding author, Mahdi Nasimifar
(`mnasimifar@agr-us.com`).
