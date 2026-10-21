# Early source-code evidence anchors (original v5 independent check)

**Status:** values transcribed from the independent audit dated 4 August 2026. They are **historical report findings**, not source trees re-downloaded and rechecked during this public update. All identifiers are Git-object or SVN-mirror references from the old research and may require that exact imported history.

| Case | Historical anchor | What is supported | What it does not prove |
| --- | --- | --- | --- |
| E001 | Added `8be979d9aef6` on 2010-01-28, removed `5253d1ab77fa` on 2010-02-15; `ui.cpp`. | An interface-maintenance frustration comment existed. | Overall burnout or reason Satoshi left. |
| E002 | `main.cpp`; first seen `98500d70a8cf` on 2010-02-12, removed in `75199de534a5` by 2010-02-20. | A local, non-transactional `fSpent` update was discussed in a source comment. | Rejection of all database transaction guarantees. |
| E003 | `market.cpp`; earliest accessible SVN import `e071a3f6c06f` (2009-08-30), removed `5253d1ab77fa`; original recorded author `sirius-m`. | Comment states persistence was not yet solved. | On-chain commercial database or automatic line attribution to Satoshi. |
| E004A | `bignum.h`; `c4319e678f69` (2010-02-14). | A 64-bit `BN_rshift` edge-case comment. | General compromise of arithmetic. |
| E004B | `bignum.h`; `6ff5f718b6a6` (2010-07-31). | Addition of a `BN_cmp` guard. | Proof all neighboring cases were fixed. |
| E005 | `net.cpp`; external-IP lookup later replaced at `222e3de4be2e` (2010-11-15). | A bootstrap dependency evolved. | Loss of all P2P connectivity. |
| E006 | `main.cpp`; genesis `The Times` string in historic snapshots. | The string is present. | Physical location when inserted or dated original insertion. |
| E007 | SVN r142 `401926283a200994ecd7df8eae8ced8e0b067c46` (2010-08-25); parallel commit `522dfe3422f562368ebdaeb2b1a13cc9ebafa333` (2010-08-28). | Signed alert mechanism timeline. | Arbitrary code execution or consensus takeover. |
| E008 | Small lexical count: `optimise` 1, `optimize` 1, `optimized` 1; three license-context occurrences were not useful as dialect evidence. | Mixed spelling in the examined snapshot. | Nationality or residence. |
| E009 | Historic `market.h` + `market.cpp` term occurrences: `CProduct` 15, `CReview` 8, `CReviewDB` 3, `mapProducts` 10, `vOrderForm` 3. | Lexical presence of a substantial commercial prototype. | A running decentralized commerce service. |
| E010 / E013 | `net.cpp` / `irc.cpp`; `GetMyExternalIP`, `ConnectNode`, `AddAddress`, `-noirc`, `-connect`; empty address map later seeded after around 60 seconds. | Different mechanisms for external address, discovery and connection. | IRC being the sole route to Bitcoin peers. |
| E011 | `market.cpp` seen `01fe1d2137d5`, absent by `5253d1ab77fa`. | Module removal boundaries in the examined files. | Removal of every `checkorder` and `submitorder` string. |
| E012 | Early `GetBlockValue`: `nSubsidy=50*COIN; nSubsidy >>= (nHeight/210000)`. | Reward-halving formula in the examined snapshot. | An immediate present-day flaw; long-range shift behavior needs a separate test. |
| E014 | `CAlert::Cancels` contains an apparent no-op `if (!IsInEffect()) false;` in the analyzed version. | Potential source-level defect candidate. | Exploitability or bypass of operational checks; other code filters expired alerts. |

**How to validate:** obtain the exact source import including referenced commits; examine the parent and child diff; record full hash, file path, line span, acquisition URL, screenshot/output and caveats. A keyword count is not a proof of network behavior.

No identity inference is supported by these comments, timestamps, DLLs or mail routing metadata.
