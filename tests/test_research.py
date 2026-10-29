import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError

PATH = Path(__file__).resolve().parents[1] / 'skills/gamecraft-research/scripts/research.py'
spec = importlib.util.spec_from_file_location('gamecraft_research', PATH)
research = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)

class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *args): self.close()

class ResearchTests(unittest.TestCase):
    def test_query_limits(self):
        for value in ['', '  ', 'x'*129]:
            with self.assertRaises(research.ResearchError): research.payload_for('search', value)
        self.assertEqual(len(research.payload_for('search', '中'*128)['query']), 128)
        for count in [0,51]:
            with self.assertRaises(research.ResearchError): research.payload_for('search','test',count)

    def test_fetch_rejects_credentials_and_local_targets(self):
        for url in ['file:///tmp/a', 'https://user:secret@example.com/x', 'http://localhost/', 'http://127.0.0.1/', 'http://10.0.0.1/', 'http://[::1]/', 'https:///missing-host']:
            with self.subTest(url=url), self.assertRaises(research.ResearchError): research.payload_for('fetch', url)
        self.assertEqual(research.payload_for('fetch','https://docs.godotengine.org/en/stable/')['url'],'https://docs.godotengine.org/en/stable/')

    def test_different_query_options_do_not_share_cache(self):
        self.assertNotEqual(research.cache_key('search',research.payload_for('search','q',5)),research.cache_key('search',research.payload_for('search','q',10)))

    def test_cached_result_does_not_require_key_or_network(self):
        calls=[]
        def opener(req, timeout):
            calls.append(req)
            return Response(json.dumps({'results':[{'title':'Official','url':'https://example.org'}]}).encode())
        with tempfile.TemporaryDirectory() as directory:
            payload=research.payload_for('search','official docs')
            first=research.run_request('search',payload,directory,key='test-credential',opener=opener,now=100)
            second=research.run_request('search',payload,directory,key='',opener=opener,now=101)
            self.assertFalse(first['cache_hit']); self.assertTrue(second['cache_hit']); self.assertEqual(len(calls),1)
            self.assertNotIn('test-credential',next(Path(directory).glob('*.json')).read_text())
            self.assertEqual(calls[0].full_url,research.ENDPOINTS['search'])

    def test_expired_cache_requires_new_request(self):
        calls=[]
        def opener(req,timeout):
            calls.append(1); return Response(b'{"results":[]}')
        with tempfile.TemporaryDirectory() as directory:
            payload=research.payload_for('search','q')
            research.run_request('search',payload,directory,key='test',opener=opener,now=100)
            research.run_request('search',payload,directory,key='test',opener=opener,now=120,ttl=10)
            self.assertEqual(len(calls),2)

    def test_http_failure_never_retries_or_caches(self):
        calls=[]
        def opener(req,timeout):
            calls.append(1); raise HTTPError(req.full_url,429,'limit',{},None)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(research.ResearchError,'429'):
                research.run_request('search',{'query':'q'},directory,key='test',opener=opener)
            self.assertEqual(len(calls),1); self.assertEqual(list(Path(directory).glob('*.json')),[])

    def test_response_with_error_is_not_evidence(self):
        for data in [{'error':'bad'},{'results':'wrong'},{'results':[{'title':'missing URL'}]}]:
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(research.ResearchError):
                    research.run_request('search',{'query':'q'},directory,key='test',opener=lambda *a,**kw:Response(json.dumps(data).encode()))

    def test_empty_results_remain_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            row=research.run_request('search',{'query':'q'},directory,key='test',opener=lambda *a,**kw:Response(b'{"results":[]}'))
            self.assertEqual(row['data']['results'],[]); self.assertEqual(row['evidence_state'],'discovered')

    def test_fetch_is_retrieved_not_locally_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            row=research.run_request('fetch',{'url':'https://example.com'},directory,key='test',opener=lambda *a,**kw:Response(b'{"title":"Doc","content":"# Doc"}'))
            self.assertEqual(row['evidence_state'],'retrieved')

    def test_output_refuses_overwrite_before_network(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)/'existing.json'; out.write_text('keep')
            self.assertEqual(research.main(['search','q','--dry-run','--out',str(out)]),1)
            self.assertEqual(out.read_text(),'keep')

if __name__=='__main__': unittest.main()
