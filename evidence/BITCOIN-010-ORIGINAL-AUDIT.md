# Bitcoin 0.1.0 — the independent Phase 3 and Phase 4 forensic trail

**Historical research record:** this document summarizes our pre-existing `REPORT_PHASE3.md` and `REPORT_PHASE4.md`. It **does not** mean the original executable or archive containers were retrieved and freshly hashed in the October 2026 publication session.

## The exact binary observed in the original audit

| Field | Historical audit value | Meaning / limitation |
| --- | --- | --- |
| Artifact | `bitcoin.exe` | Windows executable in the studied early release archive |
| Byte length | **6,440,960 bytes** | Size is not an authenticity proof alone |
| SHA-256 | `fbcac071d92e26d82ec917214e334bd43850c0691f113bab1d4741c9bdd30d2d` | Identifies exact bytes if recomputed |
| PE format | valid, x86 (`0x014c`) | Portable Executable, 32-bit |
| COFF timestamp | `2009-01-10T23:16:00Z` | **Header value**; not proof of the actual compile time or author |
| Linker reported | `2.56` | PE optional-header linker version |
| Entry-point RVA | 4768 (`0x12a0`) | Stored relative to image base |
| Image base | `0x00400000` | PE image-base header |
| Subsystem | 2 (Windows graphical application) | Header field |
| ASLR / DEP flags | not declared | Describes this binary's header, not modern exploitability |
| Authenticode | not present | No embedded signer identity |
| Overlay / Rich header | none reported | Original scanner observations |

**Reported section data:** `.text` 5,761,536 bytes; `.data` 67,072; `.rdata` 537,088; `.bss` 0 raw bytes; `.idata` 20,480; `.rsrc` 53,760. These are reported section raw sizes, **not** necessarily total mapped/virtual sizes.

Reported imported libraries include `libeay32.dll`, `mingwm10.dll`, `KERNEL32.dll`, `WS2_32.dll` and Windows GUI libraries. Berkeley DB 4.7.25 and MinGW gcc 3.4.5 strings occur in the studied binary. Library strings and DLL dependencies are evidence about software packaging, not about physical location or a hidden personal identity.

A later **external** independent reconstruction by [t4t5](https://github.com/t4t5/bitcoin-0.1-rebuilt) reports **exactly the same SHA-256 and byte count**. The matching values are a cross-reference between two research efforts; our current update **did not recompile t4t5's project**, and we must not claim our historic analysis independently reproduced all its build-environment conclusions.

## Chain of custody and container comparison

The historic Phase 3 report recorded:

- TGZ SHA-256: `ce9da46516e3042741224a7f9061e3181a5a4d17abba72b6e82922af3753d756`
- TGZ SHA-1: `35f83eaa334e0e447ceea77a7cc955a4ccdd1a1d`
- TGZ MD5: `dca1095f053a0c2dc90b19c92bd1ec00`
- **48 of 48** file paths aligned between RAR and TGZ, with matching size and CRC32 recorded
- No missing, extra or discrepant paths in the compared set
- **48/48** member timestamps had `TGZ = RAR + 28,800 seconds`

The Phase 4 report additionally recorded a project-specific audit package with **81/81 manifest entries passing** and **0 recorded integrity errors**, plus a Phase 3 ZIP SHA-256:
`2fa519e7cbab67b4538293d6ae3c87e4d470ba19e7b077d6e9b1997dc6be0a17`.

**Important interpretation:** matching filename+size+CRC32 is strong evidence of archive-member concordance but CRC32 is not cryptographically collision-resistant. The uniform eight-hour timestamp difference is consistent with timezone or archive-creation conversion behavior; it does **not** establish a geographic location, time zone of residence or the identity of Satoshi. RAR, TGZ, derived Phase 3 ZIP and executable hashes identify **different objects**; never substitute one for another.

## Software behavior: code-attested vs deployed vs executed

The original audit found that the early source and binary contain a dormant marketplace design. `CProductsDialog` was defined but not instantiated in the ordinary graphical path studied; four future panels were hidden. Some commercial request/relay commands were present without complete corresponding handling by `ProcessMessage`. The Phase 4 report therefore concluded **not** a complete usable marketplace in the distributed client.

By contrast, the original report traced interactive **IP-payment** message handling:

```text
checkorder → reply(pubkey) → submitorder(transaction) → reply
```

This documents a code path and planned network interaction. No historical live transfer was executed in the research audit. **Do not claim an on-chain transaction was personally reproduced during this investigation.**

### Distinct initial protocol facts reported

| Early Bitcoin 0.1.0 studied | Later evolution / clarification |
| --- | --- |
| Reported P2P protocol version `101` | Version of the studied January 10 state, not necessarily exact January 8 binary |
| Network message header **20 bytes** | The checksum field was introduced later; modern headers have 24 bytes |
| Network checksum **absent** | No assumption that modern wire frames can be replayed against an early client |
| General serialized message maximum **256 MiB** | Distinguish this from block validation |
| Block validation maximum **32 MiB** in the studied early code | A specific **1,000,000-byte** block limit was introduced in a later revision (r103 in our Phase 6 report) |
| Miner block construction target **below 16 MiB** | A construction target is *not* a consensus rule |

These values were reported by the Phase 4 code-and-binary review. They remain subject to confirmation from exact historical source lines and a retrieved binary; do not interpret them as parameters of current Bitcoin Core.

### Evolution to later fixes

- January client studied: first mining implementation is **single-threaded** with a TODO toward one thread per processor; multiprocessor mining arrives later (our historic Phase 6 report links it to r15).
- Early transaction construction: destination output precedes change, and change reuses a key in the studied source; later changes randomized output position and changed key generation. Neither configuration makes all transactions globally traceable or anonymous.
- Early peer time: median-based adjustment, with a noted but unenforced five-minute suggestion; later a 70-minute bound is present by r109, and an explicit warning appears by r141.
- Fifteen legacy Script operations had interpreter `case` handlers in the earlier source; r131 disabled them, while r132 separately addressed the block 74638 monetary overflow.

## How a third party can independently test our claim

1. Obtain the **exact original archive**, document retrieval URL/date/size and hash. Do not run archived binaries on an internet-connected machine carrying private keys.
2. Identify the exact member named `bitcoin.exe` and calculate SHA-256. Expected value is above.
3. Parse PE headers independently; compare size, machine, COFF timestamp, linker fields and section table. Report differences rather than adapting data to fit.
4. Independently compare the historical RAR and TGZ member paths/sizes/CRC32 and preserve the eight-hour difference as a timestamp observation only. Archive metadata is weaker evidence than byte-for-byte file hash.
5. To test behavioral claims, read the matching snapshot's `ui.cpp`, `net.cpp`, `main.cpp`, `script.cpp`, and `market.cpp`; label each finding as *defined*, *reachable*, *handled*, or *historically witnessed*. A source-line hit cannot substitute for end-to-end operation.
6. To compare against t4t5, build its project only in a disposable isolated environment, then compare exact hashes to both claimed originals. Independent rebuild reproducibility and our original archive audit remain separate investigations.

## Remaining boundaries

This current public repository **does not contain** the original historical executable, RAR/TGZ or raw Phase 3/4 research packages. It includes source-bound documentary conclusions only. The old source audits reported that no executable was run. Binary-level checksum equality and code interpretation are evidence, but neither should be mistaken for an authenticated eyewitness record of 2009 use.

**Private working files, unredacted logs and personal details are deliberately excluded.**
