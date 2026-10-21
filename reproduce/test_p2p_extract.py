"""Synthetic ZIP fixtures only; not validation of historical S1 contents."""
import gzip, tempfile, unittest, zipfile
from pathlib import Path
from p2p_extract import html_record, summary

class P2PExtractorTests(unittest.TestCase):
    def test_percent_encoded_plus_preserved(self):
        doc = b'<link rel="made" href="mailto:x@y?In-Reply-To=%3Ca%2Bb%40domain.test%3E"><h1> Hello &amp; world </h1>'
        self.assertEqual(html_record(doc), ('<a+b@domain.test>', 'Hello & world'))

    def test_zip_structural_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test-synthetic.zip'
            def page(key, subj):
                return (f'<link rel="made" href="mailto:x@y?In-Reply-To=%3C{key}%3E">'
                        f'<h1>{subj}</h1>').encode()
            mbox = (b'From one@example.test Mon Jan 01 00:00:00 2024\nMessage-ID: <A@x>\nSubject: One\n\nfirst\n\n'
                    b'From two@example.test Tue Jan 02 00:00:00 2024\nMessage-ID: <B@x>\nSubject: Two\n\nsecond\n\n'
                    b'From three@example.test Wed Jan 03 00:00:00 2024\nMessage-ID: <B@x>\nSubject: Two\n\nthird\n\n')
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('arch/000001.html', page('A@x', 'One'))
                archive.writestr('arch/000002.html', page('A@x', 'One'))
                archive.writestr('arch/000003.html', page('C@x', 'Three'))
                archive.writestr('arch/2024-January.txt.gz', gzip.compress(mbox))
            result = summary(path)
            self.assertEqual(result['html_message_pages'], 3)
            self.assertEqual(result['monthly_messages'], 3)
            self.assertEqual(result['html_pages_matching_monthly_id'], 2)
            self.assertEqual(result['html_pages_without_monthly_match'], 1)
            self.assertEqual(result['unique_monthly_ids_without_html'], 1)
            self.assertEqual(result['equal_subject_rows'], 2)
            self.assertEqual(result['duplicate_monthly_id_groups'], 1)

if __name__ == '__main__':
    unittest.main()
