import io, logging
import torchaudio
from .setting_model import get_musicgen

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

## InputText를 반영해 20초 만큼의 클래식 음악 트랙을 만드는 과정
def make_music_from_text(inputText):
    processor, model, device = get_musicgen()
    
    inputs = processor(
        text=["Happy classic " + inputText],
        padding = True,
        return_tensors="pt"
    ).to(device)
    
    ## 20초 분량의 음악을 만들어 냄
    audio_track = model.generate(**inputs, max_new_tokens=1024)
    return audio_track
    
    
## music file을 반영해 다른 음악을 만들어주는 과정
def make_music_from_music(musicFile, inputText):
    processor, model, device = get_musicgen()
    audio_value = torchaudio.load(musicFile)[0]
    
    inputs = processor(
        audio=audio_value, # 기존 음악을 prompt로 입력
        text = ["Happy classic " + inputText],
        padding = True,
        return_tensors="pt"
    ).to(device)
    
    ## 20초 분량의 음악을 만들어 냄
    audio_track = model.generate(**inputs, guidance_scale = 3, max_new_tokens=1024)
    
    return audio_track