# Intended Use, Limitations, and Disclaimer

## Intended use

The models are intended for research, informational analysis, and
network-level pavement-management screening using appropriately processed TSDD
measurements and pavement inputs.

## Limitations

1. **Simulation-based development.** The models were developed primarily from
   physics-based simulated responses. Strong agreement within that domain does
   not guarantee equivalent performance for every field condition.
2. **Initial field verification.** The complete framework was applied to 2020
   and 2023 TSD surveys on the Roskilde temperature loop. The FLR distributions
   were directionally consistent with gradual deterioration, providing an
   initial implementation and partial verification. Broader long-term field
   evaluation is still needed.
3. **Required modulus.** Users must provide damaged AC dynamic modulus at
   25 Hz in MPa. Incorrect frequency, definition, temperature basis, or units
   can invalidate a result.
4. **Temperature correction.** TSDD slopes must be adjusted to the 20°C
   reference condition. The package cannot verify that preprocessing step.
5. **Supported binders only.** The model supports five binder grades and does
   not interpolate between them.
6. **Domain uncertainty.** Numerical training-domain bounds are not enforced
   because the synthetic database is not distributed in this release.
7. **No uncertainty interval.** Predictions are point estimates.
8. **Output bounds.** The original router capped predictions above 100 but did
   not replace negative values with zero. The public interface additionally
   clips negative results to zero because negative FLR has no physical
   interpretation. The unchanged raw result remains available through an
   advanced option. Clipping is not evidence that an unusual prediction is
   reliable.

## Not appropriate as the sole basis for

- Project-level pavement design.
- Rehabilitation or funding decisions.
- Acceptance, warranty, or contractual determinations.
- Conclusions about public safety.
- Replacement of coring, laboratory testing, structural investigation, or
  professional engineering review.

## Disclaimer

The models and accompanying materials are provided on an "as is" basis,
without warranties or conditions of any kind. No warranty is made regarding
accuracy, completeness, non-infringement, merchantability, suitability, or
fitness for a particular purpose. Users are responsible for determining
whether the models are appropriate for their data and application and assume
the risks associated with use.

Use of names associated with the study does not imply endorsement of this
implementation or of results produced by third parties. No FHWA branding,
seal, or logo is included or authorized by this repository.

This project-specific statement supplements, but does not replace, the terms
of the repository license.
