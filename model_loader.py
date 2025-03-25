import torch
import torchvision.models as models

def load_model():
    # Load the ResNet model architecture
    model = models.resnet18(weights=None)  # Updated to avoid deprecated warning

    # Get the number of input features for the final layer
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 13)  # Match the number of classes (13)

    # Load the trained model weights
    model.load_state_dict(torch.load("models/resnet_leaf_disease.pth", map_location=torch.device('cpu')))
    
    # Set model to evaluation mode
    model.eval()
    return model

# Quick test to ensure the model loads correctly
if __name__ == "__main__":
    model = load_model()
    print("✅ Model loaded successfully!")
