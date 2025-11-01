"""
Submission file for EEG Challenge 2025 - Ensemble K-Fold Models
"""
import torch
from pathlib import Path

def resolve_path(name="python_packages"):
    if Path(f"/app/input/res/{name}").exists():
        return f"/app/input/res/{name}"
    elif Path(f"/app/input/{name}").exists():
        return f"/app/input/{name}"
    elif Path(f"{name}").exists():
        return f"{name}"
    elif Path(__file__).parent.joinpath(f"{name}").exists():
        return str(Path(__file__).parent.joinpath(f"{name}"))
    else:
        raise FileNotFoundError(
            f"Could not find {name} folder in /app/input/res/ or /app/input/ or current directory"
        )


class EnsembleQuixerModel(torch.nn.Module):
    """Ensemble model for k-fold predictions."""

    def __init__(self, packaged_weights, n_qubits, n_layers, degree,
                 feature_projection_layer, sim14_circuit_config, output_ff_layer,
                 n_timesteps=200, feature_dim=129, output_dim=1, dropout=0.1,
                 device='cuda'):
        super().__init__()
        import sys
        sys.path.append(resolve_path())
        from QuixerTSModel_Pennylane2 import QuixerTimeSeriesPennyLane
        self.n_folds = packaged_weights['n_folds']
        fold_weights_dict = packaged_weights['fold_weights']

        # Create k models and load their weights
        self.fold_models = torch.nn.ModuleList()
        for fold_id in range(self.n_folds):
            model = QuixerTimeSeriesPennyLane(
                n_qubits=n_qubits,
                n_timesteps=n_timesteps,
                degree=degree,
                n_ansatz_layers=n_layers,
                feature_dim=feature_dim,
                output_dim=output_dim,
                dropout=dropout,
                feature_projection_layer=feature_projection_layer,
                sim14_circuit_config=sim14_circuit_config,
                output_ff_layer=output_ff_layer,
                device=device
            )
            model.load_state_dict(fold_weights_dict[f'fold_{fold_id}'])
            self.fold_models.append(model)
            self.fold_models.to(device).float()

    def forward(self, x):
        """Average predictions across all folds."""
        predictions = []

        with torch.no_grad():
            for model in self.fold_models:
                pred = model(x)
                predictions.append(pred)

        return torch.mean(torch.stack(predictions, dim=0), dim=0)


class Submission:
    """
    Official submission class for EEG Challenge 2025.
    Must implement get_model_challenge_1() and get_model_challenge_2().
    """

    def __init__(self, SFREQ, DEVICE):
        self.sfreq = SFREQ    # 100 Hz
        self.device = DEVICE  # 'cuda' or 'cpu'

        # Model hyperparameters (MUST MATCH YOUR TRAINING CONFIG!)
        self.config_1 = {
            'n_qubits': 6,
            'n_layers': 2,
            'degree': 2,
            'dropout': 0.1,
            'feature_projection_layer': 'Conv2d_GLU',
            'sim14_circuit_config': ['RX','CRY','RX','CRY_counter'],
            'output_ff_layer': 'GLU',
            'n_timesteps': 200,  # 200 samples at 100 Hz
            'feature_dim': 129,  # 129 EEG channels
            'output_dim': 1
        }
        self.config_2 = {
            'n_qubits': 6,
            'n_layers': 2,
            'degree': 3,
            'dropout': 0.1,
            'feature_projection_layer': 'Conv2d_GLU',
            'sim14_circuit_config': ['RX','CRY','RX','CRY_counter'],
            'output_ff_layer': 'GLU',
            'n_timesteps': 200,  # 200 samples at 100 Hz
            'feature_dim': 129,  # 129 EEG channels
            'output_dim': 1
        }        

    
    def get_model_challenge_1(self):
        """
        Return ensemble model for Challenge 1 (Response Time Prediction).
        """
        # Load packaged ensemble weights
        model_path = Path(__file__).parent / "weights_challenge_1_kfold_B1_mini.pt"
        print("Loading weights for Challenge 1 model.")
        packaged_weights = torch.load(model_path, map_location=self.device, weights_only=True)

        # Create ensemble model
        model = EnsembleQuixerModel(
            packaged_weights=packaged_weights,
            n_qubits=self.config_1['n_qubits'],
            n_layers=self.config_1['n_layers'],
            degree=self.config_1['degree'],
            dropout=self.config_1['dropout'],
            feature_projection_layer=self.config_1['feature_projection_layer'],
            sim14_circuit_config=self.config_1['sim14_circuit_config'],
            output_ff_layer=self.config_1['output_ff_layer'],
            n_timesteps=self.config_1['n_timesteps'],
            feature_dim=self.config_1['feature_dim'],
            output_dim=self.config_1['output_dim'],
            device=self.device
        )

        return model.to(self.device)

    def get_model_challenge_2(self):
        """
        Return ensemble model for Challenge 2 (Externalizing Factor Prediction).
        """
        # Load packaged ensemble weights       
        model_path = Path(__file__).parent / "weights_challenge_2_kfold_B2_mini.pt"
        print("Loading weights for Challenge 2 model.")
        packaged_weights = torch.load(model_path, map_location=self.device, weights_only=True)
            
        # Create ensemble model
        model = EnsembleQuixerModel(
            packaged_weights=packaged_weights,
            n_qubits=self.config_2['n_qubits'],
            n_layers=self.config_2['n_layers'],
            degree=self.config_2['degree'],
            dropout=self.config_2['dropout'],
            feature_projection_layer=self.config_2['feature_projection_layer'],
            sim14_circuit_config=self.config_2['sim14_circuit_config'],
            output_ff_layer=self.config_2['output_ff_layer'],
            n_timesteps=self.config_2['n_timesteps'],
            feature_dim=self.config_2['feature_dim'],
            output_dim=self.config_2['output_dim'],
            device=self.device
        )

        return model.to(self.device)
