# Input Data Dictionary

## Required CSV columns

| Column | Type | Unit | Description |
|---|---|---|---|
| `binder_grade` | Text | — | Supported binder grade used to select the model |
| `slope_m450_um_per_m` | Number | µm/m | TSDD slope at -450 mm |
| `slope_m300_um_per_m` | Number | µm/m | TSDD slope at -300 mm |
| `slope_m200_um_per_m` | Number | µm/m | TSDD slope at -200 mm |
| `slope_p100_um_per_m` | Number | µm/m | TSDD slope at +100 mm |
| `slope_p200_um_per_m` | Number | µm/m | TSDD slope at +200 mm |
| `slope_p300_um_per_m` | Number | µm/m | TSDD slope at +300 mm |
| `slope_p450_um_per_m` | Number | µm/m | TSDD slope at +450 mm |
| `slope_p600_um_per_m` | Number | µm/m | TSDD slope at +600 mm |
| `slope_p900_um_per_m` | Number | µm/m | TSDD slope at +900 mm |
| `slope_p1500_um_per_m` | Number | µm/m | TSDD slope at +1500 mm |
| `ac_thickness_mm` | Number | mm | Asphalt concrete layer thickness |
| `damaged_ac_modulus_25hz_mpa` | Number | MPa | Damaged AC dynamic modulus at 25 Hz |

`m` and `p` in the slope column names denote negative and positive sensor
offsets, respectively. They do not denote the sign of the measured value.

## Binder values

The preferred values are:

```text
PG 46-40
PG 58-34
PG 64-28
PG 70-22
PG 76-10
```

The predictor also accepts the same grades without `PG`, such as `76-10`.

## Input preparation requirements

- Slopes must be in µm/m.
- Slopes must be corrected to the 20°C reference condition used in the study.
- AC thickness must be in mm and greater than zero.
- Damaged AC modulus must be the dynamic modulus at 25 Hz in MPa and greater
  than zero.
- All values must be finite and numeric.
- Missing inputs are not imputed.
- Rows are not automatically rejected as out of domain because the training
  database and its authoritative operational bounds are not part of this
  release.

## Output columns

| Column | Unit | Description |
|---|---|---|
| `flr_percent` | % | Reported FLR clipped to [0, 100] by default |
| `prediction_note` | — | Indicates whether the raw result was clipped |

Advanced users may request `flr_raw_percent`, the direct XGBoost regression
output, by using the command-line option `--include-raw` or setting
`PredictionOptions(include_raw_prediction=True)` in Python.
