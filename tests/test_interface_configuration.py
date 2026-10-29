#!/usr/bin/env python3
"""Exercise real lifecycle functions with network commands and config files mocked."""
import subprocess
import unittest
from pathlib import Path
SOURCE = (Path(__file__).resolve().parents[1] / "scripts/start-stop-status").read_text()
FUNCTIONS = SOURCE.split('mkdir -p "${log_root}"', 1)[0]
MOCKS = r"""
set +x
package_root=/mock/r8152
script_root=/mock/r8152/scripts
driver_name=r8152
function [ {
    if [[ "$1" == '!' ]]; then
        shift
        if [ "$@" ]; then return 1; else return 0; fi
    fi
    case "$1:$2" in
        -e:/sys/class/net/*/device/driver) return 0 ;;
        -f:/etc/sysconfig/network-scripts/ifcfg-eth1) return 0 ;;
        -r:/etc/sysconfig/network-scripts/ifcfg-eth1) return 0 ;;
        -f:*|-r:*|-e:*) return 1 ;;
    esac
    builtin [ "$@"
}
ls() {
    if [[ "$*" == /sys/class/net ]]; then
        echo 'eth1 eth2'
    elif [[ "$*" == *eth0/device/driver ]]; then
        echo /sys/bus/platform/drivers/r8169
    else
        echo /sys/bus/usb/drivers/r8152
    fi
}
source() {
    if [[ "$1" == /etc/VERSION ]]; then
        buildnumber=90080
    elif [[ "$1" == *ifcfg-eth1 ]]; then
        BOOTPROTO=static
        IPADDR=192.0.2.10
        NETMASK=255.255.255.0
    else
        echo "Unexpected source: $1" >&2
        return 1
    fi
}
ifconfig() { echo "IFCONFIG $*"; }
synonet() { echo "DHCP $*"; }
netstat() { :; }
ip() { echo default; }
is_ovs_enable() { return 1; }
"""
class InterfaceTests(unittest.TestCase):
    def run_case(self, command):
        result = subprocess.run(["bash", "-c", FUNCTIONS + MOCKS + command],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout
    def test_scan_configures_both_usb_interfaces(self):
        output = self.run_case("set_interfaces up")
        self.assertIn("IFCONFIG eth1 inet 192.0.2.10 netmask 255.255.255.0", output)
        self.assertIn("IFCONFIG eth2 up", output)
        self.assertIn("DHCP --dhcp eth2", output)
        self.assertNotIn("IFCONFIG eth2 inet", output)
    def test_static_config_does_not_leak_between_calls(self):
        output = self.run_case("set_interfaces up eth1; set_interfaces up eth2")
        self.assertIn("DHCP --dhcp eth2", output)
        self.assertNotIn("IFCONFIG eth2 inet", output)
    def test_explicit_target_is_respected(self):
        output = self.run_case("set_interfaces up eth2")
        self.assertIn("DHCP --dhcp eth2", output)
        self.assertNotIn("IFCONFIG eth1", output)
    def test_config_helper_keeps_callers_selection(self):
        output = self.run_case('target_interface_name=original; apply_if_config eth1; echo "TARGET=$target_interface_name"')
        self.assertIn("TARGET=original", output)
    def test_syntax(self):
        result = subprocess.run(["bash", "-n"], input=SOURCE, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
if __name__ == "__main__":
    unittest.main()
