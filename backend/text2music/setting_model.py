import torch, logging
from transformers import AutoProcessor, MusicgenForConditionalGeneration

InputProcessor = None
MusicGenModel = None
MyDevice = torch.device("cuda" if torch.cuda.is_available() else "cpu")

## model을 만드는 과정 : 이 과정을 초반에 진행해서 미리 모델을 띄워놓으면 됩니다 ##
def model_init():
    global InputProcessor, MusicGenModel
    
    InputProcessor = AutoProcessor.from_pretrained("facebook/musicgen-stereo-small")
    MusicGenModel = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-stereo-small")
    MusicGenModel.load_state_dict(torch.load('fine_tuned_model_30_4_5.pth'))
    MusicGenModel.to(MyDevice)

## model을 없애는 과정 : 할당한 InputProcessor, MusicGenModel을 없애줍니다 ##
def model_destory():
    global MusicGenModel, InputProcessor
    
    InputProcessor = None
    MusicGenModel = None
    
def get_musicgen():
    global InputProcessor, MusicGenModel, MyDevice
    return InputProcessor, MusicGenModel, MyDevice

def get_sample_rate():
    global MusicGenModel
    return MusicGenModel.config.audio_encoder.sampling_rate