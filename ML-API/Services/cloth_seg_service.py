# services/detection.py

import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from collections import OrderedDict
from io import BytesIO
from utils.network import U2NET

model = U2NET(in_ch=3, out_ch=4)
state_dict = torch.load(".\models\cloth_segm.pth", map_location="cpu")
clean_state_dict = OrderedDict((k.replace("module.", ""), v) for k, v in state_dict.items())
model.load_state_dict(clean_state_dict)
model.eval()

def preprocess_image(uploaded_file):
    image = Image.open(BytesIO(uploaded_file.file.read())).convert("RGB")
    original_size = image.size
    image = image.resize((768, 768), Image.BICUBIC)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])
    tensor = transform(image).unsqueeze(0)
    return tensor, original_size

def predict_mask(image_tensor):
    with torch.no_grad():
        output = model(image_tensor)[0]
        pred = F.softmax(output, dim=1)
        mask = torch.argmax(pred, dim=1).squeeze().cpu().numpy()
    return mask

def mask_to_rgb(mask):
    color_map = {
        0: (0, 0, 0),
        1: (255, 0, 0),
        2: (0, 255, 0),
        3: (255, 255, 0),
    }
    rgb = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    for cls, color in color_map.items():
        rgb[mask == cls] = color
    return Image.fromarray(rgb)
