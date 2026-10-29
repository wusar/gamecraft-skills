"""Validate portable skill metadata, evidence references, and public-file hygiene."""
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
errors=[];skills=[]
for folder in sorted((ROOT/'skills').iterdir()):
 if not folder.is_dir(): continue
 file=folder/'SKILL.md'
 if not file.exists(): errors.append(f'{folder.name}: missing SKILL.md');continue
 body=file.read_text(encoding='utf-8')
 if not body.startswith('---\n'):errors.append(f'{folder.name}: missing YAML frontmatter');continue
 head=body.split('---',2)[1]
 match=re.search(r'^name:\s*([a-z0-9-]+)\s*$',head,re.M)
 if not match or match[1]!=folder.name:errors.append(f'{folder.name}: name mismatch')
 if not re.search(r'^description:\s*\S',head,re.M):errors.append(f'{folder.name}: missing description')
 skills.append(folder.name)
 for doc in folder.rglob('*.md'):
  content=doc.read_text(encoding='utf-8')
  for target in re.findall(r'\]\(([^)]+)\)',content):
   if '://' in target or target.startswith('#'):continue
   if not (doc.parent/target.split('#')[0]).exists():errors.append(f'{doc.relative_to(ROOT)}: broken link {target}')
registry=json.loads((ROOT/'research/sources.json').read_text(encoding='utf-8'))
ids=[s['id'] for s in registry['sources']]
if len(ids)!=len(set(ids)):errors.append('Duplicate source ids')
sources={s['id']:s for s in registry['sources']}
for claim in registry['claims']:
 for id_ in claim['source_ids']:
  if id_ not in sources:errors.append(f'{claim["id"]}: missing source {id_}');continue
  if 'timestamp_seconds' in claim and sources[id_]['type']=='video' and not 0<=claim['timestamp_seconds']<sources[id_]['duration_seconds']:errors.append(f'{claim["id"]}: invalid timestamp')
 if not claim.get('conditions') or not claim.get('verify'):errors.append(f'{claim["id"]}: missing conditions or verification')
for file in ROOT.rglob('*'):
 if not file.is_file() or any(p in ('.git','.cache','output','node_modules','__pycache__') for p in file.relative_to(ROOT).parts):continue
 if file.suffix.lower() in ('.m4a','.m4s','.wav','.mp4','.webm'):errors.append(f'Private/generated media should not be tracked: {file.relative_to(ROOT)}')
 if file.suffix.lower() not in ('.md','.py','.json','.yaml','.yml','.mjs','.html','.ps1','.txt'):continue
 content=file.read_text(encoding='utf-8')
 if re.search(r'sk-[A-Za-z0-9_-]{20,}',content):errors.append(f'Potential credential: {file.relative_to(ROOT)}')
 if re.search(r'[A-Z]:[/\\]Users[/\\]',content):errors.append(f'Private machine path: {file.relative_to(ROOT)}')
print(json.dumps({'skills':skills,'sources':len(sources),'claims':len(registry['claims']),'errors':errors},ensure_ascii=True,indent=2))
raise SystemExit(bool(errors))
