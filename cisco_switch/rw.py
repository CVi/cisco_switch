"""
.. module:: rw
   :synopsis: Read/write and read/create functions

.. moduleauthor:: Christoffer Viken <christoffer@viken.me>

Be aware, decorators are signature altering.
Only community and server are guaranteed to be positional.
"""
import time

__author__ = 'CVi'

import random
from pysnmp.proto.rfc1905 import NoSuchInstance
from pysnmp.proto.rfc1902 import OctetString
from .snmp_funcs import set_vals, snmp_get, snmp_set, snmp_next

__all__ = ['activate_vlan_on_port', 'deactivate_vlan_on_port', 'wr_mem', 'set_port_alias', 'activate_port',
           'deactivate_port', 'make_port_trunk', 'make_port_access', 'delete_vlan', 'create_vlan', 'rename_vlan',
           'set_access_vlan', '_set_port_trunk']

def _meta_vlan(community, server, portindex, vlanid, status):
    """
    Meta function for updating vlan on a port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :param vlanid: VlanID, usually the 802.1q tag number.
    :param status: New vlan status as a 0/1 string.
    """
    if vlanid <= 0 or vlanid >= 4096:
        raise ValueError("Invalid VLAN")
    elif vlanid <= 1023:
        oid = "1.3.6.1.4.1.9.9.46.1.6.1.1.4.%i" % portindex
    elif vlanid <= 2047:
        oid = "1.3.6.1.4.1.9.9.46.1.6.1.1.17.%i" % portindex
        vlanid -= 1024
    elif vlanid <= 3071:
        oid = "1.3.6.1.4.1.9.9.46.1.6.1.1.18.%i" % portindex
        vlanid -= 2048
    else:
        oid = "1.3.6.1.4.1.9.9.46.1.6.1.1.19.%i" % portindex
        vlanid -= 3072

    ((a, serial), (b, vlans)) = snmp_get(community, server, "1.3.6.1.4.1.9.9.46.1.6.2.0", oid)
    val_str = vlans.prettyPrint()
    if val_str == "b''":
        val_str = "0000"
    l = val_str[2:].ljust(256, '0')
    b = list(bin(int(l, 16))[2:].zfill(len(l)*4))
    b[vlanid] = status
    b = "".join(b)
    os = OctetString(binValue=b)

    snmp_set(community, server, ("1.3.6.1.4.1.9.9.46.1.6.2.0", serial), (oid, os))


def activate_vlan_on_port(community, server, portindex, vlanid):
    """
    Activates a vlan on the port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :param vlanid: VlanID, usually the 802.1q tag number.
    """
    _meta_vlan(community, server, portindex, vlanid, "1")


def deactivate_vlan_on_port(community, server, portindex, vlanid):
    """
    Deactivates a vlan on the port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :param vlanid: VlanID, usually the 802.1q tag number.
    """
    _meta_vlan(community, server, portindex, vlanid, "0")


def wr_mem(community, server):
    """
    Saves the config on the switch

    :param community: SNMP Community
    :param server: Host (switch)
    """
    key = random.randint(1, 255)
    snmp_set(community, server, ('1.3.6.1.4.1.9.9.96.1.1.1.1.3.%i' % key, 4),
             ('1.3.6.1.4.1.9.9.96.1.1.1.1.4.%i' % key, 3), ('1.3.6.1.4.1.9.9.96.1.1.1.1.14.%i' % key, 4))

@set_vals('1.3.6.1.2.1.31.1.1.1.18.{portindex}')
def set_port_alias(community, server, items, portindex, value):
    """set_port_alias(community, server, portindex, value)
    Sets the alias of a port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :param value: New port alias
    """
    pass

@set_vals("1.3.6.1.2.1.2.2.1.7.{portindex}")
def _set_port_adminstatus(community, server, items, portindex, value):
    """_set_port_adminstatus(community, server, items, portindex)
    Sets the adminstatus of the port
    see: http://tools.cisco.com/Support/SNMP/do/BrowseOID.do?objectInput=ifAdminStatus&translate=Translate

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :param value: New admin status (1 = active, 2 = disabled)
    """
    # All the magic happens in the decorator
    pass

def activate_port(community, server, portindex):
    """
    Activates the port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    """
    _set_port_adminstatus(community, server, portindex=portindex, value=1)

def deactivate_port(community, server, portindex):
    """
    Deactivates the port

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    """
    _set_port_adminstatus(community, server, portindex=portindex, value=2)

@set_vals("1.3.6.1.4.1.9.9.46.1.6.1.1.13.{portindex}")
def _set_port_trunk(community, server, items, portindex, value):
    """_set_port_trunk(community, server, portindex, value)
    Sets the trunk status of the port
    see: http://tools.cisco.com/Support/SNMP/do/BrowseOID.do?objectInput=vlanTrunkPortDynamicState&translate=Translate

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    :param value: New trunk dynamic state, (1 = on, 2 = off, 3 = desirable, 4 = auto, 5 = onNoNegotiate)
    """
    # All the magic happens in the decorator
    pass

def make_port_trunk(community, server, portindex):
    """
    Makes the port a trunk, equivalent to
       >> switchport mode trunk

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    """
    _set_port_trunk(community, server, portindex=portindex, value=1)

def make_port_access(community, server, portindex):
    """
    Makes the port access, equivalent to
      >> switchport mode access

    :param community: SNMP Community
    :param server: Host (switch)
    :param portindex: Index of the interface/port
    """
    _set_port_trunk(community, server, portindex=portindex, value=2)

