from .ro import CiscoROSwitch
from .rw import CiscoWOSwitch
from cisco_switch.snmp_funcs import fetch_binds, snmp_next, snmp_get, snmp_set, set_vals

__author__ = 'CVi'
__all__ = ['CiscoROSwitch', 'CiscoWOSwitch', 'CiscoSwitch']


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

    def get_vlans(self, vlandomain=1):
        """
        Returns all Vlans as a map with CiscoVlan objects.

        :rtype : map[CiscoVlan]
        """
        return map(lambda item: CiscoVlan(self, item[0], vlandomain), self.get_vlan_names(vlandomain=vlandomain).items())

    def __str__(self):
        return "<CiscoSwitch: {0}>".format(self.server)


class CiscoPort(object):
    """
    Cisco port class

    Methods for manipulating a particular port.
    Wraps around switch-methods and keeps track of the ID for you.
    """
    def __init__(self, switch, portindex, name):
        """
        :param switch: Switch port belongs to
        :type switch: CiscoSwitch
        :param portindex: Index of the interface/port
        :type portindex: int
        :param name: Port name
        :type name: basestring
        """
        self.switch = switch
        self.portindex = portindex
        self.name = name

    def trunk_status(self):
        """
        Status trunk on port

        :return: True if the port is active and trunk, False otherwise.
        :rtype: boolean
        """
        return self.switch.trunk_status(self.portindex)

    def admin_status(self):
        """
        Retrieves the admin status of the port.

        :return: True if port is administratively up, False otherwsie.
        :rtype: boolean
        """
        return self.switch.admin_status(self.portindex)

    def vlans(self):
        """Get all the vlans on the trunk

        :return: List of all vlanids on a port (if in trunk mode)
        :rtype: list[int]
        """
        return self.switch.vlans_on_port(self.portindex)

    def get_alias(self):
        """
        Get the alias of the port

        :return: Port Alias
        :rtype: basestring
        """
        return self.switch.get_port_alias(self.portindex)

    def activate_vlan(self, vlanid):
        """
        Activates a vlan on the port

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        """
        #TODO: Add support for passing a vlan object.
        self.switch.activate_vlan_on_port(self.portindex, vlanid)

    def deactivate_vlan(self, vlanid):
        """
        Deactivates a vlan on the port

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        """
        #TODO: Add support for passing a vlan object.
        self.switch.deactivate_vlan_on_port(self.portindex, vlanid)

    def activate_vlans(self, vlans):
        """
        Activates a list of vlans on the port

        :param vlans: List of VlanID, usually the 802.1q tag number.
        :type vlans: list[int]
        """
        #TODO: Add support for passing a vlan object.
        self.switch.activate_vlans_on_port(self.portindex, vlans)

    def deactivate_vlans(self, vlans):
        """
        Deactivates a list of vlans on the port

        :param vlans: List of VlanID, usually the 802.1q tag number.
        :type vlans: list[int]
        """
        #TODO: Add support for passing a vlan object.
        self.switch.deactivate_vlans_on_port(self.portindex, vlans)

    def set_alias(self, value):
        """
        Sets the alias of the port

        :param value: New port alias
        :type value: basestring
        """
        self.switch.set_port_alias(self.portindex, value)

    def activate(self):
        """
        Activates the port
        """
        self.switch.activate_port(self.portindex)

    def deactivate(self):
        """
        Deactivates the port
        """
        self.switch.deactivate_port(self.portindex)

    def make_trunk(self):
        """
        Makes the port a trunk, equivalent to
           >> switchport mode trunk
        """
        self.switch.make_port_trunk(self.portindex)

    def make_access(self):
        """
        Makes the port access, equivalent to
          >> switchport mode access
        """
        self.switch.make_port_access(self.portindex)

    def get_access_vlan(self):
        """get_access_vlan(community, server, portindex)
        Get the access vlan on a port

        :return: The access vlan on the port
        :rtype: int
        """
        self.switch.get_access_vlan(self.portindex)

    def set_access_vlan(self, vlanid):
        """
        Sets the access vlan on an access port
        raises ValueError if the port is not found in access port table
        raises IOError if the access vlan did not change to the new value

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        """
        #TODO: Add support for passing a vlan object.
        self.switch.set_access_vlan(self.portindex, vlanid)


class CiscoVlan(object):
    """
    Cisco VLAN class

    Methods for manipulating vlans
    """
    @staticmethod
    def create(switch, vlanid, name, vlandomain=1):
        """
        Creates a vlan on the switch and returns a new vlan object

        :param switch: Switch to create vlan on
        :type switch: CiscoSwitch
        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        :param name: Name of new vlan
        :type name: basestring
        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        :return: Object representation of the new vlan
        :rtype : CiscoVlans
        """
        switch.create_vlan(vlanid, name, vlandomain=vlandomain)
        return CiscoVlan(switch, vlanid, vlandomain=vlandomain)

    def __init__(self, switch, vlanid, vlandomain=1):
        """
        :param switch: Switch port belongs to
        :type switch: CiscoSwitch
        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        """
        self.switch = switch
        self.id = vlanid
        self.vlandomain = vlandomain

    def get_name(self):
        """
        Get vlan name

        :return: Name of the vlan
        :rtype :  basestring
        """
        return self.switch.get_vlan_name(self.id, vlandomain=self.vlandomain)

    def rename(self, name):
        """
        Renames a vlan
        Raises KeyError if vlan does not exist

        :param name: New name of vlan
        :type name: basestring
        """
        self.switch.rename_vlan(self.id, name, vlandomain=self.vlandomain)
