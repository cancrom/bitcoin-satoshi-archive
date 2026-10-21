# Bitcoin avant la légende / Bitcoin Before the Legend

**Enquête historique bilingue et illustrée sur Bitcoin (2008–2011).**

*Bilingual illustrated historical study of Bitcoin's early software, conversations and forgotten mechanisms.*

### [Lire le reportage / Read the historical feature](https://cancrom.github.io/bitcoin-satoshi-archive/)

### [Laboratoire de preuves / Evidence and reproducibility lab](https://cancrom.github.io/bitcoin-satoshi-archive/proofs.html)

Le reportage rassemble les recherches éditoriales et leurs limites. Le laboratoire propose **17 protocoles de vérification**, un registre des archives historiques et un comparateur de Message-ID capable de conserver les doublons.

The feature presents editorial findings and their limits. The evidence lab offers **17 verification procedures**, an archive ledger and a duplicate-aware Message-ID index comparator.

## Documentation ouverte / Public supporting material

- [Manifeste des archives S1–S9 / Historic archive SHA-256 manifest](evidence/ARCHIVE-MANIFEST.csv)
- [Vérificateur SHA-256 / Safe archive integrity checker](reproduce/verify_archives.py)
- [Récupérateur S1/S9 avec contrôle d'intégrité / Opt-in public S1/S9 fetcher](reproduce/download_public_archives.py)
- [Sources historiques S1/S9 / Historic S1/S9 URLs](evidence/PUBLIC-ARCHIVE-SOURCES.csv)
- [Comparaison des reconstructions externes / Independent rebuild comparisons](evidence/EXTERNAL-REBUILDS.md)

- [Contrôles réalisés et limites actuelles / Executed checks and current limits](evidence/STATUS-2026-10-21.md)
- [Vérifier les prétendus messages inédits / Assess novelty and attribution](evidence/MESSAGE-NOVELTY.md)

- [Matrice de couverture / Research coverage matrix](evidence/COVERAGE.md)
- [État de l'audit documentaire / Reconciliation audit](evidence/AUDIT-2026-10-21.md)
- [Messages bitcoin-list et correspondance au code / Source-to-code correspondence](evidence/BITCOIN-LIST.md)
- [Registre des affirmations / Claims ledger](evidence/CLAIMS.csv)
- [Références des commentaires et commits / Commit anchors](evidence/COMMIT-ANCHORS.md)
- [Empreintes DLL rapportées / Documented DLL fingerprints](evidence/BINARIES.md)
- [Provenance des sources IRC / IRC provenance and limits](evidence/IRC-SOURCES.md)
- [Guide de reproduction / Reproduction guide](reproduce/README.md)
- [Extracteur direct de S1 / Raw S1 P2P ZIP extractor](reproduce/p2p_extract.py)
- [Comparateur P2P / P2P Message-ID comparator](reproduce/p2p_ids.py)
- [Tests méthodologiques / Comparator tests](reproduce/test_p2p_ids.py)

## La différence entre documentation et reproduction

Les résultats de l'enquête d'août 2026 ont été confrontés aux versions finales et aux audits contradictoires. **Cela ne signifie pas que les conteneurs S1–S9 sont hébergés ou revérifiés dans ce dépôt.**

The August 2026 findings have been reconciled against the final publications and adversarial audit reports. **This does not mean the original S1–S9 containers are hosted or newly reverified in this repository.**

- **8/9** : empreintes concordantes *rapportées dans le contrôle historique final*.
- **0/9** : pièces présentes dans le répertoire **distinct** utilisé lors de l'audit Phase 7 ; aucune empreinte vérifiable dans cette exécution.
- **7/10** : métriques historiques d'archives P2P reproduites avec les conventions explicites alors utilisées.
- **S2** : conteneur ZIP d'origine toujours signalé comme manquant.

Les illustrations du reportage sont des **reconstitutions éditoriales**, jamais des captures authentifiées de 2009. Les affirmations concernant l'identité, la localisation ou des échanges IRC attribués à Satoshi sont volontairement limitées aux preuves disponibles.

The illustrations are **editorial reconstructions**, not authenticated 2009 screenshots. Identity/location speculation and unsupported IRC authorship attributions are not presented as facts.

**Project status:** public research edition, historical findings audited for wording and completeness; independent end-to-end reproduction remains incomplete without the original source material.


### Contrôles automatiques / Automated checks

[GitHub Actions — documentaire et tests](https://github.com/cancrom/bitcoin-satoshi-archive/actions/workflows/evidence-check.yml) — scripts de vérification HTML et tests synthétiques, sans dépendance aux archives historiques manquantes. **La publication du workflow ne garantit pas encore la réussite d'une exécution.**


### Récupération volontaire des archives / Opt-in source recovery

```bash
python reproduce/download_public_archives.py --id S1 --directory ./archives
python reproduce/download_public_archives.py --id S9 --directory ./archives
python reproduce/verify_archives.py --directory ./archives --inspect-members
```

Le récupérateur ne décompresse pas et refuse les empreintes incorrectes. Il ne fonctionne que si les sources publiques sont accessibles depuis votre appareil. / The fetcher never extracts files and refuses mismatched digests. Public source availability depends on your network.
