from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from flr_model import FLRPredictor


ROOT = Path(__file__).resolve().parents[1]


def test_bundled_reference_predictions() -> None:
    inputs = pd.read_csv(ROOT / "examples" / "example_input.csv")
    expected = pd.read_csv(ROOT / "examples" / "example_output.csv")
    actual = FLRPredictor().predict_frame(inputs)

    np.testing.assert_allclose(
        actual["flr_percent"],
        expected["flr_percent"],
        rtol=0,
        atol=1e-6,
    )
