# bitcoin-list — Source-to-code cross-reference (2008–2010)

**Publication status:** a source-indexed set of cross-references to previously public messages, not previously unknown correspondence. Examined via the public Satoshi Nakamoto Institute email pages on 21 October 2026.

## Selected contemporaneous messages

| UTC date | Correspondence | Primary public copy | Technical relevance |
| --- | --- | --- | --- |
| 2008-12-10 17:00:23 | Welcome to bitcoin-list | https://satoshi.nakamotoinstitute.org/emails/bitcoin-list/19/ | Communications infrastructure existed before the 2009 release. |
| 2009-01-12 20:20:47 | Bitcoin v0.1 Alpha release notes | https://satoshi.nakamotoinstitute.org/emails/bitcoin-list/21/ | Announces Windows-only client, inbound port 8333, two sending modes (IP/Bitcoin address), and early mining. |
| 2009-01-25 16:45:25 | Reply to Nicholas Bohm's problem report | https://satoshi.nakamotoinstitute.org/emails/bitcoin-list/24/ | Source for the earliest support/debug-log exchange. |
| 2009-02-04 19:46:04 | Bitcoin v0.1.5 released | https://satoshi.nakamotoinstitute.org/emails/bitcoin-list/25/ | States disk-full, DNS, address-book and network connection fixes; credits early user reports. |
| 2009-12-17 06:52:09 | Bitcoin 0.2 released | https://satoshi.nakamotoinstitute.org/emails/bitcoin-list/29/ | Linux tested on Ubuntu, multiprocessor coin generation, TOR proxy support; acknowledges named contributors. |
| 2010-07-06 21:53:53 | Bitcoin 0.3 released | https://satoshi.nakamotoinstitute.org/emails/bitcoin-list/30/ | JSON-RPC, GUI-less daemon and Mac version. |
| 2010-07-30 06:02:38 | Upgrade to 0.3.6 alert | https://satoshi.nakamotoinstitute.org/emails/bitcoin-list/31/ | Urgent upgrade warning; do **not** conflate with August block 74638 incident. |
| 2010-08-15 20:38:33 | Network investigation alert | https://satoshi.nakamotoinstitute.org/emails/bitcoin-list/32/ | Explicit warning against trusting transactions after block 74638; precedes SVN r131 21:05:16 and r132 21:35:24 UTC in the Phase 6 reconstruction. |

## What the cross-reference actually proves

A contemporaneous announcement shows that its author publicly **described** a feature, warning or release. It is independent contextual corroboration for our archive-based interpretation. It is not, alone, an execution trace or byte-level verification of the binary distributed on the announcement date.

For example:
- The Jan. 2009 release note about IP transfers supports the existence of the **intended interface**; POC-01 still needs the exact source handlers and a version-controlled distribution to establish executable behavior.
- The December 2009 announcement credits **Martti Malmi's port work** and Satoshi's multi-processor support. It can be reconciled with our SVN multi-platform diff and r15 history, but it does not by itself validate every line count.
- The 15 August 2010 warning occurred at 20:38:33 UTC. Its ordering relative to r131 and r132 is supported by the previous Phase 6 report. This illustrates incident response, not an established causal explanation for Satoshi's 2011 withdrawal.

## Reproduction steps

1. Open each **exact** permalink above; record capture date and the link to the original SourceForge archived message if available.
2. Record the claimed date in UTC. Keep distinct the original mail date, the archive ingestion date, the SVN author date and the Git committer date.
3. Compare exact historical snapshots rather than interpreting a modern `src/` keyword match as a 2009 fact.
4. For sensitive source versions, record a SHA-256 of obtained archive bytes and distribution name before unpacking.
5. Use the "observed / reported / corroborated / unresolved" terminology in your published result. Do not infer identity from relay metadata.

## Completeness and attribution caveats

The Satoshi Nakamoto Institute index is a **curated set of messages attributed to Satoshi**, not a demonstrated complete mirror of every message sent by the full bitcoin-list membership. Earlier archives and private threads can be missing from this index.

No IRC messages have been personally attributed to Satoshi through these records. No private, user-identifying information or original unpublished email has been published here.
