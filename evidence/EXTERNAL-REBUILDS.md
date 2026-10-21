# Independent early-client reconstructions — evidence cross-checks

**Research status (21 October 2026):** these are two *external public projects* offering separate forms of historical reconstruction. Their results have been reviewed as published claims, **not independently rebuilt for this site's release**.

## Case A — reproducible January 2009 binary

**t4t5 / bitcoin-0.1-rebuilt**
https://github.com/t4t5/bitcoin-0.1-rebuilt

The project's README reports that it rebuilt a historical `bitcoin.exe` byte-for-byte:

- Executable size: **6,440,960 bytes**
- Reported SHA-256: `fbcac071d92e26d82ec917214e334bd43850c0691f113bab1d4741c9bdd30d2d`
- Reported original `bitcoin-0.1.0.rar` size: **2,132,686 bytes**
- Reported archive MD5: `91e2dfa2af043eabbb38964cbf368500`
- Reported archive SHA-1: `ec9ed4ccbc990eceb922ff0c4d71d1ad466990dd`
- Important timeline boundary: the surviving early archive's rebuilt binary dates to **10 January 2009** in the external research. It should not automatically be substituted for a fully authenticated 8 January release.

The project documents a period Windows toolchain and its reconstruction, including MinGW and wxWidgets. Refer to its exact files before asserting byte identity.

### Community procedure

1. Read and audit the external build scripts before executing them.
2. Rebuild from pinned source/dependencies in a disposable environment with **no keys/wallet files** and **no access to a live, funded Bitcoin node**.
3. Compute SHA-256 over the resulting binary and compare against the stated expected value. An exact hash match tests binary identity, not personal identity.
4. Capture the source revision, toolchain versions, full output and UTC test date.
5. Report a mismatch without changing inputs merely to force a match.

## Case B — earlier code preview and independently re-created GUI

**Kino1994 / bitcoin-history**
https://github.com/Kino1994/bitcoin-history

This second public project groups:
- `bitcoin-nov08/`: a November 2008 partial source preview, described as *not* independently compilable;
- `bitcoin-nov08-rebuild/`: a modern compilable GUI recreation; the project explicitly describes its UI as **newly recreated** rather than a recovered 2008 `ui.cpp`;
- historic January 2009 v0.1.0 and v0.1.3 source/binary collections;
- `irc/`: modified early clients with IRC bootstrap adaptations intended for newer environments.

**Do not confuse** a reconstructed GUI, the exact original early source, a later client version, or a patched client using a modern IRC service. They answer different historical questions.

## Relevance to our own work

This additional corpus may help future reviewers verify our interface reconstruction and separate period UI behavior from features visible only in code. It can also be used for an external independent cross-check of the 2009 prototype, but no live-network test has been performed in this repository.

### Safe reproduction boundary

Run historic unmaintained executables **only inside isolated environments**, without real private keys, wallet files, personal data, or normal network privileges. A modern recompile with network patches is **not** equivalent to an untouched 2009 binary. Never treat external author's machine attribution or historical tooling fingerprints as conclusive proof of Satoshi's real identity/location.

Source status: third-party claims; independent compilation not carried out in this publication pass.
