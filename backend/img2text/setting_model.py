from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch

Img2TxtModel = None
FeatureExtractor = None
Img2TxtTokenizer = None

# 모델 로드
def model_init():
    global Img2TxtModel, FeatureExtractor, Img2TxtTokenizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    Img2TxtModel = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning").to(device)
    FeatureExtractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    Img2TxtTokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    
def get_img2txt():
    global Img2TxtModel, FeatureExtractor, Img2TxtTokenizer
    
    return Img2TxtModel, FeatureExtractor, Img2TxtTokenizer
