# Software timestamp capability reporting

Ported from [wget/realtek-r8152-linux commit 48b2c2573525e20d5038a785ab62dab4be67b19f](https://github.com/wget/realtek-r8152-linux/commit/48b2c2573525e20d5038a785ab62dab4be67b19f)
by Martin Pecka, which references
[Linux a8e846b8d93de748485653dd8a6a8efd8f5d7613](https://github.com/torvalds/linux/commit/a8e846b8d93de748485653dd8a6a8efd8f5d7613).

Registers the standard ethtool_op_get_ts_info callback for kernels >= 3.5.
The callback and matching ethtool_ops signature were verified in Linux v4.4's
include/linux/ethtool.h, relevant to the RTD1296 kernel family.
The collector now queries ethtool -T and tolerates missing/unsupported tooling.

This reports generic software timestamp capabilities. It does not add hardware
PTP timestamping, increase throughput, repair RTD1296 stalls or change SG policy.

Validation performed: source-shape assertions ensure one callback and one
collector query; the existing mocked collector expectations were updated.
Execution of the tests and DSM SDK compilation were blocked by workspace disk
exhaustion. This change needs an SDK build and a real ethtool -T query on the NAS.
