## 프로젝트 소개

**인공지능 모델을 활용해, 사용자가 입력한 이미지에 어울리는 배경음악을 생성해줍니다.**

- 끊기지 않는 배경 음악
- 저작권 없는 배경 음악
- 자체 서버에 모델을 띄워 사용

### 김동하

한양대학교 컴퓨터소프트웨어학부 20학번

> 🗨️ 파이팅!
> 

### 한채연

숙명여자대학교 IT공학부 20학번

> 🗨️ 전공자답게 열심히 할게요!
> 

<aside>
🔧 사용한 도구

- Docker 🐋
- React 🌐
- huggingface 🤗
- Python 🧑‍💻
- FastAPI 💨
</aside>

## 주요 기능 소개

![Untitled](https://github.com/madcamp12/week3-InstantMusical/assets/71596178/cd32ccb5-8bb5-4191-adc7-d0dbdff93a22)

> 🖼️ 저희가 구현한 모델 pipeline은 위 사진과 같습니다.
> 
> - User Image를 분석
> - 중간 매개체(TEXT) 생성
> - TEXT를 바탕으로 음악 생성

**1️⃣ Image to Text**

[nlpconnect/vit-gpt2-image-captioning · Hugging Face](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning)

- 중간 매개체를 생성해주는 모델로 image captioning 모델을 사용했습니다.
- 자체적으로 성능을 확인하고 파인 튜닝 없이 사용했습니다.
    - 이미지를 설명하는 Text를 잘 만들어냈습니다.
    

**2️⃣ Text to Audio**

[AudioCraft](https://audiocraft.metademolab.com/musicgen.html)

**MusicGen**

- 중간 매개체(Text)를 기반으로, 음악을 생성하는 모델입니다.
- 앞선 모델이 만들어낸 Text를 이용해 **파인 튜닝**을 진행했습니다.
    - 풍경 사진들에 대해 Text를 만들어내고, 예시 음악들을 준비해 진행했습니다.

**3️⃣ 구현 방식**

- **음악 생성 방식**
    1. 웹 페이지에서 서버에 소켓을 연결해 이미지 데이터를 전송합니다.
    2. 서버에서는 이미지 데이터를 읽고, image captioning 모델을 통해 분석 text를 생성합니다.
    3. 생성된 text와 MusicGen 모델을 이용해 오디오 파일을 생성합니다.

- **끊기지 않는 음악을 위해서**
    
    *MusicGen 모델은 최대 30초의 오디오를 생성할 수 있습니다.*
    
    1. 프론트엔드에서 오디오 파일을 실행할 때, 서버에 어떤 파일을 듣고 있는지 전송합니다.
    2. 서버 측에서는 해당 정보를 바탕으로, 이어지는 오디오 파일을 추가적으로 생성합니다.
    3. 오디오 파일을 모두 재생하게 되면, 미리 만들어 둔 다음 파일을 이용해 노래가 끊기지 않게 연결합니다.

- **저장 공간 유지를 위해서**
    
    *제공 받은 서버는 350GB의 디스크 용량을 가지고 있습니다.*
    
    - 소켓 연결이 끊어지면, 서버는 해당 소켓에 해당되는 오디오 파일을 모두 삭제합니다.
        
        ⇒ 소켓 연결을 활용한 이유
        

**4️⃣ 예시**

![Untitled (1)](https://github.com/madcamp12/week3-InstantMusical/assets/71596178/1785b1c3-5299-4fd4-9263-a77c3e672ace)

- 이미지를 입력하고, `Create` 버튼을 클릭하면 이미지를 분석하고 음악을 생성하기 시작합니다.
- 음악 생성이 완료되면, 재생 버튼이 활성화됩니다.
- 재생/일시 정지 버튼을 통해 노래를 멈추고 재생할 수 있습니다.

