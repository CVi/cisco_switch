from cisco_switch.base import SwitchBase
from .ro import CiscoROSwitch
from .rw import CiscoWOSwitch
from .meta import CiscoVlan, CiscoPort
from cisco_switch.snmp_funcs import fetch_binds, snmp_next, snmp_get, snmp_set, set_vals

__author__ = 'CVi'
__all__ = ['CiscoROSwitch', 'CiscoWOSwitch', 'CiscoSwitch', 'CiscoVlan', 'CiscoPort']


class CiscoSwitch(CiscoROSwitch, CiscoWOSwitch):
    """
    Cisco Switch class

    Has all methods for manipulating a switch
    """
    def get_ports(self):
        """
        Returns all ports as a map with CiscoPort objects.

        :rtype : map[CiscoPort]
        """
        return map(lambda item: CiscoPort(self, item[1], item[0]), self.port_names().items())

    def get_ports_regular(self):
        """
        Returns all ports as a map with CiscoPort objects.

        :rtype : map[CiscoPort]
        """
        return map(lambda item: CiscoPort(self, item[1], item[0]), self.port_names_regular().items())

    def get_vlans(self, vlandomain=1):
        """
        Returns all Vlans as a map with CiscoVlan objects.

        :rtype : map[CiscoVlan]
        """
        return map(lambda item: CiscoVlan(self, item[0], vlandomain), self.get_vlan_names(vlandomain=vlandomain).items())

    def __str__(self):
        return "<CiscoSwitch: {0}>".format(self.server)