"""Command-line interface for batch FLR prediction."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .predictor import FLRPredictor, InputValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Predict pavement fatigue life ratio (FLR) from a CSV file."
    )
    parser.add_argument("input_csv", type=Path, help="CSV containing model inputs")
    parser.add_argument("output_csv", type=Path, help="Destination CSV")
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=None,
        help="Optional directory containing the five UBJ models and manifest",
    )
    parser.add_argument(
        "--no-clip",
        action="store_true",
        help="Do not clip reported FLR values to the physical range [0, 100]",
    )
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Include the direct XGBoost output as flr_raw_percent",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        frame = pd.read_csv(args.input_csv)
        from .predictor import PredictionOptions

        predictor = FLRPredictor(
            model_dir=args.model_dir,
            options=PredictionOptions(
                clip_to_physical_range=not args.no_clip,
                include_raw_prediction=args.include_raw,
            ),
        )
        result = predictor.predict_frame(frame)
        args.output_csv.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(args.output_csv, index=False)
    except (FileNotFoundError, InputValidationError, pd.errors.ParserError) as exc:
        raise SystemExit(f"Prediction failed: {exc}") from exc

    print(f"Wrote {len(result)} prediction(s) to {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
