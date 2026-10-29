# Fork review: DS220j / RTL8156B

Reviewed 2026-10-29 against upstream `477a723a41c3340bd7d701f657711c334d0c42bd`.
The supplied GitHub forks page could not be fetched and the connector does not
expose the forks-list endpoint. Instead, repository searches for r8152/Synology
forks pushed since 2025-10-29 were cross-checked against each repository's
`source.full_name=bb-qq/r8152`. This found 29 matching forks. All listed branch
heads were inspected, deduplicated to 30 SHAs, and compared with upstream.
This is search-based coverage, not a guarantee that GitHub indexed every renamed fork.
Generic and historical branches were checked too; ahead counts are commit ancestry,
not proof of unique useful changes. No verified DS220j stability fix was found.

## Decisions

- **chadlwilson/syno-driver-realtek-r8152**: adopt the RTD1296/DSM 7.4 container
  approach as a draft, with attribution. Move EnvDeploy to privileged runtime,
  propagate failures, pin toolkit source, collect artifacts and source checksums.
  Do not wholesale merge its older driver/header: the current upstream source
  retains additional TX timestamp updates, compatibility guards and device IDs.
- **henrycarrero/r8152**: useful manual-build CI idea, but not safe to copy as-is.
  Its `EnvDeploy -t` disables downloads (an empty cache will not be populated);
  its `PkgCreate.py -S` is absent from the official DSM7.4 argument parser.
  Artifact search uses `-maxdepth 1`, missing nested collected SPKs.
  The two latest observed workflow runs failed; the source inspection identifies
  these risks without claiming they explain every run failure.
- **DARQEnergy/r8152**: useful same-filesystem source-copy/hard-link insight;
  defaults target DS1819+ / denverton DSM 7.3, not this NAS.
- **jaykumar2001/r8152 docker-spk-build**: reject for DS220j. Hard-coded x86_64
  kernel paths/ARCH and native gcc compile both driver and helper for the wrong
  architecture; changing PLATFORM alone does not fix it. Also suppresses archive
  extraction errors. VLAN branch retains the issues recorded in our earlier review.
- **HeyMingjin/dsm_r8152**: its TX timeout fix adds `netif_trans_update()` to both
  bulk completion callbacks. Both calls already exist in current upstream/our base.
- **stickpin/r8152**: 2.21.4 vendor update and compatibility additions are superseded
  by our 2.22.1 base; verified the queue helper and PHY OCP enum entries exist.
- **malhal/r8152**: helper-recovery wording already exists. The USB-C orientation
  note overgeneralizes all adapters; relevant only to affected converters.
  Historical 2.14 LPM patch is not a new RTD1296 fix; modern driver already sets
  `disable_hub_initiated_lpm`. Do not transplant old power-management code blindly.
- **steveduff/r8152**: README adds a 5 GbE RTL8157 model and a duplicated bullet.
  No benefit for the user's RTL8156B.
- **007revad/r8152**: already imported in fork PR #1.
- **maxromanovsky/r8152**, **henrycarrero** troubleshooting branch: reviewed earlier;
  corrected guidance is proposed in fork PR #2.
- Other inspected default heads have no commits ahead of upstream.

No driver change from another fork was merged as a result of this review.
The build-tooling draft must pass a real SDK build before merge.

## Inventory

