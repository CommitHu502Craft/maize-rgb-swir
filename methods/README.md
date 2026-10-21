# Method implementation functions

These modules contain exact function/class/constant definitions extracted from the research implementation; historical experiment drivers, filesystem loaders and unused model dependencies are omitted. They are callable library functions, not full training or analysis pipelines.

| Module | Scope and required inputs |
| --- | --- |
| board_geometry.py | Eight checkerboard-plane geometric measurements and replacement of the first eight RGB feature columns; accepts an instance mask and calibrated transformation matrices |
| physical_crop.py | Masked 224 × 224 fixed-field RGB crop; accepts aligned RGB/label arrays and the analysis-to-checkerboard transformation. A field of 1.7 checker squares corresponds to 17 mm for the recorded 10 mm checker spacing |
| donor_reassignment.py | Same-group, cross-tray, cross-variety and fold-matched donor-index rules; balanced-subset selection accepts the original row table and a caller-supplied random generator |
| group_sharing.py | SGSEF evaluation of supplied selected seed indices, fitted D/S probabilities and homogeneous-tray labels; includes matched D and full SD endpoints |

These functions do not run on import. Geometry/crops require OpenCV; group-sharing metrics require scikit-learn; donor functions use NumPy/Pandas. The optional pyproject.toml records a separate environment. The portable result replay needs neither OpenCV nor scikit-learn. The archived protocol fixes the class order, which also matches group_sharing.py.

For M, board_geometry.py replaces pixel geometry with physical geometry; it is not the entire 28-feature extraction/model-fitting pipeline. The retained 18 color statistics and two near-saturation proportions are specified in the article's Supplementary Methods. Images, calibration matrices and model checkpoints are not part of this result-data release. No new donor assignments or sharing simulations were generated during packaging.
