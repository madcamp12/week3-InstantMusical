import torch
import torchaudio
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import os

processor = AutoProcessor.from_pretrained("facebook/musicgen-stereo-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-stereo-small")
model.to("cuda")

## input, ouput을 정해줘야 함
input_text = ['a stone wall with a view of a mountain range',
              'a river filled with rocks and a waterfall',
              'a picture taken from the top of a hill overlooking a lake',
              'snow covered mountains and trees in the distance',
              'a city street filled with lots of traffic',
              'a view of a lake from a boat in the snow',
              'people on a boat in a body of water',
              'a view through a fence of a forest',
              'a road that has some trees on it',
              'a scenic view of a mountain range with mountains']

mp3_list = [file for file in os.listdir('/workspace/music')]

output_label = [] ## 요거 쓸거임
for file_name in mp3_list:
    path = os.path.join('/workspace/music', file_name)
    
    wavform, _ = torchaudio.load(path, normalize=True)
    wavform = wavform[:, :960000]
    wavform = torch.Tensor(wavform)
    wavform.requires_grad = True
    
    output_label.append(wavform)



loss_func = torch.nn.MSELoss().to("cuda")
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

model.train()

for epoch in range(5):
    print(f'epoch: {epoch + 1} / 5 . . .')
    print('-' * 30)
    
    for i in range(10):
        if(i == 5):
            torch.save(model.state_dict(), f'fine_tuned_model_30_{epoch + 1}_{i}.pth')
        
        print(f'training . . . :: {i + 1} / 10 . . .')
        optimizer.zero_grad()
        
        inputs = processor(
            text = ['10s classic track feels like' + 'TODO'],
            padding = True,
            return_tensors='pt'
        ).to("cuda")
        
        music = model.generate(**inputs, max_new_tokens=1503)
        output = music[0]
        
        loss = loss_func(output, output_label[i].to("cuda"))
        loss.backward()
        optimizer.step()
        
torch.save(model.state_dict(), 'fine_tuned_model_30_origin.pth')
    
    