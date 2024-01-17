import React, { useEffect, useRef, useState } from 'react';
import ReactDOM from 'react-dom/client';
import Title from './components/title/Title';
import { ImageForm, get_image_file } from './components/imageform/ImageForm';
import Button from './components/button/Button';
import Spinner from 'react-bootstrap/Spinner';

let filename = null;
let currIdx = 0;
let isLoaded = false;
const PlayPNG = require('./components/play/play.png');
const PuasePNG = require('./components/play/pause.png');

function App() {
  const [isMobile, setIsMobile] = useState(false); // 모바일인지, 컴퓨터인지 확인하는 변수
  const socketRef = useRef(null);
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [flag, setFlag] = useState(false);
  const [flag2, setFlag2] = useState(false);

  useEffect(() => {
    // isMobile을 설정하는 함수
    const handleResize = () => {
      const screenWidth = window.innerWidth;
      const isMobileDevice = screenWidth <= 768; // 768픽셀을 기준으로

      setIsMobile(isMobileDevice);
    }
    
    handleResize(); // 초기 설정

    // listener 등록: 화면 크기가 바뀔 때마다 handleResize 호출
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };

  }, []);

  // 기본 body의 스타일 적용: desktop과 mobile을 구분해서
  const rootStyle = () => {
    const ret = {
      "width": isMobile ? '100%' : '70vw',
      "margin": isMobile ? '' : 'auto',
    };

    return ret;
  }

  // 버튼을 누르면 소켓을 연결하고, 이미지 데이터를 base64로 인코딩해 넘겨줍니다
  const handleCreateButton = () => {
    if(get_image_file() == null){
      alert('이미지를 넣어주세요!');
      return;
    }

    // 이미 소켓이 있으면 끊기
    if(socketRef.current != null){
      socketRef.current.close();
      filename = null;
      setFlag(true);
      setFlag2(false);
      isLoaded = false;
    }
    
    // 소켓 연결
    const socket = new WebSocket("ws://localhost:8000/ws");
    socketRef.current = socket;

    // 리스너 등록
    socket.onmessage = (event) => {
      filename = event.data;
      setFlag2(true);
    }

    // 소켓이 연결되면
    socket.onopen = (event) => {
      const img = get_image_file().split(',')[1];
      const message = "Image\n" + img;
      socketRef.current.send(message);

      setFlag(true);
    }

    window.addEventListener('beforeunload', () => {socketRef.current.close();})
  }

  // 재생 버튼을 눌렀을 때 동작 정의
  const handlePlayButton = () => {
    if(isPlaying){
      const audio = audioRef.current;
      audio.pause();
      setIsPlaying(false);
      return;
    }
    if(!isPlaying && isLoaded){
      const audio = audioRef.current;
      audio.play();
      setIsPlaying(true);
      return;
    }
    
    const audio = audioRef.current;
    audio.src = "http://localhost:9000/static/" + filename + "0.wav";
    
    audio.addEventListener('ended', () => {
      const audio = audioRef.current;
      const socket = socketRef.current;

      if(currIdx == 0){
        audio.src = "http://localhost:9000/static/" + filename + "1.wav";
        audio.play();

        socket.send("1\n");
        currIdx = 1;
      }else if(currIdx == 1){
        audio.src = "http://localhost:9000/static/" + filename + "0.wav";
        audio.play();

        socket.send("0\n");
        currIdx = 0;
      }
    })

    window.addEventListener('beforeunload', () => {
      socketRef.current.close();
    });

    audio.play();
    setIsPlaying(true);
    socketRef.current.send("0\n");
    isLoaded = true;
  }

  // 메인 화면 표현
  return (
    <div style={rootStyle()}>
      <div style={{marginTop: '10vh'}}>
        <Title/>
      </div>

      <ImageForm/>
      <Button onclick = {handleCreateButton}/>
      
      {flag && !flag2 && (
        <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center'}}>
          <Spinner animation="border" variant="primary"/>
          <span>Creating background music ...</span>
        </div>
      )}

      {flag && flag2 && (

        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
          <img src={isPlaying ? PuasePNG : PlayPNG} style={{width: '100px', height: '100px', cursor: 'pointer'}} onClick={handlePlayButton}/>
          <audio style={{visibility: 'hidden'}} ref={audioRef}></audio>
        </div>
      )}

    </div>
  );
}

export default App;
