"""Binder-routed inference for the pavement fatigue life ratio models."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
import xgboost as xgb


PUBLIC_TO_MODEL_FEATURES: dict[str, str] = {
    "slope_m450_um_per_m": "S_450_µm_per_m",
    "slope_m300_um_per_m": "S_300_µm_per_m",
    "slope_m200_um_per_m": "S_200_µm_per_m",
    "slope_p100_um_per_m": "S100_µm_per_m",
    "slope_p200_um_per_m": "S200_µm_per_m",
    "slope_p300_um_per_m": "S300_µm_per_m",
    "slope_p450_um_per_m": "S450_µm_per_m",
    "slope_p600_um_per_m": "S600_µm_per_m",
    "slope_p900_um_per_m": "S900_µm_per_m",
    "slope_p1500_um_per_m": "S1500_µm_per_m",
    "ac_thickness_mm": "AC_(mm)",
    "damaged_ac_modulus_25hz_mpa": "DM_@_25_Hz_(Mpa)",
}

NUMERIC_INPUT_COLUMNS = tuple(PUBLIC_TO_MODEL_FEATURES)
INPUT_COLUMNS = ("binder_grade", *NUMERIC_INPUT_COLUMNS)
SUPPORTED_BINDERS = ("PG 46-40", "PG 58-34", "PG 64-28", "PG 70-22", "PG 76-10")

_BINDER_ALIASES = {
    "46-40": "PG 46-40",
    "PG46-40": "PG 46-40",
    "PG 46-40": "PG 46-40",
    "58-34": "PG 58-34",
    "PG58-34": "PG 58-34",
    "PG 58-34": "PG 58-34",
    "64-28": "PG 64-28",
    "PG64-28": "PG 64-28",
    "PG 64-28": "PG 64-28",
    "70-22": "PG 70-22",
    "PG70-22": "PG 70-22",
    "PG 70-22": "PG 70-22",
    "76-10": "PG 76-10",
    "PG76-10": "PG 76-10",
    "PG 76-10": "PG 76-10",
}


class InputValidationError(ValueError):
    """Raised when model inputs are missing, malformed, or physically invalid."""


@dataclass(frozen=True)
class PredictionOptions:
    """Controls post-processing of raw model predictions."""

    clip_to_physical_range: bool = True
    include_raw_prediction: bool = False


class FLRPredictor:
    """Load the five native XGBoost models and route rows by binder grade."""

    def __init__(
        self,
        model_dir: str | Path | None = None,
        *,
        options: PredictionOptions | None = None,
    ) -> None:
        package_models = Path(__file__).resolve().parent / "models"
        self.model_dir = Path(model_dir) if model_dir else package_models
        self.options = options or PredictionOptions()
        self._manifest = self._load_manifest()
        self._models: dict[str, xgb.Booster] = {}

    @property
    def manifest(self) -> Mapping[str, Any]:
        return self._manifest

    def _load_manifest(self) -> dict[str, Any]:
        path = self.model_dir / "model_manifest.json"
        if not path.is_file():
            raise FileNotFoundError(f"Model manifest not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _model_for(self, binder: str) -> xgb.Booster:
        if binder not in self._models:
            filename = self._manifest["models"][binder]["file"]
            path = self.model_dir / filename
            if not path.is_file():
                raise FileNotFoundError(f"Model file not found for {binder}: {path}")
            booster = xgb.Booster()
            booster.load_model(path)
            expected = list(PUBLIC_TO_MODEL_FEATURES.values())
            if booster.feature_names != expected:
                raise RuntimeError(
                    f"Unexpected feature metadata in {path.name}. "
                    f"Expected {expected}, found {booster.feature_names}."
                )
            self._models[binder] = booster
        return self._models[binder]

    @staticmethod
    def _normalise_binder(value: object) -> str:
        key = " ".join(str(value).strip().upper().split())
        key = key.replace("PG ", "PG ")
        canonical = _BINDER_ALIASES.get(key)
        if canonical is None:
            allowed = ", ".join(SUPPORTED_BINDERS)
            raise InputValidationError(
                f"Unsupported binder grade {value!r}. Supported grades: {allowed}."
            )
        return canonical

    @staticmethod
    def validate_frame(frame: pd.DataFrame) -> pd.DataFrame:
        """Return a validated copy with canonical binders and numeric inputs."""

        if not isinstance(frame, pd.DataFrame):
            raise InputValidationError("Input must be a pandas DataFrame.")
        missing = [name for name in INPUT_COLUMNS if name not in frame.columns]
        if missing:
            raise InputValidationError(
                "Missing required input column(s): " + ", ".join(missing)
            )
        if frame.empty:
            raise InputValidationError("Input contains no rows.")

        clean = frame.loc[:, INPUT_COLUMNS].copy()
        clean["binder_grade"] = clean["binder_grade"].map(
            FLRPredictor._normalise_binder
        )

        for column in NUMERIC_INPUT_COLUMNS:
            clean[column] = pd.to_numeric(clean[column], errors="coerce")

        invalid_numeric = clean[list(NUMERIC_INPUT_COLUMNS)].isna()
        if invalid_numeric.any().any():
            locations = [
                f"row {index}, {column}"
                for index, row in invalid_numeric.iterrows()
                for column, invalid in row.items()
                if invalid
            ]
            raise InputValidationError(
                "Missing or nonnumeric value(s): " + "; ".join(locations[:10])
            )

        values = clean[list(NUMERIC_INPUT_COLUMNS)].to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise InputValidationError("All numerical inputs must be finite.")
        if (clean["ac_thickness_mm"] <= 0).any():
            raise InputValidationError("ac_thickness_mm must be greater than zero.")
        if (clean["damaged_ac_modulus_25hz_mpa"] <= 0).any():
            raise InputValidationError(
                "damaged_ac_modulus_25hz_mpa must be greater than zero."
            )
        return clean

    def predict_frame(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Predict FLR for one or more rows.

        Returns the original columns plus:
        - ``flr_percent``: output clipped to the physical interval [0, 100].
        - ``prediction_note``: indicates whether clipping was applied.

        Set ``PredictionOptions(include_raw_prediction=True)`` to include the
        direct XGBoost output as ``flr_raw_percent`` for advanced review.

        The caller is responsible for confirming that slope values have been
        corrected to the 20 degree C reference condition and that all inputs
        are appropriate for the study domain.
        """

        clean = self.validate_frame(frame)
        raw = np.empty(len(clean), dtype=float)

        for binder in SUPPORTED_BINDERS:
            row_positions = np.flatnonzero(
                clean["binder_grade"].to_numpy() == binder
            )
            if not len(row_positions):
                continue
            public_values = clean.iloc[row_positions][
                list(NUMERIC_INPUT_COLUMNS)
            ].copy()
            model_values = public_values.rename(columns=PUBLIC_TO_MODEL_FEATURES)
            matrix = xgb.DMatrix(
                model_values,
                feature_names=list(PUBLIC_TO_MODEL_FEATURES.values()),
            )
            raw[row_positions] = self._model_for(binder).predict(matrix)

        if self.options.clip_to_physical_range:
            reported = np.clip(raw, 0.0, 100.0)
            notes = np.where(
                np.isclose(raw, reported),
                "",
                "raw prediction clipped to the physical range [0, 100]",
            )
        else:
            reported = raw.copy()
            notes = np.full(len(raw), "", dtype=object)

        result = frame.copy()
        result["binder_grade"] = clean["binder_grade"].to_numpy()
        if self.options.include_raw_prediction:
            result["flr_raw_percent"] = raw
        result["flr_percent"] = reported
        result["prediction_note"] = notes
        return result

    def predict_one(self, inputs: Mapping[str, object]) -> float:
        """Predict the reported FLR percentage for a single input mapping."""

        result = self.predict_frame(pd.DataFrame([dict(inputs)]))
        return float(result.loc[result.index[0], "flr_percent"])


def required_columns() -> Sequence[str]:
    """Return the ordered public input schema."""

    return INPUT_COLUMNS
