"""Align captions to actual synthesized phrase WAV files and join the narration."""
import json, pathlib, re, wave
ROOT=pathlib.Path(__file__).parent.resolve()
board=json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
output=ROOT/'output'; output.mkdir(exist_ok=True)
current=0.; captions=[]; scenes=[]; samples=[]; rate=None
for scene in board['scenes']:
 scene=dict(scene,start=current)
 for index,phrase in enumerate(re.findall(r'[^。！？]+[。！？]?',scene['narration'])):
  with wave.open(str(output/'audio'/f'{scene["id"]}-{index:02}.wav'),'rb') as stream:
   if stream.getnchannels()!=1 or stream.getsampwidth()!=2: raise ValueError('Expected mono PCM16')
   if rate is None: rate=stream.getframerate()
   if stream.getframerate()!=rate: raise ValueError('Mixed sample rates')
   frames=stream.readframes(stream.getnframes());duration=stream.getnframes()/rate
  elapsed=0.
  parts=[]; part=''
  for token in re.findall(r'[A-Za-z][A-Za-z0-9 ./-]*|.',phrase):
   if part and len(part)+len(token)>25:
    parts.append(part);part=''
   part+=token
  if part: parts.append(part)
  for part in parts:
   length=duration*len(part)/len(phrase)
   captions.append({'start':current+elapsed,'end':current+elapsed+length,'text':part});elapsed+=length
  samples.append(frames);current+=duration
 samples.append(b'\0'*(round(rate*.6)*2));current+=.6
 scene['end']=current;scenes.append(scene)
with wave.open(str(output/'narration.wav'),'wb') as stream:
 stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(rate);stream.writeframes(b''.join(samples))
timeline=dict(board,scenes=scenes,captions=captions,duration=current)
(output/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
def srt_time(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
(output/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt_time(c["start"])} --> {srt_time(c["end"])}\n{c["text"]}' for i,c in enumerate(captions))+'\n',encoding='utf-8')
print(json.dumps({'duration':current,'scenes':len(scenes),'captions':len(captions),'sample_rate':rate}))
