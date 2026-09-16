import torch
from langchain_core.tools import tool


# ==========================================
# MODEL
# ==========================================

class DroneRiskModel(torch.nn.Module):

    def __init__(self):
        super().__init__()

        self.network = torch.nn.Sequential(
            torch.nn.Linear(3, 16),
            torch.nn.ReLU(),

            torch.nn.Linear(16, 8),
            torch.nn.ReLU(),

            torch.nn.Linear(8, 1),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)


# ==========================================
# LOAD MODEL
# ==========================================

model = DroneRiskModel()

model.load_state_dict(
    torch.load(
        "ml/drone_risk_model.pth",
        weights_only=True
    )
)

model.eval()


# ==========================================
# LOAD NORMALIZATION VALUES
# ==========================================

stats = torch.load(
    "ml/drone_risk_stats.pth",
    weights_only=True
)

mean = stats["mean"]
std = stats["std"]


# ==========================================
# ML TOOL
# ==========================================

@tool
def predict_drone_risk(
    battery: float,
    temperature: float,
    signal_strength: float
) -> str:
    """
    Predict drone operational risk.

    battery:
    Drone battery percentage.

    temperature:
    Drone temperature in Celsius.

    signal_strength:
    Communication signal strength percentage.
    """

    input_data = torch.tensor(
        [[
            battery,
            temperature,
            signal_strength
        ]],
        dtype=torch.float32
    )

    # Normalize input
    input_data = (input_data - mean) / std

    # Prediction
    with torch.no_grad():
        prediction = model(input_data)

    risk_score = prediction.item()
    risk_percentage = risk_score * 100

    if risk_score >= 0.5:
        risk_level = "HIGH"
    else:
        risk_level = "LOW"

    return (
        f"Drone Risk: {risk_level}\n"
        f"Risk Score: {risk_percentage:.1f}%"
    )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    result = predict_drone_risk.invoke({
        "battery": 28,
        "temperature": 61,
        "signal_strength": 72
    })

    print(result)