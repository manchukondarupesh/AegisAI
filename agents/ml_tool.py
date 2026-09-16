import torch
import json
from langchain_core.tools import tool


# ==========================================
# MODEL
# ==========================================

class DeliveryPredictor(torch.nn.Module):

    def __init__(self):

        super().__init__()

        self.network = torch.nn.Sequential(
            torch.nn.Linear(4, 32),
            torch.nn.ReLU(),

            torch.nn.Linear(32, 16),
            torch.nn.ReLU(),

            torch.nn.Linear(16, 1)
        )

    def forward(self, x):

        return self.network(x)


# ==========================================
# LOAD MODEL
# ==========================================

model = DeliveryPredictor()

model.load_state_dict(
    torch.load(
        "ml/food_delivery_model.pth",
        weights_only=True
    )
)

model.eval()


# ==========================================
# LOAD NORMALIZATION VALUES
# ==========================================

with open("ml/model_stats.json", "r") as file:

    stats = json.load(file)


mean = torch.tensor(stats["mean"])

std = torch.tensor(stats["std"])


# ==========================================
# ML TOOL
# ==========================================

@tool
def predict_delivery_time(
    distance: float,
    items: int,
    preparation_time: float,
    traffic: int
) -> str:
    """
    Predict food delivery time using a PyTorch model.

    traffic:
    1 = Low
    2 = Medium
    3 = High
    """

    input_data = torch.tensor(
        [
            [
                distance,
                items,
                preparation_time,
                traffic
            ]
        ],
        dtype=torch.float32
    )

    # Normalize
    input_data = (
        input_data - mean
    ) / std

    # Prediction
    with torch.no_grad():

        prediction = model(
            input_data
        )

    minutes = prediction.item()

    return (
        f"Predicted food delivery time: "
        f"{minutes:.1f} minutes"
    )