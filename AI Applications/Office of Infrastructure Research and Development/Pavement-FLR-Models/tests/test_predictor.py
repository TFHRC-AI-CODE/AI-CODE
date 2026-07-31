from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from flr_model import FLRPredictor, InputValidationError, SUPPORTED_BINDERS


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = ROOT / "examples" / "example_input.csv"
MODEL_DIR = ROOT / "src" / "flr_model" / "models"


def example_frame() -> pd.DataFrame:
    return pd.read_csv(EXAMPLE_INPUT)


def test_all_five_models_load_and_predict() -> None:
    result = FLRPredictor().predict_frame(example_frame())
    assert tuple(result["binder_grade"]) == SUPPORTED_BINDERS
    assert "flr_raw_percent" not in result.columns
    assert np.isfinite(result["flr_percent"]).all()
    assert result["flr_percent"].between(0, 100).all()


def test_binder_alias_is_normalised() -> None:
    frame = example_frame().iloc[[0]].copy()
    frame["binder_grade"] = "46-40"
    result = FLRPredictor().predict_frame(frame)
    assert result.iloc[0]["binder_grade"] == "PG 46-40"


def test_missing_column_is_rejected() -> None:
    frame = example_frame().drop(columns=["ac_thickness_mm"])
    with pytest.raises(InputValidationError, match="ac_thickness_mm"):
        FLRPredictor().predict_frame(frame)


def test_nonpositive_modulus_is_rejected() -> None:
    frame = example_frame().iloc[[0]].copy()
    frame["damaged_ac_modulus_25hz_mpa"] = 0
    with pytest.raises(InputValidationError, match="greater than zero"):
        FLRPredictor().predict_frame(frame)


def test_unknown_binder_is_rejected() -> None:
    frame = example_frame().iloc[[0]].copy()
    frame["binder_grade"] = "PG 99-99"
    with pytest.raises(InputValidationError, match="Unsupported binder"):
        FLRPredictor().predict_frame(frame)


def test_manifest_lists_every_supported_binder() -> None:
    manifest = json.loads(
        (MODEL_DIR / "model_manifest.json").read_text(encoding="utf-8")
    )
    assert tuple(manifest["models"]) == SUPPORTED_BINDERS
    for details in manifest["models"].values():
        assert (MODEL_DIR / details["file"]).is_file()
        assert details["conversion_max_abs_difference"] == 0.0


def test_raw_prediction_is_available_as_advanced_option() -> None:
    from flr_model import PredictionOptions

    result = FLRPredictor(
        options=PredictionOptions(include_raw_prediction=True)
    ).predict_frame(example_frame().iloc[[0]])
    assert np.isfinite(result.iloc[0]["flr_raw_percent"])
