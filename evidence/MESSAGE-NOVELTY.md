# Previously unknown messages: verification protocol

**Editorial standard:** an archived message can be newly recovered *for this project* without being unknown to the wider community. We do not publish “exclusive Satoshi messages” based on a nickname, an email header or a missing index row.

## Comparison corpora

- Satoshi Nakamoto Institute [email indexes](https://satoshi.nakamotoinstitute.org/emails/threads/) (including bitcoin-list, P2P Research, Cryptography).
- Public [Satoshi Forum Archive](https://jonnyace.github.io/satoshi-forum-archive/): its catalog is described as **543 attributed Satoshi posts**, including one explicitly disputed 2014 entry; not a guarantee that unknown missing posts cannot exist.
- Public [Martti Malmi correspondence](https://mmalmi.github.io/satoshi/), released in 2024 and explicitly incomplete.
- [Mike Hearn's published Satoshi correspondence](https://plan99.net/~mike/satoshi-emails/thread5.html).
- Historical [Bitcoin IRC log directories](https://diyhpl.us/~bryan/irc/bitcoin/): community discussions, not a validated Satoshi account.

## Candidate checklist

1. Preserve source location, file-byte SHA-256, publication/acquisition date, channel, exact UTC timestamp and raw nickname/author string.
2. Normalize only *for matching*, not to alter the original evidence. Preserve punctuation, case and line breaks in the retained source.
3. Deduplicate on Message-ID where possible, then compare normalized textual content, dates and reply-chain links across archives.
4. Identify existing mirrors and contemporary citations. A known message absent from one index is not “previously unknown.”
5. Classify authorship as **originally signed/authenticated**, **archived attributed**, **nickname only**, or **unknown**. Do not promote “nickname only” without independent evidence.
6. Publish candidate metadata and rationale without exposing private email addresses, raw log metadata or private personal details.
7. State **provenance uncertain** whenever proof is missing; allow disagreement.

## Publication format

| Field | Allowed values |
|---|---|
| Evidence ID | Stable identifier, e.g. CAND-001 |
| Source type | Mailing list / forum / IRC / private correspondence later released |
| Date | Original declared UTC and captured UTC, distinguished |
| Original identifier | Message-ID / forum permalink / IRC file and line offsets |
| Attribution | Authenticated / independently corroborated / claimed / unknown |
| Novelty | Already indexed / archived variant / uncertain / possibly previously unindexed |
| Confirming evidence | Independent URL + immutable revision or hash |
| Editorial conclusion | Strictly limited to supported information |

No positive novelty claim exists in this repository without an actual candidate having undergone this review.
