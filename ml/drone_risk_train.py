import torch
import torch.nn as nn
import torch.optim as optim


# ==========================================
# DRONE RISK DATA
# ==========================================

# Features:
# battery, temperature, signal_strength

X = torch.tensor([
    [90, 40, 95],
    [85, 42, 92],
    [75, 45, 88],
    [65, 48, 85],
    [55, 50, 80],
    [45, 53, 75],
    [35, 57, 70],
    [28, 61, 72],
    [20, 65, 60],
    [15, 68, 50]
], dtype=torch.float32)


# Normalize the input features
mean = X.mean(dim=0)
std = X.std(dim=0)

X_normalized = (X - mean) / std


# 0 = Low Risk
# 1 = High Risk

y = torch.tensor([
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [1],
    [1],
    [1],
    [1]
], dtype=torch.float32)


# ==========================================
# MODEL
# ==========================================

class DroneRiskModel(nn.Module):

    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),

            nn.Linear(16, 8),
            nn.ReLU(),

            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)


# ==========================================
# TRAIN
# ==========================================

model = DroneRiskModel()

criterion = nn.BCELoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.01
)


for epoch in range(2000):

    prediction = model(X_normalized)

    loss = criterion(prediction, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


# ==========================================
# SAVE MODEL
# ==========================================

torch.save(
    model.state_dict(),
    "ml/drone_risk_model.pth"
)

torch.save(
    {
        "mean": mean,
        "std": std
    },
    "ml/drone_risk_stats.pth"
)


print("Drone risk model trained successfully.")
print("Model saved to: ml/drone_risk_model.pth")
print("Normalization values saved to: ml/drone_risk_stats.pth")