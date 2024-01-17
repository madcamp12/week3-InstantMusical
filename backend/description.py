from PIL import Image
import os, logging
import img2text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

img2text.model_init()

image_extensions = [".jpeg", ".jpg"]
image_paths = []
for file in os.listdir('images'):
    if any(file.endswith(ext) for ext in image_extensions):
        image_paths.append(os.path.join('images', file))

# print(image_paths)

for image_path in image_paths:
    # 경로상에 있는 이미지 가져와서 모델에 넣고, description 저장
    with Image.open(image_path) as image:
        print(img2text.make_text_from_image(image))