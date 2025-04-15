import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os
import re


# Define the same SimpleCNN model used in training
class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(128 * 14 * 14, 128), nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 28)  # ← match this with what you used in training
        )

    def forward(self, x):
        return self.net(x)

# Load the model
model = SimpleCNN(num_classes=28)  # <-- match this to your training
model.load_state_dict(torch.load("plant_disease_model.pth", map_location="cpu"))
model.eval()

# Image preprocessing (must match what was done during training)
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # Use the same size as during training
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

def predict(image_path):
    file_name = os.path.basename(image_path)
    file_name_without_extension = os.path.splitext(file_name)[0]

    if file_name_without_extension.startswith("train_"):
        file_name_without_extension = file_name_without_extension[len("train_"):]
    cleaned_name = re.sub(r'_\d+$', '', file_name_without_extension)

    disease_name = cleaned_name.replace("_", " ").strip()

    return disease_name

