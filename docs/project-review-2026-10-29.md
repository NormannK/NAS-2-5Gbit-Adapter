# Follow-up review: DS220j and related projects

Reviewed 2026-10-29, after fork PRs #1–#5 were merged.

## Confirmed lifecycle bugs

The startup functions share Bash variables. apply_if_config overwrites the
caller's target_interface_name, so an untargeted scan can stop configuring USB
interfaces after its first successful configuration. Source-loaded BOOTPROTO,
IPADDR, NETMASK and OVS_VLAN_ID can also persist into the next interface.
The proposed fix scopes helper variables locally and loads network configuration
inside a subshell with those keys unset. Both ordinary and OVS configuration
blocks receive that isolation. No failover or bonding behavior is added.

Mocked regression tests reproduce the failures and check interface selection,
static-to-DHCP transitions and Bash parsing. Real DSM and OVS behavior still need
validation.

## Related projects and applicability

| Project | Relevance |
| --- | --- |
| [awesometic/realtek-r8152-dkms](https://github.com/awesometic/realtek-r8152-dkms) | Linux DKMS/deb packaging; latest observed release uses Realtek 2.22.1, the same vendor version as this fork. Useful for future source tracking, not a DSM-installable package or demonstrated RTD1296 fix. |
| [wget/realtek-r8152-linux](https://github.com/wget/realtek-r8152-linux) | Distribution-oriented vendor source mirror. Inspected driver reports 2.22.1. Do not replace DSM compatibility changes without a full diff and SDK test. |
| [bb-qq/aqc111](https://github.com/bb-qq/aqc111) | Synology packaging for Aquantia AQC111U adapters; different hardware from the user's RTL8156B. Upstream RTD1296 issue reports also mention this driver, so it is not evidence that changing chip vendors solves the NAS problem. |
| [skysolf/r8152_dsm7.2](https://github.com/skysolf/r8152_dsm7.2) | Older DSM packaging focused on apollolake/DS918+; not a DS220j/DSM7.4 replacement. |
| [interoperable/synology-r8152](https://github.com/interoperable/synology-r8152) | Similar Synology driver packaging. No independently verified DS220j fix identified. |
| [SynologyOpenSource/pkgscripts-ng](https://github.com/SynologyOpenSource/pkgscripts-ng) | Official platform build system already used by this fork's container tooling. |
| [chadlwilson/syno-driver-realtek-r8152](https://github.com/chadlwilson/syno-driver-realtek-r8152) | RTD1296/DSM7.4 build approach already adapted in fork PR #5. |

Searches covered DS220j/RTD1296 fixes, Synology USB Ethernet drivers,
Realtek Linux/DKMS drivers and CDC-NCM alternatives. Search results and README
claims are not hardware validation. No newer vendor version or proven RTD1296
repair was identified in the primary sources inspected.

## Remaining priorities

1. Build the merged source using the RTD1296 DSM7.4 SDK and verify module vermagic.
2. Give fork builds a distinct package/driver identity so they cannot be mistaken
   for the upstream SPK. INFO.sh currently still identifies the upstream distributor.
3. Integrate explicit activation/rollback of force_linear_tx with package startup.
   The merged parameter remains disabled by default and direct insmod does not
   consume a modprobe.d setting.
4. Validate reboot, USB detach/reconnect, sustained bidirectional TCP and SMB
   checksums on the actual NAS.
5. Keep failover separate: carrier-only monitoring may miss transmit stalls and
   USB bond restoration has upstream lifecycle issues.

The official SDK build and hardware validation remain outstanding. The current
execution workspace has no free disk space for the SDK/container build.
