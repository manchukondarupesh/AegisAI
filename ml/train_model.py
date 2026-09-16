import torch
import torch.nn as nn
import pandas as pd
import random
import json


# ==========================================
# 1. CREATE FOOD DELIVERY DATASET
# ==========================================

random.seed(42)

data = []

for i in range(500):

    distance = random.uniform(1, 15)
    items = random.randint(1, 8)
    preparation_time = random.uniform(5, 30)
    traffic = random.randint(1, 3)

    # Synthetic delivery-time formula
    delivery_time = (
        8
        + distance * 2.5
        + items * 1.2
        + preparation_time * 0.8
        + traffic * 5
        + random.uniform(-2, 2)
    )

    data.append([
        distance,
        items,
        preparation_time,
        traffic,
        delivery_time
    ])


df = pd.DataFrame(
    data,
    columns=[
        "distance",
        "items",
        "preparation_time",
        "traffic",
        "delivery_time"
    ]
)

print("Dataset created.")
print(df.head())


# ==========================================
# 2. PREPARE DATA
# ==========================================

X = df[
    [
        "distance",
        "items",
        "preparation_time",
        "traffic"
    ]
].values

y = df["delivery_time"].values


# Convert to PyTorch tensors
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)


# ==========================================
# 3. NORMALIZE INPUT
# ==========================================

X_mean = X.mean(dim=0)
X_std = X.std(dim=0)

X_normalized = (X - X_mean) / X_std


# ==========================================
# 4. CREATE NEURAL NETWORK
# ==========================================

class DeliveryPredictor(nn.Module):

    def __init__(self):

        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(4, 32),
            nn.ReLU(),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 1)
        )

    def forward(self, x):

        return self.network(x)


model = DeliveryPredictor()


# ==========================================
# 5. LOSS AND OPTIMIZER
# ==========================================

criterion = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)


# ==========================================
# 6. TRAIN MODEL
# ==========================================

print("\nTraining PyTorch model...\n")

for epoch in range(1000):

    predictions = model(X_normalized)

    loss = criterion(
        predictions,
        y
    )

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if (epoch + 1) % 100 == 0:

        print(
            f"Epoch {epoch + 1}/1000 "
            f"Loss: {loss.item():.4f}"
        )


# ==========================================
# 7. SAVE MODEL
# ==========================================

torch.save(
    model.state_dict(),
    "ml/food_delivery_model.pth"
)


# ==========================================
# 8. SAVE NORMALIZATION VALUES
# ==========================================

stats = {
    "mean": X_mean.tolist(),
    "std": X_std.tolist()
}

with open(
    "ml/model_stats.json",
    "w"
) as file:

    json.dump(stats, file)


print("\nModel saved successfully!")
print("File: ml/food_delivery_model.pth")
print("Statistics saved: ml/model_stats.json")