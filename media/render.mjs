import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
const root=path.dirname(fileURLToPath(import.meta.url));
const board=JSON.parse(fs.readFileSync(path.join(root,'output/timeline.json'),'utf8'));
const out=path.join(root,'output/gamecraft-intro.mp4');
const preview=process.argv.includes('--preview');
if(!preview&&fs.existsSync(out))throw new Error('Output exists; choose or archive the existing output before rendering.');
const modulePath=process.env.PLAYWRIGHT_MODULE;
const {chromium}=await import(modulePath?pathToFileURL(modulePath).href:'playwright');
const browserPath=process.env.CHROME_PATH;
const browser=await chromium.launch({headless:true,...(browserPath?{executablePath:browserPath}:{}),args:['--allow-file-access-from-files']});
const page=await browser.newPage({viewport:{width:board.width,height:board.height},deviceScaleFactor:1});
const pageErrors=[];page.on('pageerror',e=>pageErrors.push(String(e)));
await page.goto(pathToFileURL(path.join(root,'render.html')).href);
await page.evaluate(data=>window.Gamecraft.init(data),board);
const states=[];
try{
 if(preview){
  for(const scene of board.scenes){const t=(scene.start+scene.end)/2;states.push(await page.evaluate(t=>window.Gamecraft.frame(t),t));await page.screenshot({path:path.join(root,'output',`preview-${scene.id}.png`)});}
 }else{
  const args=['-hide_banner','-loglevel','error','-f','image2pipe','-vcodec','mjpeg','-framerate',String(board.fps),'-i','pipe:0','-i',path.join(root,'output/narration.wav'),'-vf','scale=in_range=pc:out_range=tv,format=yuv420p','-color_range','tv','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out];
  const encoder=spawn(process.env.FFMPEG_PATH||'ffmpeg',args,{stdio:['pipe','inherit','inherit']});
  let encoderError;encoder.on('error',e=>{encoderError=e});
  const completion=once(encoder,'close');
  const count=Math.ceil(board.duration*board.fps);
  for(let i=0;i<count;i++){
   const data=await page.evaluate(t=>{const state=window.Gamecraft.frame(t);return {state,jpeg:document.querySelector('canvas').toDataURL('image/jpeg',.91).split(',')[1]}},i/board.fps);
   if(data.state.overflows.length)throw new Error(`Text overflow: ${JSON.stringify(data.state.overflows)}`);
   if(encoderError)throw encoderError;
   if(!encoder.stdin.write(Buffer.from(data.jpeg,'base64')))await once(encoder.stdin,'drain');
   if(i%240===0)console.log(JSON.stringify({frame:i,total:count,scene:data.state.scene}));
  }
  encoder.stdin.end();const [code]=await completion;if(code!==0)throw new Error(`FFmpeg exited ${code}`);
 }
}finally{await browser.close()}
if(pageErrors.length)throw new Error(JSON.stringify(pageErrors));
fs.writeFileSync(path.join(root,'output',preview?'preview-validation.json':'render-validation.json'),JSON.stringify({preview,pageErrors,states,duration:board.duration,fps:board.fps,route:board.route},null,2));
console.log(JSON.stringify({output:preview?'preview PNGs':out,duration:board.duration}));
