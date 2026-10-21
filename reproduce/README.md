# Running the public Message-ID index comparator

This is a *method demonstrator*, not a parser of historical raw sources and not a re-execution of the August 2026 S2 forensic run.

Requirements: Python 3.10+, no third-party dependencies.

```bash
cd reproduce
python -m unittest -v test_p2p_ids
python p2p_ids.py --html-index example_html.csv --mbox-index example_mbox.csv
```

The two CSV inputs must each have a `message_id` header and **one row for each HTML page or mbox message**. Duplicate IDs are allowed and counted separately.

Historical reference checkpoints are:

- 11,784 HTML pages
- 10,782 matching HTML pages by Message-ID
- 1,002 HTML pages without an exact monthly match
- 1,009 distinct monthly Message-IDs without a corresponding HTML page
- 10,771 equal normalized subjects
- 3 monthly messages without Message-ID
- 8 duplicated monthly Message-ID groups

Only the first four fields and the duplicate-group / no-ID method are demonstrated by the provided script. **Subject equality and threading/body normalization require source-specific parsers and are not implemented here**.

The earlier S2 reconstruction reported **7/10 historical structural metrics reproduced**, with three unresolved historical target measures:
- Body normalization old 7008 / 3774 versus conservative rebuilt 7001 / 3781
- Missing thread parent old 2417 versus conservative rebuilt 2392

The historical analysis is not reproducible from CSV indexes alone. Source HTML and 41 monthly `.txt.gz` mbox archives, exact extractor version and normalization conventions are required.

Outputs with zero sample input are not Bitcoin history evidence. Do not commit corpus dumps containing private personal data, unreviewed addresses or messages.

See `evidence/CLAIMS.csv`, `evidence/AUDIT-2026-10-21.md`, and the main `proofs.html` reader-friendly protocols.
