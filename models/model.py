import torch
import torchvision.models as models

def load_model(model_path):
    """
    Load the pre-trained ResNet model for leaf disease detection.
    """
    model = models.resnet18(pretrained=False)  # Ensure correct architecture
    num_ftrs = model.fc.in_features
    
    # 🔹 Update this to 13 (since your trained model expects 13 classes)
    model.fc = torch.nn.Linear(num_ftrs, 13)  # Change 13 to match your trained model

    # Load model weights
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()  # Set model to evaluation mode
    return model
