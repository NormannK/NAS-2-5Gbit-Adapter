#!/usr/bin/env python3
"""Read-only collector tests; mocks avoid requiring a NAS, root or real sysfs."""
import subprocess
import unittest
from pathlib import Path

SOURCE = (Path(__file__).resolve().parents[1] / "scripts" / "diagnose-rtd1296").read_text()
MOCKS = r"""
function [ {
    case "$1:$2" in
        -d:/sys/class/net/eth1) return 0 ;;
        -d:/sys/class/net/missing) return 1 ;;
        -r:*) return 1 ;;
    esac
    builtin [ "$@"
}
readlink() {
    case "$*" in
        *device/driver) echo /sys/bus/usb/drivers/r8152 ;;
        *device) echo /sys/devices/platform/xhci/usb3/3-1/3-1:1.0 ;;
        *) return 1 ;;
    esac
}
ethtool() { printf 'MOCK ethtool %s\n' "$*"; }
date() { echo MOCK_DATE; }
uname() { echo MOCK_KERNEL; }
"""

class CollectorTests(unittest.TestCase):
    def run_collector(self, args, mocks=MOCKS):
        return subprocess.run(["bash", "-c", mocks + "\n" + SOURCE, "diagnose", *args],
                              capture_output=True, text=True)
    def test_shell_syntax(self):
        for shell in ("sh", "bash"):
            result = subprocess.run([shell, "-n"], input=SOURCE, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
    def test_invalid_arguments(self):
        for args in ([], ["eth1", "extra"], ["../eth0"], ["eth1;reboot"], [""]):
            result = self.run_collector(args)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("MOCK ethtool", result.stdout)
    def test_absent_interface(self):
        result = self.run_collector(["missing"])
        self.assertEqual(result.returncode, 1)
    def test_builtin_ethernet_rejected(self):
        result = self.run_collector(["eth1"], MOCKS.replace("drivers/r8152", "drivers/r8169"))
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("MOCK ethtool", result.stdout)
    def test_success_with_unavailable_optional_files(self):
        result = self.run_collector(["eth1"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("USB-scatter-gather: unavailable", result.stdout)
        calls = [line for line in result.stdout.splitlines() if line.startswith("MOCK ethtool")]
        self.assertEqual(calls, ["MOCK ethtool -i eth1", "MOCK ethtool eth1",
                                "MOCK ethtool -k eth1", "MOCK ethtool --show-eee eth1",
                                "MOCK ethtool -S eth1"])
    def test_missing_ethtool(self):
        mocks = MOCKS + '\ncommand() { return 1; }\n'
        result = self.run_collector(["eth1"], mocks)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Missing optional tool: ethtool", result.stdout)
    def test_unsupported_ethtool_options(self):
        result = self.run_collector(["eth1"], MOCKS + '\nethtool() { return 1; }\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Command unavailable or unsupported", result.stdout)

if __name__ == "__main__":
    unittest.main()
