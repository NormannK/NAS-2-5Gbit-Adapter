# ASUS USB mode selection

Ported from [wget/realtek-r8152-linux commit 44b51ee072b0ebc2f6ce31b4982e02b72ce7399f](https://github.com/wget/realtek-r8152-linux/commit/44b51ee072b0ebc2f6ce31b4982e02b72ce7399f),
by Hyacinthe Cartiaux.

Adds the vendor-mode configuration rule for USB ID 0b05:1976, already supported
by the driver. It follows the existing guarded USB add-event rules and changes
configuration only when it differs from mode 1. It is not a generic RTL8156B fix.

If the adapter identifies as 0bda:8156, the existing Realtek rule already covers
it and this ASUS rule has no effect. Check the collector's actual USB ID.

Validation: verified matching driver ID, one new exact rule, no existing ASUS rule,
and preservation of existing rules and event guards. udev execution, SPK build
and hardware enumeration are untested; workspace disk exhaustion prevents them.
On NAS, verify the package installs these rules and inspect normal reboot enumeration.
