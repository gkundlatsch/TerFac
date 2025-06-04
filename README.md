# TerFac (Terminator Factory)

TerFac is a web-based tool for designing and generating ρ-independent (intrinsic) transcription terminators with a user-defined target strength. It uses a pre-trained machine-learning model to optimize nucleotide composition and secondary-structure features (A-tract, U-tract, hairpin, loop) and returns a predicted-strength value along with the corresponding terminator sequence.

**Online Demo & Documentation:**  
[TerFac Web Application](https://www2.fcfar.unesp.br/#!/instituicao/departamentos/bioprocessos-e-biotecnologia-novo/laboratorios/synbio/terfac)  
**GitHub Repository:**  
https://github.com/gkundlatsch/TerFac

IMPORTANT: If you are only interested in a terminator with maximum strength, they were already calculated and are stored in max_strength.html

If you want to run TerFac locally, please check the offline repository: https://github.com/gkundlatsch/TerFac-offline

## Features

- **Target‐Strength Optimization**  
  Uses a trained XGBoost/Scikit-Learn model (`terminator_strength_predictor.joblib`) to predict terminator strength and guide a Differential Evolution (DE) optimizer.

- **Discrete Feature Mapping**  
  Snaps continuous DE candidates to biologically valid discrete feature values using precomputed CSV mappings for:
  - A-tract features (`Atract_feature_mapping_normalized.csv`)
  - U-tract features (`Utract_feature_mapping_normalized.csv`)
  - Hairpin features (`Hairpin_feature_mapping_normalized.csv`)
  - Loop features (`Loop_feature_mapping_normalized.csv`)

- **Asynchronous Background Processing**  
  Enqueues bioinformatics‐heavy optimization jobs in Redis via RQ to avoid request timeouts.

- **Web Interface**  
  Built with Flask; users specify a desired terminator strength and (optionally) advanced parameters. Results display optimized sequence, predicted strength, feature breakdown, and progress logs.

TerFac/
├── .gitattributes
├── .gitignore
├── Atract_feature_mapping_normalized.csv
├── Hairpin_feature_mapping_normalized.csv
├── Loop_feature_mapping_normalized.csv
├── Procfile
├── Utract_feature_mapping_normalized.csv
├── app.py
├── app.yaml
├── requirements.txt
├── runtime.txt
├── sequence_generator2_6.py
├── tasks.py
├── templates/
│   ├── error.html
│   ├── index.html
│   ├── results.html
│   ├── max_strength.html
│   └── status.html
└── terminator_strength_predictor.joblib

If you have any questions or suggestions, you can find more information about our research group here: https://www2.fcfar.unesp.br/#!/instituicao/departamentos/bioprocessos-e-biotecnologia-novo/laboratorios/synbio/contact/
