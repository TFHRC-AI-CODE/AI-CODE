"""Run the bundled illustrative CSV example."""

from pathlib import Path

import pandas as pd

from flr_model import FLRPredictor


HERE = Path(__file__).resolve().parent
inputs = pd.read_csv(HERE / "example_input.csv")
predictions = FLRPredictor().predict_frame(inputs)
predictions.to_csv(HERE / "example_output.csv", index=False)

print(predictions[["binder_grade", "flr_percent"]].to_string(index=False))

