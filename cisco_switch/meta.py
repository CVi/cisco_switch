from cisco_switch.base import SwitchBase

__author__ = 'CVi'

class CiscoPort(SwitchBase):
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
        return self.switch.trunk_status(port=self)

    def admin_status(self):
        """
        Retrieves the admin status of the port.

        :return: True if port is administratively up, False otherwsie.
        :rtype: boolean
        """
        return self.switch.admin_status(port=self)

    def octets_in(self):
        """
        Retrieves number of octets that has come in on the port.

        :return: Octet (byte) count
        :rtype: boolean
        """
        return self.switch.octets_in(port=self)

    def octets_out(self):
        """
        Retrieves number of octets that has come out on the port.

        :return: Octet (byte) count
        :rtype: boolean
        """
        return self.switch.octets_out(port=self)

    def vlans(self):
        """Get all the vlans on the trunk

        :return: List of all vlanids on a port (if in trunk mode)
        :rtype: list[int]
        """
        return self.switch.vlans_on_port(port=self)

    def get_alias(self):
        """
        Get the alias of the port

        :return: Port Alias
        :rtype: basestring
        """
        return self.switch.get_port_alias(port=self)

    def activate_vlan(self, vlanid=0, vlan=None):
        """
        Activates a vlan on the port

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        """
        self.switch.activate_vlan_on_port(port=self, vlanid=vlanid, vlan=vlan)

    def deactivate_vlan(self, vlanid=0, vlan=None):
        """
        Deactivates a vlan on the port

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        """
        self.switch.deactivate_vlan_on_port(port=self, vlanid=vlanid, vlan=vlan)

    def activate_vlans(self, vlans=None):
        """
        Activates a list of vlans on the port

        :param vlans: List of VlanID, usually the 802.1q tag number.
        :type vlans: list[int]
        """
        self.switch.activate_vlans_on_port(port=self, vlans=vlans)

    def deactivate_vlans(self, vlans):
        """
        Deactivates a list of vlans on the port

        :param vlans: List of VlanID, usually the 802.1q tag number.
        :type vlans: list[int]
        """
        self.switch.deactivate_vlans_on_port(port=self, vlans=vlans)

    def set_alias(self, value):
        """
        Sets the alias of the port

        :param value: New port alias
        :type value: basestring
        """
        self.switch.set_port_alias(port=self, value=value)

    def activate(self):
        """
        Activates the port
        """
        self.switch.activate_port(port=self)

    def deactivate(self):
        """
        Deactivates the port
        """
        self.switch.deactivate_port(port=self)

    def make_trunk(self):
        """
        Makes the port a trunk, equivalent to
           >> switchport mode trunk
        """
        self.switch.make_port_trunk(port=self)

    def make_access(self):
        """
        Makes the port access, equivalent to
          >> switchport mode access
        """
        self.switch.make_port_access(port=self)

    def get_access_vlan(self):
        """get_access_vlan(community, server, portindex)
        Get the access vlan on a port

        :return: The access vlan on the port
        :rtype: int
        """
        self.switch.get_access_vlan(port=self)

    def set_access_vlan(self, vlanid=0, vlan=None):
        """
        Sets the access vlan on an access port
        raises ValueError if the port is not found in access port table
        raises IOError if the access vlan did not change to the new value

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        """
        self.switch.set_access_vlan(port=self, vlanid=vlanid, vlan=vlan)


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
        return self.switch.get_vlan_name(vlan=self, vlandomain=self.vlandomain)

    def rename(self, name):
        """
        Renames a vlan
        Raises KeyError if vlan does not exist

        :param name: New name of vlan
        :type name: basestring
        """
        self.switch.rename_vlan(vlan=self, name=name, vlandomain=self.vlandomain)
