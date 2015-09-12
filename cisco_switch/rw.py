"""
.. module:: rw
   :synopsis: Read/write and read/create functions

.. moduleauthor:: Christoffer Viken <christoffer@viken.me>
"""
import random
from pysnmp.proto.rfc1902 import OctetString
import time
from pysnmp.proto.rfc1905 import NoSuchInstance
from cisco_switch.snmp_funcs import snmp_next, snmp_get, snmp_set, set_vals

__author__ = 'CVi'
__all__ = ['CiscoWOSwitch']


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

    def _meta_vlan(self, portindex, status, vlanid=0, vlan_list=[]):
        """
        Meta function for updating vlan on a port

        :param portindex: Index of the interface/port
        :param vlanid: VlanID, usually the 802.1q tag number.
        :param status: New vlan status as a 0/1 string.
        :param vlan_list: if vlanid is 0, you can bulk set using this.
        """
        multi = False
        if vlanid == 0:
            vlanid = min(vlan_list) if len(vlan_list) > 0 else 0
            multi = True
            if len(vlan_list) == 0:
                return
        if vlanid < 0 or vlanid >= 4096:
            raise ValueError("Invalid VLAN")
        elif vlanid <= 1023:
            oid = "1.3.6.1.4.1.9.9.46.1.6.1.1.4.%i" % portindex
            diff = 0
        elif vlanid <= 2047:
            oid = "1.3.6.1.4.1.9.9.46.1.6.1.1.17.%i" % portindex
            diff = -1024
        elif vlanid <= 3071:
            oid = "1.3.6.1.4.1.9.9.46.1.6.1.1.18.%i" % portindex
            diff = -2048
        else:
            oid = "1.3.6.1.4.1.9.9.46.1.6.1.1.19.%i" % portindex
            diff = -3072

        ((a, serial), (b, vlans)) = snmp_get(self.community, self.server, "1.3.6.1.4.1.9.9.46.1.6.2.0", oid)
        val_str = vlans.prettyPrint()
        if val_str == "b''":
            val_str = "0000"
        l = val_str[2:].ljust(256, '0')
        b = list(bin(int(l, 16))[2:].zfill(len(l)*4))
        if not multi:
            b[vlanid+diff] = status
        else:
            for v in vlan_list:
                if 0 <= v+diff <= 1023:
                    b[v+diff] = status
        b = "".join(b)
        os = OctetString(binValue=b)

        snmp_set(self.community, self.server, ("1.3.6.1.4.1.9.9.46.1.6.2.0", serial), (oid, os))

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
        self._meta_vlan(portindex=portindex, vlanid=vlanid, status="1")

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
        self._meta_vlan(portindex=portindex, vlanid=vlanid, status="0")

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
        self._meta_vlan(self.community, self.server, portindex, "1", vlan_list=[v for v in vlans if 0 < v <= 1023])
        self._meta_vlan(self.community, self.server, portindex, "1", vlan_list=[v for v in vlans if 1023 < v <= 2047])
        self._meta_vlan(self.community, self.server, portindex, "1", vlan_list=[v for v in vlans if 2047 < v <= 3071])
        self._meta_vlan(self.community, self.server, portindex, "1", vlan_list=[v for v in vlans if 3071 < v <= 4095])

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
        self._meta_vlan(self.community, self.server, portindex, "0", vlan_list=[v for v in vlans if 0 < v <= 1023])
        self._meta_vlan(self.community, self.server, portindex, "0", vlan_list=[v for v in vlans if 1023 < v <= 2047])
        self._meta_vlan(self.community, self.server, portindex, "0", vlan_list=[v for v in vlans if 2047 < v <= 3071])
        self._meta_vlan(self.community, self.server, portindex, "0", vlan_list=[v for v in vlans if 3071 < v <= 4095])

    def wr_mem(self):
        """
        Saves the configuration to flash/disk.
        """
        key = random.randint(1, 255)
        snmp_set(self.community, self.server, ('1.3.6.1.4.1.9.9.96.1.1.1.1.3.%i' % key, 4),
                 ('1.3.6.1.4.1.9.9.96.1.1.1.1.4.%i' % key, 3), ('1.3.6.1.4.1.9.9.96.1.1.1.1.14.%i' % key, 4))

    @set_vals('1.3.6.1.2.1.31.1.1.1.18.{portindex}')
    def set_port_alias(self, portindex, value):
        """
        Sets the alias of a port

        :param portindex: Index of the interface/port
        :type portindex: int
        :param value: New port alias
        :type value: str
        """
        #TODO: Add support for passing a port object.
        return {"portindex": portindex, "value": value}

    @set_vals("1.3.6.1.2.1.2.2.1.7.{portindex}")
    def _set_port_adminstatus(self, items, portindex, value):
        """_set_port_adminstatus(community, server, items, portindex)
        Sets the adminstatus of the port
        see: http://tools.cisco.com/Support/SNMP/do/BrowseOID.do?objectInput=ifAdminStatus&translate=Translate

        :param portindex: Index of the interface/port
        :type portindex: int
        :param value: New admin status (1 = active, 2 = disabled)
        :type value: int
        """
        return {"portindex": portindex, "value": value}

    def activate_port(self, portindex):
        """
        Activates the port

        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        self._set_port_adminstatus(portindex=portindex, value=1)

    def deactivate_port(self, portindex):
        """
        Deactivates the port

        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        self._set_port_adminstatus(portindex=portindex, value=2)

    @set_vals("1.3.6.1.4.1.9.9.46.1.6.1.1.13.{portindex}")
    def _set_port_trunk(self, items, portindex, value):
        """_set_port_trunk(community, server, portindex, value)
        Sets the trunk status of the port
        see: http://tools.cisco.com/Support/SNMP/do/BrowseOID.do?objectInput=vlanTrunkPortDynamicState&translate=Translate

        :param portindex: Index of the interface/port
        :param value: New trunk dynamic state, (1 = on, 2 = off, 3 = desirable, 4 = auto, 5 = onNoNegotiate)
        """
        return {"portindex": portindex, "value": value}

    def make_port_trunk(self, portindex):
        """
        Makes the port a trunk, equivalent to
           >> switchport mode trunk

        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        self._set_port_trunk(portindex=portindex, value=1)

    def make_port_access(self, portindex):
        """
        Makes the port access, equivalent to
          >> switchport mode access

        :param portindex: Index of the interface/port
        :type portindex: int
        """
        #TODO: Add support for passing a port object.
        self._set_port_trunk(portindex=portindex, value=2)

    def _start_vlan_transaction(self, vlandomain):
        """
        Initiates a vlan update transaction
        raises BlockingIOError if one is in progress.
        raises IOError if the edit table did not get populated

        :param community: SNMP Community
        :param server: Host (switch)
        :param vlandomain: vlan domain, usually 1
        """
        names = "1.3.6.1.4.1.9.9.46.1.4.2.1.4.{vlandomain}".format(vlandomain=vlandomain)
        edits = "1.3.6.1.4.1.9.9.46.1.4.1.1.1.{vlandomain}".format(vlandomain=vlandomain)
        owner = "1.3.6.1.4.1.9.9.46.1.4.1.1.3.{vlandomain}".format(vlandomain=vlandomain)
        if next(snmp_next(self.community, self.server, names, max_rows=1), False):
            data = snmp_get(self.community, self.server, owner)
            raise BlockingIOError("The vlan is being editd by {0}".format(str(data[0][1])))

        snmp_set(self.community, self.server, (edits, 2), (owner, "cisco_swith.py"))

        if next(snmp_next(self.community, self.server, "1.3.6.1.4.1.9.9.46.1.4.2", max_rows=1), False):
            return
        else:
            raise IOError("Vlan Edit table did not prepare properly")

    def _commit_vlan_transaction(self, vlandomain):
        """
        Finishes and commits a vlan transaction
        raises IOError if the update status becomes something other than succeeded
        see: http://tools.cisco.com/Support/SNMP/do/BrowseOID.do?objectInput=vtpVlanApplyStatus&translate=Translate

        :param vlandomain: vlan domain, usually 1
        """
        edits = "1.3.6.1.4.1.9.9.46.1.4.1.1.1.{vlandomain}".format(vlandomain=vlandomain)
        updat = "1.3.6.1.4.1.9.9.46.1.4.1.1.2.{vlandomain}".format(vlandomain=vlandomain)
        snmp_set(self.community, self.server, (edits, 3))
        stat = int(snmp_get(self.community, self.server, updat)[0][1])
        count = 0
        while stat != 2:
            if stat == 1:
                count += 1
                if count > 10:
                    break
                # Give the switch some breathing time
                time.sleep(0.1)
            elif stat > 2:
                raise IOError("Something went wrong during apply, vtpVlanApplyStatus = {0}".format(stat))
            stat = int(snmp_get(self.community, self.server, updat)[0][1])
        snmp_set(self.community, self.server, (edits, 4))

    def _abort_vlan_transaction(self, vlandomain):
        """
        Cancel a vlan transaction.

        :param vlandomain: vlan domain, usually 1
        """
        edits = "1.3.6.1.4.1.9.9.46.1.4.1.1.1.{vlandomain}".format(vlandomain=vlandomain)
        snmp_set(self.community, self.server, (edits, 4))

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
        self._start_vlan_transaction(vlandomain)
        vlanedit = "1.3.6.1.4.1.9.9.46.1.4.2.1.11.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
        vlanname = "1.3.6.1.4.1.9.9.46.1.4.2.1.4.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
        try:
            if type(snmp_get(self.community, self.server, vlanedit)[0][1]) != NoSuchInstance:
                raise ValueError("Vlan does already exist")
            snmp_set(self.community, self.server, (vlanedit, 4), (vlanname, name))
        except ValueError as e:
            self._abort_vlan_transaction(vlandomain)
            raise e
        self._commit_vlan_transaction(vlandomain)

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
        self._start_vlan_transaction(vlandomain)
        vlanedit = "1.3.6.1.4.1.9.9.46.1.4.2.1.11.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
        vlanname = "1.3.6.1.4.1.9.9.46.1.4.2.1.4.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
        try:
            if type(snmp_get(self.community, self.server, vlanedit)[0][1]) == NoSuchInstance:
                raise KeyError("Vlan does not exist")
            snmp_set(self.community, self.server, (vlanname, name))
        except KeyError as e:
            self._abort_vlan_transaction(vlandomain)
            raise e
        self._commit_vlan_transaction(vlandomain)

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
        accessvlan = "1.3.6.1.4.1.9.9.68.1.2.2.1.2.{portindex}".format(portindex=portindex)
        if type(list(snmp_get(self.community, self.server, accessvlan))) == NoSuchInstance:
            raise ValueError("Port does not exist or is not set to mode access")
        snmp_set(self.community, self.server, (accessvlan, vlanid))
        if int(snmp_get(self.community, self.server, accessvlan)[0][1]) == vlanid:
            raise IOError("Could not update access vlan")

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
        self._start_vlan_transaction(vlandomain)
        vlanedit = "1.3.6.1.4.1.9.9.46.1.4.2.1.11.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
        try:
            if type(snmp_get(self.community, self.server, vlanedit)[0][1]) == NoSuchInstance:
                raise KeyError("Vlan does not exist")
            snmp_set(self.community, self.server, (vlanedit, 6))
        except KeyError as e:
            self._abort_vlan_transaction(vlandomain)
            raise e
        self._commit_vlan_transaction(vlandomain)

