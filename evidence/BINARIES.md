# Two early Windows DLLs — documentary fingerprints

Extracted from the Phase 9 research report (7 August 2026). These are historic reported values, **not freshly hashed files** in this repository.

| Component | Reported SHA-256 | PE timestamp | Other historical indicators |
| --- | --- | --- | --- |
| `libeay32.dll` | `d108cdff2922a60e0054718a84178a40526ba00401fa34a87fb055947c77a182` | 2008-08-28 | OpenSSL 0.9.8h / MinGW32 |
| `mingwm10.dll` | `1badf3972d9a861a69fafb2c5e3282aecc30007b9d51c199806e542b32d7708f` | 2007-08-03 | MinGW runtime |

## Reproduce on a legitimately obtained historic distribution

```bash
sha256sum libeay32.dll mingwm10.dll
file libeay32.dll mingwm10.dll
strings libeay32.dll | grep -i -E 'openssl|mingw'
```

PowerShell SHA-256: `Get-FileHash -Algorithm SHA256 .\libeay32.dll`.

Record source archive URL and checksum **before extraction**. A shared DLL hash can show common vendor toolchain or packaging, not the identity or physical device of the developer. The independent t4t5 reconstruction provides additional, separately attributed, evidence about the January 2009 release: https://github.com/t4t5/bitcoin-0.1-rebuilt.