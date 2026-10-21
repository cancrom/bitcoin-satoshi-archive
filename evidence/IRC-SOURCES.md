# IRC reconstruction — coverage and attribution boundary

The earlier private research created a multi-source recovery utility `bitcoin_irc_multisource_recovery_v2.py` with the following planned inputs:

- The historical `bitcoin-logs.2010-2018.tar.bz2` archive, internally catalogued as S9.
- Archived Bitcoinstats pages through Wayback (HTTP/HTTPS and www variants).
- A previously available Veritas/cdecker directory.
- Public daily files indexed at `https://diyhpl.us/~bryan/irc/bitcoin/bitcoin-dev/`.

Planned outputs included: `REPORT.md`, `summary.json`, `daily-coverage.csv`, `coverage-gaps.json`, `irc-normalized.csv`, `irc-normalized.jsonl`, `line-provenance.jsonl`, `file-inventory.json`, `wayback-cdx-index.json`, and `integrity-manifest.json`.

**These planned output formats are not the same as verified findings.** The current public edition contains no independently validated line of IRC dialogue attributed to Satoshi.

## Community submission schema

| field | meaning |
| --- | --- |
| source URL and archive hash | Exact public artifact and immutable digest |
| channel | e.g. #bitcoin or #bitcoin-dev |
| UTC timestamp | Raw format and normalization rule |
| nickname | As written in the original log; do not infer civil identity |
| content span | Exact line offsets; quotation limited by source license |
| corroboration | Matching contemporaneous email, commit, post or issue |
| editorial status | Transcript verified / nickname unverified / attribution disputed |

Do not publish raw personal data or invent lines when a channel or day is missing.

Reference public archive: https://diyhpl.us/~bryan/irc/bitcoin/bitcoin-logs.2010-2018.tar.bz2
