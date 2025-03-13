from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image

class CLIPModelWrapper:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        """Initialize CLIP model and processor"""
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)
    
    def get_image_embedding(self, image_path):
        """Get dense embeddings for images"""
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            embedding = self.model.get_image_features(**inputs)
        # normalization for faster cosine similarity calculation
        return embedding / embedding.norm(dim=-1)
    
    def get_text_embedding(self, query):
        """Get dense embeddings for text"""
        # Preprocess the text query
        inputs = self.processor(
            text=[query], return_tensors="pt", padding=True, truncation=True
        )
        with torch.no_grad():
            embedding = self.model.get_text_features(**inputs)
        # normalization for faster cosine similarity calculation
        return embedding / embedding.norm(dim=-1) 