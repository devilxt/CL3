import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
import torchvision.transforms as transforms
import torchvision.models as models
from torchvision.utils import save_image
import numpy as np

def load_image(image_path, max_size=400, shape=None):
    """Loads and resizes an image, converting it to a PyTorch tensor."""
    image = Image.open(image_path).convert('RGB')
    
    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)
        
    if shape is not None:
        size = shape
        
    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])
    
    return transform(image)[:3, :, :].unsqueeze(0)

class VGG(nn.Module):
    def __init__(self):
        super(VGG, self).__init__()
        self.chosen_features = ['0', '5', '10', '19', '28']
        self.model = models.vgg19(pretrained=True).features[:29]
        
    def forward(self, x):
        features = []
        for layer_num, layer in enumerate(self.model):
            x = layer(x)
            if str(layer_num) in self.chosen_features:
                features.append(x)
        return features

def calc_gram_matrix(tensor):
    """Calculates the Gram Matrix for style representation."""
    _, d, h, w = tensor.size()
    tensor = tensor.view(d, h * w)
    return torch.mm(tensor, tensor.t())

def run_style_transfer():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running on device: {device}")

    # Load Images
    content_img = load_image("content.jpg").to(device)
    style_img = load_image("style.jpg", shape=[content_img.shape[2], content_img.shape[3]]).to(device)

    # The image we will optimize
    generated_img = content_img.clone().requires_grad_(True)

    # Initialize model
    model = VGG().to(device).eval()
    for param in model.parameters():
        param.requires_grad = False

    # Hyperparameters
    total_steps = 2000
    learning_rate = 0.01
    alpha = 1        # Content weight
    beta = 100000    # Style weight

    optimizer = optim.Adam([generated_img], lr=learning_rate)

    print("Starting optimization...")
    for step in range(total_steps):
        gen_features = model(generated_img)
        content_features = model(content_img)
        style_features = model(style_img)

        style_loss = 0
        content_loss = 0

        for gen_feat, cont_feat, styl_feat in zip(gen_features, content_features, style_features):
            content_loss += torch.mean((gen_feat - cont_feat) ** 2)
            G = calc_gram_matrix(gen_feat)
            A = calc_gram_matrix(styl_feat)
            style_loss += torch.mean((G - A) ** 2)

        total_loss = alpha * content_loss + beta * style_loss

        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        if step % 200 == 0:
            print(f"Step [{step}/{total_steps}] | Total Loss: {total_loss.item():.4f}")
            save_image(generated_img, f"generated_step_{step}.png")

    save_image(generated_img, "final_artistic_image.png")
    print("Style transfer complete! Image saved.")

if __name__ == "__main__":
    run_style_transfer()