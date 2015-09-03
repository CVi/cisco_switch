"""
.. module:: ro
   :synopsis: Read only functions

.. moduleauthor:: Christoffer Viken <christoffer@viken.me>

Be aware, decorators are signature altering.
Only community and server are guaranteed to be positional.
"""
__author__ = 'CVi'

from cisco_switch.snmp_funcs import fetch_binds, snmp_next
from pysnmp.proto.rfc1905 import NoSuchInstance

__all__ = ['trunk_status', 'get_admin_status', 'port_names', 'vlans_on_port', 'get_vlans', 'get_port_alias',
           'get_access_vlan', 'get_vlan_name']


@fetch_binds('1.3.6.1.2.1.2.2.1.7.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.16.{portindex}',
             '1.3.6.1.4.1.9.9.46.1.6.1.1.14.{portindex}')
def trunk_status(community, server, binds, portindex):
    """trunk_status(community, server, portindex)
    Checks if the port is a trunk port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :return: True if the port is active and trunk, False otherwise.
    """
    for name, val in binds:
        nm_str = name.prettyPrint()
        if '1.3.6.1.2.1.2.2.1.7' in nm_str:
            admin = val
        elif '1.3.6.1.4.1.9.9.46.1.6.1.1.16' in nm_str:
            trunk = val
        elif '1.3.6.1.4.1.9.9.46.1.6.1.1.14' in nm_str:
            is_trunk = val
    return admin == 1 and is_trunk == 1 and trunk != 6


@fetch_binds('1.3.6.1.2.1.2.2.1.7.{portindex}')
def get_admin_status(community, server, binds, portindex):
    """get_admin_status(community, server, portindex)
    Get the Admin Status of a port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :return: True if port is administratively up, False otherwsie.
    """
    return binds[0][1] == 1


def port_names(community, server):
    """
    Gets all the ports and port IDs on a switch

    :param community: SNMP Community
    :param server: Host (switch)
    :return: Dictionary, port name as key and index as value.
    """
    pf = "1.3.6.1.2.1.31.1.1.1.1"
    return {str(val): int(name.prettyPrint()[len(pf)+1:]) for name, val in snmp_next(community, server, pf)}

@fetch_binds('1.3.6.1.4.1.9.9.46.1.6.1.1.4.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.17.{portindex}',
             '1.3.6.1.4.1.9.9.46.1.6.1.1.18.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.19.{portindex}')
def vlans_on_port(community, server, binds, portindex):
    """vlans_on_port(community, server, portindex)
    Get all the vlans on a vlan trunk port.

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :return: List of all vlanids on a port (if in trunk mode)
    :trype list[int]
    """
    vlans = []
    pf = "1.3.6.1.4.1.9.9.46.1.6.1.1"
    mappings = {'4.': 0, '17': 1024, '18': 2048, '19': 3072}
    for name, val in binds:
        nm_str = name.prettyPrint()
        val_str = val.prettyPrint()
        pr_str = nm_str[len(pf)+1:][:2]

        v = mappings.get(pr_str, -1024)

        if val_str == "b''" or val_str == "No Such Instance currently exists at this OID":
            continue
        l = val_str[2:].ljust(256, '0')
        b = bin(int(l, 16))[2:].zfill(len(l)*4)
        for i in range(len(b)):
            if b[i] == "1":
                vlans.append(v+i)
    return vlans

def get_vlans(community, server, vlandomain):
    """
    Get all the vlans on a domain on a switch

    :param community: SNMP Community
    :param server: Host (switch)
    :param vlandomain: vlan domain, usually 1
    :return: Dictionary, vlanid as key, name as value.
    """
    pf = "1.3.6.1.4.1.9.9.46.1.3.1.1.4.{vlandomain}".format(vlandomain=vlandomain)
    cleaned = map(lambda x: (x[0].prettyPrint(), x[1]), snmp_next(community, server, pf))
    return {int(name[name.rfind('.')+1:]): str(val) for name, val in cleaned}

@fetch_binds("1.3.6.1.2.1.31.1.1.1.18.{portindex}")
def get_port_alias(community, server, portindex, binds):
    """get_port_alias(community, server, portindex)
    Get the alias of a port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :return: Port Alias
    """
    return str(binds[0][1]) or None

@fetch_binds('1.3.6.1.4.1.9.9.68.1.2.2.1.2.{portindex}')
def get_access_vlan(community, server, binds, portindex):
    """get_access_vlan(community, server, portindex)
    Get the access vlan on a port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :return: The access vlan on the port
    """
    return int(binds[0][1]) if type(binds[0][1]) != NoSuchInstance else None

@fetch_binds("1.3.6.1.4.1.9.9.46.1.3.1.1.4.{vlandomain}.{vlanid}")
def get_vlan_name(community, server, binds, vlanid, vlandomain):
    """get_vlan_name(community, server, vlanid, vlandomain)
    Get the name of a vlan

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :param vlanid: VlanID, usually the 802.1q tag number.
    :param vlandomain: vlan domain, usually 1
    :return: The name of the vlan
    """
    return str(binds[0][1])
