"""Dependency-light release checks that do not require pytest."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from flr_model import FLRPredictor, InputValidationError, SUPPORTED_BINDERS


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    inputs = pd.read_csv(ROOT / "examples" / "example_input.csv")
    expected = pd.read_csv(ROOT / "examples" / "example_output.csv")
    predictor = FLRPredictor()
    actual = predictor.predict_frame(inputs)

    assert tuple(actual["binder_grade"]) == SUPPORTED_BINDERS
    assert "flr_raw_percent" not in actual.columns
    assert np.isfinite(actual["flr_percent"]).all()
    assert actual["flr_percent"].between(0, 100).all()
    np.testing.assert_allclose(
        actual["flr_percent"],
        expected["flr_percent"],
        rtol=0,
        atol=1e-6,
    )

    missing = inputs.drop(columns=["ac_thickness_mm"])
    try:
        predictor.predict_frame(missing)
    except InputValidationError:
        pass
    else:
        raise AssertionError("Missing required column was not rejected.")

    manifest_path = (
        ROOT / "src" / "flr_model" / "models" / "model_manifest.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert tuple(manifest["models"]) == SUPPORTED_BINDERS
    assert all(
        details["conversion_max_abs_difference"] == 0.0
        for details in manifest["models"].values()
    )

    print("Smoke test passed: five models, reference outputs, and validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