| Fork | Selected branch heads (all other listed branches also compared) |
| --- | --- |
| [chinamilk/r8152](https://github.com/chinamilk/r8152) | `master` eb067ccc0ebd (0 commits ahead) |
| [superwh/r8152](https://github.com/superwh/r8152) | `master` a9130c2d19e5 (0 commits ahead) |
| [Shawn1565/r8152](https://github.com/Shawn1565/r8152) | `master` 477a723a41c3 (0 commits ahead) |
| [acostaja/r8152](https://github.com/acostaja/r8152) | `master` eb067ccc0ebd (0 commits ahead) |
| [stickpin/r8152](https://github.com/stickpin/r8152) | `master` fcb837f103dc (3 commits ahead) |
| [Sh0rtC1rcu1t/r8152](https://github.com/Sh0rtC1rcu1t/r8152) | `master` eb067ccc0ebd (0 commits ahead) |
| [jaykumar2001/r8152](https://github.com/jaykumar2001/r8152) | `docker-spk-build` 41c5860b7cee (1 commits ahead); `fix/vlan-persistence` 41a509f2aaf3 (1 commits ahead); `master` a9130c2d19e5 (0 commits ahead) |
| [tailwind0/r8152](https://github.com/tailwind0/r8152) | `master` a9130c2d19e5 (0 commits ahead) |
| [DylanBatt/r8152](https://github.com/DylanBatt/r8152) | `master` a9130c2d19e5 (0 commits ahead) |
| [alioshasemionov/r8152](https://github.com/alioshasemionov/r8152) | `master` a9130c2d19e5 (0 commits ahead) |
| [malhal/r8152](https://github.com/malhal/r8152) | `2.13` 1d4e43bacbb8 (0 commits ahead); `2.14` a1293fa0c417 (1 commits ahead); `2.15` 21ce1e82a92c (0 commits ahead); `master` adf32d40c599 (0 commits ahead); `patch-1` 61e284e97c5a (1 commits ahead); `patch-2` 99108ccd7bc7 (1 commits ahead) |
| [jhbsz/r8152](https://github.com/jhbsz/r8152) | `master` a9130c2d19e5 (0 commits ahead) |
| [mbi-png/r8152](https://github.com/mbi-png/r8152) | `2.13` 1d4e43bacbb8 (0 commits ahead); `2.14` a1293fa0c417 (1 commits ahead); `2.15` 21ce1e82a92c (0 commits ahead); `master` eb067ccc0ebd (0 commits ahead) |
| [henrycarrero/r8152](https://github.com/henrycarrero/r8152) | `fix/dsm-upgrade-troubleshooting` 1c45691bdd72 (1 commits ahead); `master` b227e6088a71 (3 commits ahead) |
| [kirinse/r8152](https://github.com/kirinse/r8152) | `2.13` 1d4e43bacbb8 (0 commits ahead); `2.14` a1293fa0c417 (1 commits ahead); `2.15` 21ce1e82a92c (0 commits ahead); `master` a9130c2d19e5 (0 commits ahead) |
| [DARQEnergy/r8152](https://github.com/DARQEnergy/r8152) | `master` cef7dbb3e089 (1 commits ahead) |
| [sellerie98/r8152](https://github.com/sellerie98/r8152) | `2.13` 1d4e43bacbb8 (0 commits ahead); `2.14` a1293fa0c417 (1 commits ahead); `2.15` 21ce1e82a92c (0 commits ahead); `master` a9130c2d19e5 (0 commits ahead) |
| [ezOneWork/r8152](https://github.com/ezOneWork/r8152) | `master` eb067ccc0ebd (0 commits ahead) |
| [svbfromnl/r8152](https://github.com/svbfromnl/r8152) | `master` 477a723a41c3 (0 commits ahead) |
| [007revad/r8152](https://github.com/007revad/r8152) | `master` 997a3a2098e4 (2 commits ahead) |
| [ahembree/r8152](https://github.com/ahembree/r8152) | `master` a9130c2d19e5 (0 commits ahead) |
| [gsnas/r8152](https://github.com/gsnas/r8152) | `master` a9130c2d19e5 (0 commits ahead) |
| [maxromanovsky/r8152](https://github.com/maxromanovsky/r8152) | `docs-update` b1e3370a0c0f (1 commits ahead); `master` a9130c2d19e5 (0 commits ahead) |
| [Cyclonekid/r8152](https://github.com/Cyclonekid/r8152) | `master` 477a723a41c3 (0 commits ahead) |
| [steveduff/r8152](https://github.com/steveduff/r8152) | `2.13` 1d4e43bacbb8 (0 commits ahead); `2.14` a1293fa0c417 (1 commits ahead); `2.15` 21ce1e82a92c (0 commits ahead); `master` eb067ccc0ebd (0 commits ahead); `patch-1` d422900c7894 (1 commits ahead) |
| [Matt-uSk/r8152-backup](https://github.com/Matt-uSk/r8152-backup) | `master` a9130c2d19e5 (0 commits ahead) |
| [chadlwilson/syno-driver-realtek-r8152](https://github.com/chadlwilson/syno-driver-realtek-r8152) | `master` b60f0a733747 (2 commits ahead) |
| [Nossie/usb-r8152](https://github.com/Nossie/usb-r8152) | `master` 477a723a41c3 (0 commits ahead) |
| [HeyMingjin/dsm_r8152](https://github.com/HeyMingjin/dsm_r8152) | `master` 5af0380f021d (1 commits ahead) |

## Primary references

- [DSM7.4 EnvDeploy](https://github.com/SynologyOpenSource/pkgscripts-ng/blob/b26769cbd5f7564e5bc5e4b5e494760292025c44/EnvDeploy)
- [DSM7.4 PkgCreate.py](https://github.com/SynologyOpenSource/pkgscripts-ng/blob/b26769cbd5f7564e5bc5e4b5e494760292025c44/PkgCreate.py)
- [RTD1296 toolkit availability](https://github.com/SynologyOpenSource/pkgscripts-ng/blob/b26769cbd5f7564e5bc5e4b5e494760292025c44/include/toolkit.config)
- [Upstream stability issue](https://github.com/bb-qq/r8152/issues/275)
