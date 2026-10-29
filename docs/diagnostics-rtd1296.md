# Read-only DS220j / RTL8156B snapshots

Run from a checkout with a POSIX shell on the NAS:

```sh
sh scripts/diagnose-rtd1296 eth1
```

Replace eth1 with the USB adapter's interface name. When included in a rebuilt
SPK, the collector is also available under
`/var/packages/r8152/scripts/diagnose-rtd1296`.
The upstream SPK does not include this new script.

The script verifies the interface binds to r8152 and only reads data.
It collects DSM/kernel identity, USB identifiers/revision/speed and controller
path, internal USB SG state, link/offload/EEE settings and packet/error counters.
Optional missing files and unsupported ethtool requests are reported without
aborting the rest of the snapshot. It does not reset the adapter or alter settings.

Capture output immediately before and after the same sustained transfer,
including NAS-to-client traffic. Compare TX/RX byte and error counters alongside
the benchmark; snapshots alone do not establish whether a stalled USB request
completed. Kernel TX submission/completion logs may be needed for deeper analysis.

No IP configuration, MAC address query, USB serial, or kernel log dump is collected.
Review output before posting it because tool/driver-specific output may vary.
Run as an ordinary user first; elevated privileges may be required for some
driver statistics. Tests run on a development host with:

```sh
python3 tests/test_diagnose_rtd1296.py
```

Tests mock sysfs/ethtool and do not validate real DSM behavior.
