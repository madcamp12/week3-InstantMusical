import torch
from PIL import Image
from .setting_model import get_img2txt

## some setting for inference values ##
max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def make_text_from_image(image: Image.Image):
  
  ## get model from setting_model.py ##
  model, feature_extractor, tokenizer = get_img2txt()
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  
  ## get image from path ##
  if(image.mode != 'RGB'):
    image = image.convert(mode='RGB') ## we need just one image

  ## get picxel values from images ##
  pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(device) # to device (GPU or CPU)

  ## get output from model ##
  output_ids = model.generate(pixel_values, **gen_kwargs)

  ## match to text with tokenizer ##
  ret = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
  ret = ret[0].strip() # return justo one sentence
  
  return ret