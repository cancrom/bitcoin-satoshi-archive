# Coverage matrix — public edition versus historic research

Updated **21 October 2026** against the 8 August 2026 final report, the 7 August Phase 9 technical report, Phase 6 adversarial report, Phase 7 folder-integrity audit and v5 source-code claim register.

**Purpose:** show where each *identified historical topic* is published. This is not a numerical claim that all original source files are present or that all historical observations have been independently verified.

| Topic | Reader-facing location | Evidence or method | Coverage |
| --- | --- | --- | --- |
| History and scope | `index.html#top` | `proofs.html#approach` | Covered |
| Pre-launch 2008 code / provenance limits | `index.html#avant-publication` | Original Bitcointalk source attribution | Covered with limitations |
| Jan 2009 binary reconstruction by t4t5 | `index.html#avant-publication` | External build project and SHA-256 | Covered, third-party result |
| 2009 public wallet GUI | `index.html#chapter-1` | `proofs.html#cases` | Covered, reconstruction |
| Send-to-IP / checkorder / submitorder | `index.html#chapter-2` | POC-01 | Covered, implementation vs use qualified |
| Market product listing / ranking | `index.html#chapter-3` | POC-02, E009 | Covered, prototype |
| Reviews, signed reputation, Power/atoms | `index.html#chapter-4` | E009 and Phase 9 | Covered, prototype |
| Dynamic order form up to 20 fields | `index.html#chapter-5` | POC-02 and Phase 9 | Covered, prototype |
| Escrow/order panels hidden from public workflow | `index.html#chapter-6` | Phase 9 UI report | Covered, not shipped UI |
| Market UI removal vs remaining wire primitives | `index.html#chronique-technique` | POC-12 / r64→r180 | Covered, historic report |
| Script opcodes r131 versus overflow r132 | `index.html#chapter-8` | POC-03; source register | Covered, corrected |
| Dedicated 1 MB block limit r103 | `index.html#chapter-7` | POC-04 | Covered, corrected |
| r15 mining and change privacy | `index.html#chronique-technique` | POC-11 | Covered, reported |
| Clock-time protections r109/r141 | `index.html#chronique-technique` | POC-13 | Covered, reported |
| Network checksums r78 | `index.html#chronique-technique` | Source and Phase 6 report | Covered, reported |
| IRC/HTTP/peer map/bootstrap | `index.html#chapter-10` | POC-06, E010/E013 | Covered; no IRC speaker attribution |
| SVN copy ancestry 33/33 and 42 files | `index.html#chapter-11` | POC-07 | Covered; needs original SVN mirror |
| P2P HTML/mbox numerical audit | `index.html#chapter-12` | POC-08 + duplicate-aware script | Covered with historic normalization gap |
| Five P2P mail copies and metadata limitations | `index.html#archive-finds` | POC-09 | Covered without identity inference |
| Linux port tree delta | `index.html#chronique-technique` | POC-14 | Covered, reported |
| Two early DLL hashes | `index.html#sources-methodes` | `evidence/BINARIES.md` | Covered, historical values |
| Signed alerts and limits | `index.html#satoshi-crises` | POC-10, E007/E014 | Covered without backdoor claim |
| Genesis newspaper marker | `index.html#satoshi-crises` | E006 | Covered without location inference |
| Maintenance comments and incomplete persistence | `index.html#satoshi-crises` | `evidence/COMMIT-ANCHORS.md` | Covered, bounded interpretation |
| 2010 overflow and 2011 withdrawal | `index.html#satoshi-crises` | Public correspondence links | Covered, no causal claim |
| Selected Hal, Malmi and Hearn correspondence | `index.html#correspondances` | Original published sources | Covered, selective not complete corpus |
| S9 IRC source inventory and recovery protocol | `index.html#pistes-inexplorees` | `evidence/IRC-SOURCES.md` | Partial: no verified message-level output |
| S2 original ZIP and exact original body/thread normalization | `proofs.html#ledger` | `evidence/AUDIT-2026-10-21.md` | Blocked by missing original |
| Seven reconstructed UI images incl. review editor | `index.html#comparaisons-visuelles`, `#chronique-technique` | Six embedded PNGs + one HTML explanatory layout | Partial: exact seventh source PNG not uploaded |
| Nine original archive containers | `proofs.html#ledger` | historical digests, Phase 7 audit distinction | Partial: referenced not distributed |

## Real limitations — not a completion percentage

- **Research history coverage:** the themes we could identify in the retrieved reports are indexed above.
- **Primary data completeness:** unresolved; S1–S9 not all present in our public working copy.
- **Independent test coverage:** only the comparator method was exercised against synthetic fixture data in this publication workflow, not historical corpora or old binaries.
- **IRC attribution:** unresolved; no authenticated Satoshi IRC dialogue or “previously unknown” message is claimed.
- **Visual fidelity:** six PNG reconstructions included in the article; additional review-control schematic is labeled as editorial, not as a period screenshot.

A new corroborated result should update both `evidence/CLAIMS.csv` and this matrix, with its immutable source reference, negative controls and dated output.
