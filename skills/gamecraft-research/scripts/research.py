"""Small, cached DeepSeek Search/Fetch client. Python 3.10+, standard library only."""
from __future__ import annotations
import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ENDPOINTS = {'search': 'https://api.deepseek.com/v1/tools/search', 'fetch': 'https://api.deepseek.com/v1/tools/fetch'}

class ResearchError(Exception):
    pass

def payload_for(kind, value, count=5, with_content=False):
    if kind == 'search':
        if not value.strip() or len(value) > 128:
            raise ResearchError('Search query must contain 1–128 characters.')
        if not 1 <= count <= 50:
            raise ResearchError('Search count must be 1–50.')
        return {'query': value, 'count': count, 'need_content': with_content}
    if kind != 'fetch':
        raise ResearchError('Unknown operation.')
    try:
        parsed = urlsplit(value)
        host = (parsed.hostname or '').lower()
        if len(value) > 8192 or parsed.scheme not in ('http', 'https') or not host or parsed.username is not None or parsed.password is not None:
            raise ValueError()
        if host == 'localhost' or host.endswith(('.localhost', '.local')):
            raise ValueError()
        try:
            if not ipaddress.ip_address(host).is_global:
                raise ValueError()
        except ValueError as exc:
            if host.replace('.', '').isdigit() or ':' in host:
                raise ValueError() from exc
    except ValueError:
        raise ResearchError('Fetch requires a public HTTP(S) URL without credentials.') from None
    return {'url': value}

def cache_key(kind, payload):
    raw = json.dumps([kind, payload], sort_keys=True, ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def valid_body(kind, body):
    if not isinstance(body, dict) or body.get('error'):
        return False
    if kind == 'search':
        results = body.get('results')
        return isinstance(results, list) and all(isinstance(r, dict) and isinstance(r.get('url'), str) and isinstance(r.get('title'), str) for r in results)
    return isinstance(body.get('title'), str) and isinstance(body.get('content'), str)

def run_request(kind, payload, cache_dir, *, key=None, refresh=False, ttl=86400, opener=urlopen, now=None):
    if kind not in ENDPOINTS or ttl < 0:
        raise ResearchError('Invalid operation or cache TTL.')
    stamp = time.time() if now is None else now
    cache_path = Path(cache_dir) / (cache_key(kind, payload) + '.json')
    if not refresh and cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text(encoding='utf-8'))
            age = stamp - cached['fetched_at_unix']
            if cached.get('operation') == kind and cached.get('request') == payload and 0 <= age < ttl and valid_body(kind, cached.get('data')):
                return dict(cached, cache_hit=True)
        except (ValueError, KeyError, TypeError):
            pass
    token = key if key is not None else os.environ.get('DEEPSEEK_API_KEY')
    if not token:
        raise ResearchError('Set DEEPSEEK_API_KEY to make a network request; cached results remain usable without it.')
    req = Request(ENDPOINTS[kind], data=json.dumps(payload).encode('utf-8'), headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, method='POST')
    try:
        with opener(req, timeout=45) as response:
            body = json.load(response)
    except HTTPError as error:
        raise ResearchError(f'DeepSeek HTTP {error.code}; not retried. Check authentication, quota, or rate limits.') from None
    except (URLError, TimeoutError, OSError):
        raise ResearchError('DeepSeek network request failed; outcome may be unknown and was not retried.') from None
    except (ValueError, UnicodeError):
        raise ResearchError('DeepSeek returned invalid JSON; not cached.') from None
    if not valid_body(kind, body):
        raise ResearchError('DeepSeek response schema was invalid; not cached.')
    record = {'provider': 'deepseek-search-fetch', 'operation': kind, 'request': payload, 'fetched_at_unix': stamp, 'evidence_state': 'discovered' if kind == 'search' else 'retrieved', 'cache_hit': False, 'data': body}
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = cache_path.with_suffix('.tmp')
    temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(cache_path)
    return record

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('operation', choices=ENDPOINTS)
    p.add_argument('value', help='Search query or public page URL')
    p.add_argument('--count', type=int, default=5)
    p.add_argument('--with-content', action='store_true')
    p.add_argument('--cache-dir', type=Path, default=Path('.cache/gamecraft-research'))
    p.add_argument('--ttl', type=float, default=86400)
    p.add_argument('--refresh', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--out', type=Path)
    args = p.parse_args(argv)
    try:
        payload = payload_for(args.operation, args.value, args.count, args.with_content)
        if args.ttl < 0:
            raise ResearchError('TTL must not be negative.')
        if args.out and args.out.exists():
            raise ResearchError('--out already exists; choose a new path.')
        result = {'method': 'POST', 'endpoint': ENDPOINTS[args.operation], 'payload': payload, 'network_called': False} if args.dry_run else run_request(args.operation, payload, args.cache_dir, refresh=args.refresh, ttl=args.ttl)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with args.out.open('x', encoding='utf-8') as stream:
                json.dump(result, stream, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except ResearchError as error:
        print(json.dumps({'error': str(error)}), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