def _start_vlan_transaction(community, server, vlandomain):
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
    if next(snmp_next(community, server, names, max_rows=1), False):
        data = snmp_get(community, server, owner)
        raise BlockingIOError("The vlan is being editd by {0}".format(str(data[0][1])))

    snmp_set(community, server, (edits, 2), (owner, "cisco_swith.py"))

    if next(snmp_next(community, server, "1.3.6.1.4.1.9.9.46.1.4.2", max_rows=1), False):
        return
    else:
        raise IOError("Vlan Edit table did not prepare properly")

def _commit_vlan_transaction(community, server, vlandomain):
    """
    Finishes and commits a vlan transaction
    raises IOError if the update status becomes something other than succeeded
    see: http://tools.cisco.com/Support/SNMP/do/BrowseOID.do?objectInput=vtpVlanApplyStatus&translate=Translate

    :param community: SNMP Community
    :param server: Host (switch)
    :param vlandomain: vlan domain, usually 1
    """
    edits = "1.3.6.1.4.1.9.9.46.1.4.1.1.1.{vlandomain}".format(vlandomain=vlandomain)
    updat = "1.3.6.1.4.1.9.9.46.1.4.1.1.2.{vlandomain}".format(vlandomain=vlandomain)
    snmp_set(community, server, (edits, 3))
    stat = int(snmp_get(community, server, updat)[0][1])
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
        stat = int(snmp_get(community, server, updat)[0][1])
    snmp_set(community, server, (edits, 4))

def _abort_vlan_transaction(community, server, vlandomain):
    """
    Cancel a vlan transaction.

    :param community: SNMP Community
    :param server: Host (switch)
    :param vlandomain: vlan domain, usually 1
    """
    edits = "1.3.6.1.4.1.9.9.46.1.4.1.1.1.{vlandomain}".format(vlandomain=vlandomain)
    snmp_set(community, server, (edits, 4))


def delete_vlan(community, server, vlanid, vlandomain):
    """
    Delete a vlan
    Raises KeyError if vlan does not exist

    :param community: SNMP Community
    :param server: Host (switch)
    :param vlanid: VlanID, usually the 802.1q tag number.
    :param vlandomain: vlan domain, usually 1
    """
    _start_vlan_transaction(community, server, vlandomain)
    vlanedit = "1.3.6.1.4.1.9.9.46.1.4.2.1.11.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
    try:
        if type(snmp_get(community, server, vlanedit)[0][1]) == NoSuchInstance:
            raise KeyError("Vlan does not exist")
        snmp_set(community, server, (vlanedit, 6))
    except KeyError as e:
        _abort_vlan_transaction(community, server, vlandomain)
        raise e
    _commit_vlan_transaction(community, server, vlandomain)


def create_vlan(community, server, vlanid, name, vlandomain):
    """
    Creates a new vlan
    Raises ValueError if vlan does already exist

    :param community: SNMP Community
    :param server: Host (switch)
    :param vlanid: VlanID, usually the 802.1q tag number.
    :param name: Name of vlan
    :param vlandomain: vlan domain, usually 1
    """
    _start_vlan_transaction(community, server, vlandomain)
    vlanedit = "1.3.6.1.4.1.9.9.46.1.4.2.1.11.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
    vlanname = "1.3.6.1.4.1.9.9.46.1.4.2.1.4.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
    try:
        if type(snmp_get(community, server, vlanedit)[0][1]) != NoSuchInstance:
            raise ValueError("Vlan does already exist")
        snmp_set(community, server, (vlanedit, 4), (vlanname, name))
    except ValueError as e:
        _abort_vlan_transaction(community, server, vlandomain)
        raise e
    _commit_vlan_transaction(community, server, vlandomain)

def rename_vlan(community, server, vlanid, name, vlandomain):
    """
    Renames a vlan
    Raises KeyError if vlan does not exist

    :param community: SNMP Community
    :param server: Host (switch)
    :param vlanid: VlanID, usually the 802.1q tag number.
    :param name: New name of vlan
    :param vlandomain: vlan domain, usually 1
    """
    _start_vlan_transaction(community, server, vlandomain)
    vlanedit = "1.3.6.1.4.1.9.9.46.1.4.2.1.11.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
    vlanname = "1.3.6.1.4.1.9.9.46.1.4.2.1.4.{vlandomain}.{vlanid}".format(vlandomain=vlandomain, vlanid=vlanid)
    try:
        if type(snmp_get(community, server, vlanedit)[0][1]) == NoSuchInstance:
            raise KeyError("Vlan does not exist")
        snmp_set(community, server, (vlanname, name))
    except KeyError as e:
        _abort_vlan_transaction(community, server, vlandomain)
        raise e
    _commit_vlan_transaction(community, server, vlandomain)



def set_access_vlan(community, server, vlanid, portindex):
    """
    Sets the access vlan on an access port
    raises ValueError if the port is not found in access port table
    raises IOError if the access vlan did not change to the new value

    :param community: SNMP Community
    :param server: Host (switch)
    :param vlanid: VlanID, usually the 802.1q tag number.
    :param portindex: Index of the interface/port
    """
    accessvlan = "1.3.6.1.4.1.9.9.68.1.2.2.1.2.{portindex}".format(portindex=portindex)
    if type(list(snmp_get(community, server, accessvlan))) == NoSuchInstance:
        raise ValueError("Port does not exist or is not set to mode access")
    snmp_set(community, server, (accessvlan, vlanid))
    if int(snmp_get(community, server, accessvlan)[0][1]) == vlanid:
        raise IOError("Could not update access vlan")
