# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a quantum machine learning (QML) research codebase focused on applying variational quantum algorithms to biomedical signal processing and time-series analysis. The repository implements various quantum neural network architectures for EEG/fMRI data classification, regression, and time-series prediction using hybrid classical-quantum neural networks.

**Primary Research Focus**: EEG signal analysis, fMRI data processing, and response time prediction through quantum transformers, quantum CNNs, and hybrid temporal convolutional networks.

## Environment Setup

### Conda Environment
```bash
conda activate ./conda-envs/qml_eeg
```
This activates a Python 3.11 environment with all quantum machine learning dependencies.

### Key Dependencies
- **Quantum Frameworks**: PennyLane (primary), Qiskit (IBM backend), CUDA-Q (GPU-accelerated)
- **Deep Learning**: PyTorch, TorchVision
- **Signal Processing**: MNE-Python, BrainDecode, Scikit-Learn
- **Utilities**: Pandas, NumPy, Matplotlib, TQDM, Wandb

### Dependency Management
Check dependencies for a specific file:
```bash
python DependencyCheck.py --filename=<script_name>.py
```
This generates a requirements.txt with package versions.

## Common Development Commands

### Running Experiments

**Basic experiment (CPU/GPU auto-detect):**
```bash
python EEGChallenge_QTSTransformer.py \
    --challenge=1 \
    --n-qubits=6 \
    --n-layers=2 \
    --degree=2 \
    --n-epochs=100 \
    --batch-size=32 \
    --lr=1e-3
```

**With mini dataset for testing:**
```bash
python EEGChallenge_QTSTransformer.py --challenge=1 --mini --n-qubits=6 --n-epochs=10
```

**Resume from checkpoint:**
```bash
python EEGChallenge_QTSTransformer.py \
    --challenge=1 \
    --n-qubits=6 \
    --n-epochs=100 \
    --resume \
    --base-path=./checkpoints \
    --job-id=<unique_id>
```

**With Wandb tracking:**
```bash
python EEGChallenge_QTSTransformer.py \
    --challenge=1 \
    --n-qubits=6 \
    --wandb \
    --user_name=<your_name> \
    --model_name=<descriptive_name>
```

### SLURM Job Submission

**Submit a batch job:**
```bash
sbatch EEGChallenge_externalizing_A1.sh
```

**Typical SLURM configuration:**
- Account: `m4138_g` (GPU allocation)
- Constraint: `gpu&hbm80g` (80GB HBM GPU)
- QOS: `shared`
- Time limit: `48:00:00` (48 hours)
- Resources: 1 node, 1 GPU, 32 CPU cores

### Parameter Sweeps

Run hyperparameter sweeps using runner scripts:
```bash
python multichip_run_eeg_new.py      # EEG parameter sweep
python multichip_run_cifar.py        # CIFAR parameter sweep
python multichip_run_synthetic.py    # Synthetic benchmark sweep
```

## High-Level Architecture

### Core Quantum Circuit Framework

**Base Module: `MultiChip.py`**
- Provides foundational variational quantum circuits (VQC)
- Key classes:
  - `VQC`: Basic variational circuit with customizable qubits/depth
  - `VQC_dm`: VQC with density matrix measurement (full quantum state)
  - `VQC_noise`: VQC with noise models (Depolarizing, Amplitude Damping)
  - `QuantumAutoencoder`: Hybrid classical-quantum encoder-decoder
  - `QuantumAutoencoder_Noise`: With quantum error mitigation (ZNE)
- Circuit architecture: RX, RY, RZ, CRX gates with angle embedding
- Multi-chip support: Divides qubits into logical "chips" for distributed processing
- Backend: PennyLane's `lightning.qubit` for efficient simulation

### Model Architectures

**1. Quantum Convolutional Neural Networks (QCNN)**
- Files: `QCNN_EEG.py`, `MultiChip_EEG.py`, `MultiChip_Ensemble.py`
- Purpose: Feature extraction via quantum convolution + pooling
- Architecture flow:
  1. Classical dimension reduction (FC layer → n_qubits)
  2. Variational angle embedding into quantum state
  3. Repeated conv-pool layers with qubit reduction
  4. Parametrized convolutions (U3, IsingXX, IsingYY, IsingZZ gates)
  5. Final measurement on reduced qubit set
- Ensemble variant: Up to 272 parallel quantum circuits

