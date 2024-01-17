#### FastAPI를 활용한 웹 소켓 구성 ####
## 웹 소켓을 통해 이미지 파일을 전달하면
## 배경음악을 계속해서 만들면서 소켓을 통해 전달해줍니다

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import soundfile as sf
from PIL import Image
from io import BytesIO
import os, logging
import img2text, text2music
import base64
import numpy as np
import asyncio

img2text.model_init()
text2music.model_init()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path("wavs")), name="static")

sampling_rate = text2music.get_sample_rate()
start_frame1 = int(5 * sampling_rate)
end_frame1 = int(25 * sampling_rate)
start_frame2= int(20 * sampling_rate)
end_frame2 = int(25 * sampling_rate)

async def get_websocket_tag():
    import uuid
    return str(uuid.uuid4())

async def delete_file(tag):
    try:
        import os
        os.remove(tag)
    except Exception as e:
        pass
     
async def handle_zero_case(websocket: WebSocket, description: str, initial_audio_file: str):
    next_audio = text2music.make_music_from_music(initial_audio_file + "00.wav", description)  # musicfile, inputText
    next_audio = next_audio.cpu().numpy()

    # 새로 생성된 오디오 트랙 잘라내고
    
    # 덮어씌우기
    await delete_file(initial_audio_file + "1.wav")
    sf.write(initial_audio_file + "1.wav", next_audio[0].T[start_frame1:end_frame1], sampling_rate)
    
    
    await delete_file(initial_audio_file + "11.wav")
    sf.write(initial_audio_file + "11.wav", next_audio[0].T[start_frame2:end_frame2], sampling_rate)

    
async def handle_one_case(websocket: WebSocket, description: str, initial_audio_file: str):
    next_audio = text2music.make_music_from_music(initial_audio_file + "11.wav", description)
    next_audio = next_audio.cpu().numpy()
    
    await delete_file(initial_audio_file + "0.wav")
    sf.write(initial_audio_file + "0.wav", next_audio[0].T[start_frame1:end_frame1], sampling_rate)
    
    
    await delete_file(initial_audio_file + "00.wav")
    sf.write(initial_audio_file + "00.wav", next_audio[0].T[start_frame2:end_frame2], sampling_rate)
    
async def handle_image(websocket: WebSocket, description: str, initial_audio_file: str):     
    audio_track = text2music.make_music_from_text(description)
    audio_sample = audio_track.cpu().numpy()
    sampling_rate = text2music.get_sample_rate()
    
    # 처음에 하나 또 만들어야함
    start_frame = int(15 * sampling_rate)
    end_frame = int(20 * sampling_rate)
    
    sf.write(initial_audio_file + "0.wav", audio_sample[0].T, sampling_rate)
    sf.write(initial_audio_file + "00.wav", audio_sample[0].T[start_frame:end_frame], sampling_rate)
    

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, background: BackgroundTasks):
    await websocket.accept()
    tag = await get_websocket_tag()
    
    initial_audio_file = f"/workspace/wavs/{tag}"
    description = ""
    
    try:
        while True:
            # 바이너리 데이터 수신
            data = await websocket.receive_text()
            data_list = data.split("\n")

            if data_list[0] == "Image":
                image_stream = BytesIO(base64.b64decode(data_list[1]))
                image = Image.open(image_stream)
                description = img2text.make_text_from_image(image)
                logger.info(description)
                
                await handle_image(websocket, description, initial_audio_file)
                await websocket.send_text(tag)
            elif data_list[0] == "0":
                await handle_zero_case(websocket, description, initial_audio_file)
            elif data_list[0] == "1":
                await handle_one_case(websocket, description, initial_audio_file)
        
    except WebSocketDisconnect:
        # 0이랑 1 모두 삭제
        await delete_file(initial_audio_file + "1.wav")
        await delete_file(initial_audio_file + "0.wav")
        await delete_file(initial_audio_file + "00.wav")
        await delete_file(initial_audio_file + "11.wav")