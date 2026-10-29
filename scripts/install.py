"""Install the bundled skills by copying; dry-run unless --apply is passed."""
import argparse
import os
from pathlib import Path
import shutil

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest',type=Path,default=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'skills')
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    sources=sorted((Path(__file__).resolve().parents[1]/'skills').iterdir())
    targets=[args.dest/s.name for s in sources if s.is_dir()]
    if any(t.exists() for t in targets):
        parser.error('A target already exists; compare and back it up before updating. Nothing was copied.')
    for source,target in zip([s for s in sources if s.is_dir()],targets):
        print(f'{"COPY" if args.apply else "PLAN"} {source.name} -> {target}')
        if args.apply:
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(source,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.cache'))
    return 0

if __name__=='__main__': raise SystemExit(main())