**2. Quantum Temporal Convolutional Networks (QTCN/HQTCN)**
- Files: `HQTCN_NARMA.py`, `HQTCN2_EEG.py`, `HQTCN3_EEG.py`
- Purpose: Time-series processing with quantum feature extraction
- Variants:
  - HQTCN: Classical TCN + quantum convolution blocks
  - HQTCN2: Enhanced pooling mechanisms
  - HQTCN3: Latest version with modified kernel handling
- Applications: NARMA prediction, EEG motor imagery classification

**3. Quantum Transformers (Quixer Models)**
- Files: `QuixerTSModel_Pennylane2.py`, `QuixerTSModel_Pennylane3.py`
- Purpose: Advanced transformer architecture for complex biomedical signals
- Core components:
  - Feature projection: Conv2d with GLU (Gated Linear Unit) activation
  - Quantum transformer core: Multi-layer quantum ansatz circuits
  - Configurable gate sequences: RY, CRX, IsingYY, etc.
  - Multi-observable measurement: PauliX, PauliY, PauliZ
  - Output module: Feed-forward with optional GLU gating
  - QSVT integration: Quantum Singular Value Transformation
- Typical config: 6-8 qubits, 2-3 layers, degree 2-3

**4. Quantum LSTM**
- File: `QLSTM_v0_PhysioNet_EEG.py`
- Purpose: Quantum-enhanced recurrent processing
- Architecture: Classical LSTM with quantum feature extraction gates

### Data Pipeline Architecture

**Data Loading Flow:**
```
Raw Data (EEG/fMRI/Images)
    ↓
LoadData Modules
    ├─ LoadData_MultiChip.py (MNIST, Fashion-MNIST, CIFAR, CelebA)
    ├─ Load_PhysioNet_EEG.py (PhysioNet EEG)
    └─ challenge_dataloaders.py (EEG Challenge 1 & 2)
    ↓
Preprocessing
    ├─ Standardization/Normalization
    ├─ Windowing (time-series)
    ├─ Artifact removal (EEG)
    └─ Train/Val/Test split
    ↓
Quantum Model
    ↓
Training Loop (with noise options)
    ├─ Noiseless: Ideal simulation
    ├─ Noisy: With depolarizing + amplitude damping
    └─ ZNE: Zero-Noise Extrapolation (Richardson method)
    ↓
Evaluation & Checkpointing
    ├─ Metrics: RMSE, AUC, accuracy
    ├─ Checkpoint: .pt model files
    └─ Logging: CSV/JSON results
```

**Key Data Sources:**
- **EEG**: PhysioNet Motor Imagery (64 channels, 160 Hz), EEG Challenge datasets (129 channels, 200 timesteps)
- **fMRI**: ABCD dataset, UK Biobank (various parcellations)
- **Images**: MNIST, Fashion-MNIST, CIFAR-10, CelebA
- **Synthetic**: NARMA time-series, binary classification benchmarks

### Experiment Design Patterns

**Pattern 1: Single Model Training**
```python
# 1. Define runner function factory: get_<ModelName>_run()
# 2. Accept: dataset_name, seed, batch_size, device
# 3. Return: callable function with model hyperparameters
# 4. Training loop: epoch iteration with tqdm progress
# 5. Output: CSV metrics, model checkpoints, optional density matrices
```

**Pattern 2: Noise & Error Mitigation Studies**
- Run three parallel model variants:
  1. Noiseless (ideal quantum simulation)
  2. Noisy (with quantum noise models)
  3. ZNE (quantum error mitigation via extrapolation)
- Compare robustness across variants

**Pattern 3: Multi-Chip Ensembles**
- Scale from 1 → 272 parallel quantum circuits
- Aggregate predictions via voting/averaging
- Analyze chip-count scaling laws

## Directory Structure Key Locations

```
/pscratch/sd/j/junghoon/
├── MultiChip.py                          # Core VQC implementations
├── QCNN_EEG.py                           # Quantum CNN for EEG
├── HQTCN2_EEG.py, HQTCN3_EEG.py          # Hybrid quantum TCN variants
├── QuixerTSModel_Pennylane2.py           # Main quantum transformer
├── EEGChallenge_QTSTransformer.py        # Challenge competition entry point
├── LoadData_MultiChip.py                 # Image dataset loaders
├── Load_PhysioNet_EEG.py                 # EEG data loader (MNE-based)
├── challenge_dataloaders.py              # Challenge 1 & 2 loaders
├── logger.py                             # Training metrics logger
├── utils.py                              # Learning rate schedulers
├── DependencyCheck.py                    # Dependency version checker
├── checkpoints/                          # Model checkpoints (.pt files)
├── data/                                 # Image datasets
├── ABCD/                                 # fMRI data (~9400 subjects)
├── EEGChallenge/                         # Challenge datasets
└── *.sh                                  # SLURM batch scripts (86 total)
```

