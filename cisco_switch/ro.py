"""
.. module:: ro
   :synopsis: Read only functions

.. moduleauthor:: Christoffer Viken <christoffer@viken.me>

Be aware, decorators are signature altering.
"""
from cisco_switch.base import SwitchBase, get_port, get_vlan
from cisco_switch.snmp_funcs import fetch_binds, snmp_next
from pysnmp.proto.rfc1905 import NoSuchInstance

__author__ = 'CVi'
__all__ = ['CiscoROSwitch']


class CiscoROSwitch(SwitchBase):
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

    @get_port
    @fetch_binds('1.3.6.1.2.1.2.2.1.7.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.16.{portindex}',
                 '1.3.6.1.4.1.9.9.46.1.6.1.1.14.{portindex}')
    def trunk_status(self, binds, portindex, port):
        """
        Status of a trunk port

        :param portindex: Index of the port
        :type portindex: int
        :return: True if the port is active and trunk, False otherwise.
        :rtype: boolean
        """
        admin = 0
        is_trunk = 0
        trunk = 0
        for name, val in binds:
            nm_str = name.prettyPrint()
            if '1.3.6.1.2.1.2.2.1.7' in nm_str:
                admin = val
            elif '1.3.6.1.4.1.9.9.46.1.6.1.1.16' in nm_str:
                trunk = val
            elif '1.3.6.1.4.1.9.9.46.1.6.1.1.14' in nm_str:
                is_trunk = val
        return admin == 1 and is_trunk == 1 and trunk != 6

    @get_port
    @fetch_binds('1.3.6.1.2.1.2.2.1.7.{portindex}')
    def admin_status(self, binds, portindex, port):
        """
        Retrieves the admin status of a port.

        :param portindex: Index of the port
        :type portindex: int
        :return: True if port is administratively up, False otherwsie.
        :rtype: boolean
        """
        return binds[0][1] == 1

    @get_port
    @fetch_binds('1.3.6.1.2.1.2.2.1.10.{portindex}')
    def octets_in(self, binds, portindex, port):
        """
        Retrieves number of octets that has come in on the port.

        :param portindex: Index of the port
        :type portindex: int
        :return: Octet (byte) count
        :rtype: int
        """
        return int(binds[0][1])

    @get_port
    @fetch_binds('1.3.6.1.2.1.2.2.1.16.{portindex}')
    def octets_out(self, binds, portindex, port):
        """
        Retrieves number of octets that has come out on the port.

        :param portindex: Index of the port
        :type portindex: int
        :return: Octet (byte) count
        :rtype: int
        """
        return int(binds[0][1])

    def port_names(self):
        """
        Gets all the ports and port IDs on a switch

        :return: Dictionary, port name as key and index as value.
        :rtype: dictionary
        """
        pf = "1.3.6.1.2.1.31.1.1.1.1"
        return {str(val): int(name.prettyPrint()[len(pf)+1:]) for name, val in snmp_next(self.community, self.server, pf)}

    def port_names_regular(self):
        """
        Gets all the ports and port IDs on a switch (without using ifXTable)

        :return: Dictionary, port name as key and index as value.
        :rtype: dictionary
        """
        pf = "1.3.6.1.2.1.2.2.1.2"
        return {str(val): int(str(name.getOid())[len(pf)+1:]) for name, val in snmp_next(self.community, self.server, pf)}

    @get_port
    @fetch_binds('1.3.6.1.4.1.9.9.46.1.6.1.1.4.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.17.{portindex}',
                 '1.3.6.1.4.1.9.9.46.1.6.1.1.18.{portindex}', '1.3.6.1.4.1.9.9.46.1.6.1.1.19.{portindex}')
    def vlans_on_port(self, binds, portindex, port):
        """Get all the vlans on a vlan trunk port.

        :param portindex: Index of the interface/port
        :type portindex: int
        :return: List of all vlanids on a port (if in trunk mode)
        :rtype: list[int]
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

    def get_vlan_names(self, vlandomain=1):
        """
        Get all the vlans on a domain on a switch

        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        :return: Dictionary, vlanid as key, name as value.
        :rtype: dictionary
        """
        pf = "1.3.6.1.4.1.9.9.46.1.3.1.1.4.{vlandomain}".format(vlandomain=vlandomain)
        cleaned = map(lambda x: (x[0].prettyPrint(), x[1]), snmp_next(self.community, self.server, pf))
        return {int(name[name.rfind('.')+1:]): str(val) for name, val in cleaned}

    @get_port
    @fetch_binds("1.3.6.1.2.1.31.1.1.1.18.{portindex}")
    def get_port_alias(self, binds, portindex, port):
        """
        Get the alias of a port

        :param portindex: Index of the interface/port
        :type portindex: int
        :return: Port Alias
        :rtype: basestring
        """
        return str(binds[0][1]) or None

    @get_vlan
    @fetch_binds("1.3.6.1.4.1.9.9.46.1.3.1.1.4.{vlandomain}.{vlanid}")
    def get_vlan_name(self, binds, vlanid, vlandomain, vlan_name=None, vlan=None):
        """
        Get the name of a vlan

        :param vlanid: VlanID, usually the 802.1q tag number.
        :type vlanid: int
        :param vlandomain: vlan domain, usually 1
        :type vlandomain: int
        :return: The name of the vlan
        :rtype: basestring
        """
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
