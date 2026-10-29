# Experimental linear USB transmit path on DS220j

Status: unvalidated; draft for DSM 7.4 RTD1296 builds and RTL8156B testing.
This is not a confirmed fix for upstream issue #275.

## What changes

The read-only module parameter `force_linear_tx` defaults to false.
When explicitly set to 1 during module loading, it makes the existing
`rtl_hc_support_sg()` gate reject scatter-gather USB transmission.
Both initial probe and the existing `rtl_adv/sg_en` enable path consult
that gate. The existing linear-buffer transmit path is used instead.
All adapters bound to this module are affected, not just one interface.

No automatic RTD1296 detection or permanent quirk is added because evidence
does not yet justify changing the default for every RTD1296 user.
Ethernet speed negotiation and ordinary TSO/GSO settings are unchanged.
This internal USB choice is distinct from `ethtool -K ... sg off`.
Copying into linear buffers may increase CPU usage or reduce throughput,
particularly on the DS220j.

The parameter is load-time only (0444). It cannot be toggled during traffic.
The existing sysfs enable request is rejected with EINVAL while forced linear
mode is active; disabling SG remains allowed.

## Build and test gate

Do not use an upstream release SPK to test this option: it does not contain
the parameter. Build this branch using the Synology RTD1296 DSM 7.4 toolkit,
retain the original package, and verify kernel version magic against the NAS.
This PR has not been compiled against that SDK or run on a NAS.

Use built-in Ethernet for management. Stop the driver package and ensure the
old module is unloaded before loading the newly built module with
`force_linear_tx=1`. The package start script uses `insmod` directly, so a
modprobe.d setting alone will NOT enable this experiment. No startup script
is changed here and no persistent configuration is installed.

Once the new module is loaded and the USB interface is configured, verify:

```sh
cat /sys/module/r8152/parameters/force_linear_tx
cat /sys/class/net/eth1/rtl_adv/sg_en
```

Replace eth1 with the verified USB interface name. Expected values are Y and
disable. If either is absent or different, the experiment is not active.
Do not run the package's normal start operation over an already loaded module.

Compare default versus forced-linear mode using the same MTU 1500, USB port,
cable and client. Run sustained TCP in both directions and SMB checksum tests,
record CPU usage, throughput, stalls, and before/after driver counters.
A negotiated 2500 Mb/s link alone is not success.

## Rollback

Through built-in Ethernet, stop USB traffic and unload the experimental module,
then restart the original package/module without the parameter. If the
experimental module replaced a packaged file, reinstall the original matching
SPK first. Verify the interface uses the baseline driver and settings.
Do not force-unload a stuck module; use a controlled NAS reboot if necessary.

## Review scope

The change reuses the existing ASMedia-controller eligibility gate but does not
claim that the RTD1296 has the same defect. Default false preserves that gate's
existing controller decisions. No EEE, global USB power, MTU, routing, VLAN,
automatic recovery, or watchdog policy changes are included.