**Important**: Ignore `conda-cache/` and `conda-envs/` directories for code analysis.

## Hyperparameter Tuning Guidelines

**Common Hyperparameter Ranges:**
- Qubits: 4, 6, 8, 12 (typical); 16+ (advanced)
- Circuit depth: 1-4 layers
- Batch size: 16, 32, 64, 128
- Learning rate: 1e-4, 1e-3, 1e-2
- Epochs: 50, 100, 200
- Seed: 2024, 2025 (for reproducibility)

**Multi-Chip Experiments:**
- Small scale: 1, 2, 3, 4, 6 chips
- Large ensemble: 272 chips

## Checkpoint Management

**Checkpoint Naming Convention:**
```
<model>_seed<seed>_chips<n>.pt
checkpoint_challenge_<challenge_num>_<job_id>.pt
```

**Resume Training:**
- Checkpoints saved per epoch in `--base-path` directory
- Contains: model state, optimizer state, epoch number, best metrics
- Use `--resume` flag with matching `--job-id` to continue training

## Logging and Metrics

**Training Logger (`logger.py`):**
- Per-epoch CSV logging
- Metrics tracked:
  - Classification: Accuracy, ROC-AUC, Loss
  - Regression: RMSE, MSE, MAE
  - Quantum: Density matrix properties, circuit depth

**Wandb Integration:**
- Entity: `QML_EEGChallenge`
- Project: `eeg-challenge_200`
- Tracks: hyperparameters, loss curves, validation metrics
- Requires `--wandb` flag

## Code Conventions

**Device Management:**
```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```
All models explicitly handle CPU/GPU placement.

**Reproducibility:**
```python
def set_all_seeds(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ["PL_GLOBAL_SEED"] = str(seed)
    qml.numpy.random.seed(seed)
```
Always use fixed seeds (2024, 2025) for reproducible experiments.

**Quantum Circuit Configuration:**
- Use `ast.literal_eval()` to parse circuit config strings from CLI
- Example: `--sim14-circuit-config="['RY', 'CRX', 'RY', 'CRX_counter']"`

## Important Data Paths

**Server Data Directory:**
```python
SERVER_DATA_DIR = Path("/global/cfs/cdirs/m4750/ty/neurips_hbn")
```
Used for EEG Challenge datasets.

**Checkpoint Base Path:**
```python
--base-path=./checkpoints  # Default
--base-path=/path/to/custom/checkpoints  # Custom
```

## Quantum Circuit Visualization

Draw and save quantum circuit diagrams:
```python
from QuixerTSModel_Pennylane2 import draw_and_save_circuit
draw_and_save_circuit(model, save_path="circuit_diagram.png")
```

## Research Focus Areas

1. **Quantum Advantage**: Testing quantum circuits vs. classical baselines
2. **Noise Resilience**: Investigating quantum error mitigation (ZNE, noise models)
3. **Biomedical Applications**: Real-world EEG/fMRI for clinical relevance
4. **Scalability**: Multi-chip architectures for larger qubit counts

## Best Practices

1. **Always specify seed** for reproducibility (`--seed=2024` or `--seed=2025`)
2. **Use mini datasets first** (`--mini`) to verify code before full runs
3. **Enable checkpointing** (`--resume`, `--job-id`) for long experiments
4. **Track with Wandb** (`--wandb`) for experiment monitoring
5. **Test on CPU** before submitting GPU jobs (comment out `device = "cpu"` line)
6. **Check dependencies** with `DependencyCheck.py` before running on new environments
7. **Unique job IDs** prevent checkpoint collisions when running parallel experiments

## Troubleshooting

**CUDA Out of Memory:**
```bash
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256
```
Uncomment this line in SLURM scripts if encountering GPU memory issues.

**Missing Packages:**
Run dependency checker and install missing packages:
```bash
python DependencyCheck.py --filename=<script>.py
# Review generated requirements.txt
pip install -r requirements.txt
```

**Checkpoint Loading Errors:**
Ensure `--job-id` matches the checkpoint filename and paths are correct.
