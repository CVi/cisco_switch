"""
.. module:: ro
   :synopsis: Read only functions

.. moduleauthor:: Christoffer Viken <christoffer@viken.me>

Be aware, decorators are signature altering.
"""
__author__ = 'CVi'

from cisco_switch.snmp_funcs import fetch_binds, snmp_next
from pysnmp.proto.rfc1905 import NoSuchInstance

__all__ = ['CiscoROSwitch']


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

    @fetch_binds('1.3.6.1.2.1.2.2.1.7.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.16.{portindex}',
                 '1.3.6.1.4.1.9.9.46.1.6.1.1.14.{portindex}')
    def trunk_status(self, binds, portindex):
        """
        Status of a trunk port

        :param portindex: Index of the port
        :type portindex: int
        :return: True if the port is active and trunk, False otherwise.
        :rtype: boolean
        """
        #TODO: Add support for passing a port object.
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
    def admin_status(self, binds, portindex):
        """
        Retrieves the admin status of a port.

        :param portindex: Index of the port
        :type portindex: int
        :return: True if port is administratively up, False otherwsie.
        :rtype: boolean
        """
        #TODO: Add support for passing a port object.
        return binds[0][1] == 1

    def port_names(self):
        """
        Gets all the ports and port IDs on a switch

        :return: Dictionary, port name as key and index as value.
        :rtype: dictionary
        """
        pf = "1.3.6.1.2.1.31.1.1.1.1"
        return {str(val): int(name.prettyPrint()[len(pf)+1:]) for name, val in snmp_next(self.community, self.server, pf)}

    @fetch_binds('1.3.6.1.4.1.9.9.46.1.6.1.1.4.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.17.{portindex}',
                 '1.3.6.1.4.1.9.9.46.1.6.1.1.18.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.19.{portindex}')
    def vlans_on_port(self, binds, portindex):
        """Get all the vlans on a vlan trunk port.

        :param portindex: Index of the interface/port
        :type portindex: int
        :return: List of all vlanids on a port (if in trunk mode)
        :rtype: list[int]
        """
        #TODO: Add support for passing a port object.
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

    def get_vlan_names(self, vlandomain=1):
        """
        Get all the vlans on a domain on a switch

        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        :return: Dictionary, vlanid as key, name as value.
        :rtype: dictionary
        """
        #TODO: Add support for passing a vlan object.
        pf = "1.3.6.1.4.1.9.9.46.1.3.1.1.4.{vlandomain}".format(vlandomain=vlandomain)
        cleaned = map(lambda x: (x[0].prettyPrint(), x[1]), snmp_next(self.community, self.server, pf))
        return {int(name[name.rfind('.')+1:]): str(val) for name, val in cleaned}

    @fetch_binds("1.3.6.1.2.1.31.1.1.1.18.{portindex}")
    def get_port_alias(self, binds, portindex):
        """
        Get the alias of a port

        :param portindex: Index of the interface/port
        :type portindex: int
        :return: Port Alias
        :rtype: basestring
        """
        #TODO: Add support for passing a port object.
        return str(binds[0][1]) or None

    @fetch_binds("1.3.6.1.4.1.9.9.46.1.3.1.1.4.{vlandomain}.{vlanid}")
    def get_vlan_name(self, binds, vlanid, vlandomain=1):
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
        return str(binds[0][1])

    @fetch_binds('1.3.6.1.4.1.9.9.68.1.2.2.1.2.{portindex}')
    def get_access_vlan(self, binds, portindex):
        """get_access_vlan(community, server, portindex)
        Get the access vlan on a port

        :param portindex: Index of the interface/port
        :type portindex: int
        :return: The access vlan on the port
        :rtype: int
        """
        return int(binds[0][1]) if type(binds[0][1]) != NoSuchInstance else None
