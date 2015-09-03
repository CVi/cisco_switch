from .ro import *
from .rw import *

__author__ = 'CVi'
__all__ = ['CiscoROSwitch', 'CiscoWOSwitch', 'CiscoSwitch']


class CiscoROSwitch(object):
    """
    Read only switch class
    """
    def __init__(self, community, server):
        """
        :param community: SNMP Community
        :type community: basestring
        :param server: Host (switch) FQDN or IP
        :type server: basestring
        """
        self.community = community
        self.server = server

    def trunk_status(self, portindex):
        """
        Status of a trunk port

        :param portindex: Index of the port
        :type portindex: int
        :return: True if the port is active and trunk, False otherwise.
        :rtype: boolean
        """
        #TODO: Add support for passing a port object.
        return trunk_status(self.community, self.server, portindex=portindex)

    def admin_status(self, portindex):
        """
        Retrieves the admin status of a port.

        :param portindex: Index of the port
        :type portindex: int
        :return: True if port is administratively up, False otherwsie.
        :rtype: boolean
        """
        #TODO: Add support for passing a port object.
        return get_admin_status(self.community, self.server, portindex=portindex)

    def port_names(self):
        """
        Gets all the ports and port IDs on a switch

        :return: Dictionary, port name as key and index as value.
        :rtype: dictionary
        """
        return port_names(self.community, self.server)

    def vlans_on_port(self, portindex):
        """Get all the vlans on a vlan trunk port.

        :param portindex: Index of the interface/port
        :type portindex: int
        :return: List of all vlanids on a port (if in trunk mode)
        :rtype: list[int]
        """
        #TODO: Add support for passing a port object.
        return vlans_on_port(self.community, self.server, portindex=portindex)

    def get_vlan_names(self, vlandomain=1):
        """
        Get all the vlans on a domain on a switch

        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        :return: Dictionary, vlanid as key, name as value.
        :rtype: dictionary
        """
        #TODO: Add support for passing a vlan object.
        return get_vlans(self.community, self.server, vlandomain=vlandomain)

    def get_port_alias(self, portindex):
        """
        Get the alias of a port

        :param portindex: Index of the interface/port
        :type portindex: int
        :return: Port Alias
        :rtype: basestring
        """
        #TODO: Add support for passing a port object.
        return get_port_alias(self.community, self.server, portindex=portindex)

    def get_vlan_name(self, vlanid, vlandomain=1):
        """
        Get the name of a vlan

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        :return: The name of the vlan
        :rtype: basestring
        """
        #TODO: Add support for passing a vlan object.
        return get_vlan_name(self.community, self.server, vlanid=vlanid, vlandomain=vlandomain)

    def get_access_vlan(self, portindex):
        """get_access_vlan(community, server, portindex)
        Get the access vlan on a port

        :param portindex: Index of the interface/port
        :type portindex: int
        :return: The access vlan on the port
        :rtype: int
        """
        get_access_vlan(self.community, self.server, portindex)


class CiscoWOSwitch(object):
    """
    Cisco write/create-only switch class.

    Only has methods that require both read/write or read/create
    """
    def __init__(self, community, server):
        """
        :param community: SNMP Community
        :type community: basestring
        :param server: Host (switch) FQDN or IP
        :type server: basestring
        """
        self.community = community
        self.server = server

    def activate_vlan_on_port(self, portindex, vlanid):
        """
        Activates a vlan on the port

        :param portindex: Index of the interface/port
        :type portindex: int
        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        """
        #TODO: Add support for passing a port object.
        #TODO: Add support for passing a vlan object.
        activate_vlan_on_port(self.community, self.server, portindex=portindex, vlanid=vlanid)

    def deactivate_vlan_on_port(self, portindex, vlanid):
        """
        Deactivates a vlan on the port

        :param portindex: Index of the interface/port
        :type portindex: int
        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        """
        #TODO: Add support for passing a port object.
        #TODO: Add support for passing a vlan object.
        deactivate_vlan_on_port(self.community, self.server, portindex=portindex, vlanid=vlanid)

    def activate_vlans_on_port(self, portindex, vlans):
        """
        Activates a list of vlans on the port

        :param portindex: Index of the interface/port
        :type portindex: int
        :param vlans: List of VlanID, usually the 802.1q tag number.
        :type vlans: list[int]
        """
        #TODO: Add support for passing a port object.
        #TODO: Add support for passing a vlan object.
        activate_vlans_on_port(self.community, self.server, portindex=portindex, vlans=vlans)

    def deactivate_vlans_on_port(self, portindex, vlans):
        """
        Deactivates a list of vlans on the port

        :param portindex: Index of the interface/port
        :type portindex: int
        :param vlans: List of VlanID, usually the 802.1q tag number.
        :type vlans: list[int]
        """
        #TODO: Add support for passing a port object.
        #TODO: Add support for passing a vlan object.
        deactivate_vlans_on_port(self.community, self.server, portindex=portindex, vlans=vlans)

    def wr_mem(self):
        """
        Saves the configuration to flash/disk.
        """
        wr_mem(self.community, self.server)

    def set_port_alias(self, portindex, value):
        """
        Sets the alias of a port

        :param portindex: Index of the interface/port
        :type portindex: int
        :param value: New port alias
        :type value: basestring
        """
        #TODO: Add support for passing a port object.
        set_port_alias(self.community, self.server, portindex=portindex, value=value)

    def activate_port(self, portindex):
        """
        Activates the port

        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        activate_port(self.community, self.server, portindex=portindex)

    def deactivate_port(self, portindex):
        """
        Deactivates the port

        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        deactivate_port(self.community, self.server, portindex=portindex)

    def make_port_trunk(self, portindex):
        """
        Makes the port a trunk, equivalent to
           >> switchport mode trunk

        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        make_port_trunk(self.community, self.server, portindex=portindex)

    def make_port_access(self, portindex):
        """
        Makes the port access, equivalent to
          >> switchport mode access

        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        make_port_access(self.community, self.server, portindex=portindex)

    def create_vlan(self, vlanid, name, vlandomain=1):
        """
        Creates a new vlan
        Raises ValueError if vlan does already exist

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        :param name: Name of vlan
        :type name: basestring
        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        """
        #TODO: Add support for passing a vlan object.
        create_vlan(self.community, self.server, vlanid=vlanid, name=name, vlandomain=vlandomain)

    def rename_vlan(self, vlanid, name, vlandomain=1):
        """
        Renames a vlan
        Raises KeyError if vlan does not exist

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        :param name: New name of vlan
        :type name: basestring
        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        """
        #TODO: Add support for passing a vlan object.
        rename_vlan(self.community, self.server, vlanid=vlanid, name=name, vlandomain=vlandomain)

    def set_access_vlan(self, portindex, vlanid):
        """
        Sets the access vlan on an access port
        raises ValueError if the port is not found in access port table
        raises IOError if the access vlan did not change to the new value

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        #TODO: Add support for passing a vlan object.
        set_access_vlan(self.community, self.server, vlanid=vlanid, portindex=portindex)

    def delete_vlan(self, vlanid, vlandomain=1):
        """
        Delete a vlan
        Raises KeyError if vlan does not exist

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        :param name: Name of vlan
        :type name: basestring
        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        """
        #TODO: Add support for passing a vlan object.
        #TODO: Add support for passing a vlan object.
        delete_vlan(self.community, self.server, vlanid=vlanid, vlandomain=vlandomain)


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
