# GBM Survival Mamba Prediction

This project implements a Mamba-based survival prediction model for Glioblastoma Multiforme (GBM) data from TCGA.

## Project Structure

- `data/`: Raw and processed TCGA data.
- `models/`: Neural network architectures (Denoising Autoencoder, Mamba, Survival Net).
- `utils/`: Data loaders, preprocessing functions, loss functions, and metrics.
- `scripts/`: Implementation of training and evaluation pipelines.
- `configs/`: Hyperparameter configurations.
- `notebooks/`: Exploratory Data Analysis and visualization.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Preprocess data:
   ```bash
   python scripts/preprocess_data.py
   ```

3. Train Autoencoder (Unsupervised):
   ```bash
   python scripts/train_ae.py
   ```

4. Train Survival Mamba:
   ```bash
   python scripts/train_mamba.py
   ```

5. Evaluate model:
   ```bash
   python scripts/evaluate.py
   ```
