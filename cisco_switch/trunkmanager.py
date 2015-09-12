import logging
from cisco_switch import CiscoSwitch, CiscoPort, CiscoVlan

__author__ = 'CVi'
__all__ = ['TrunkManager', 'Host', 'Vlan', 'Port']
"""
This module is a vlan manager that replicates some of the functionality VTP has.
It does not autodiscover topology.

In combination with minifier it can be used to automatically deploy vlans from
an asset manager with minimised trees.
The minimised trees is very useful if STP is causing a lot of CPU-fluctuation
on certain switches. The minimised trees will not compromise alternate-paths.
"""


class Host(object):
    """
    A minimal data object for containing host information,
    also contains the method for retrieving the ports.

    This is made as a class in order to make it easier to extend upon it.
    """
    def __init__(self, name, host_id, fqdn, *args, **kwargs):
        self.name = name
        self.id = host_id
        self.fqdn = fqdn
        self.others_list = args
        self.others_dict = kwargs

    def get_outgoing_links(self):
        """
        Retrieves links that go from this host.
        Must be overridden for trunk-port management to work

        :return: list of ports
        :trype : list[Port]
        """
        return []

    def __str__(self):
        return "<Host: ID:{id}, name:{name}, fqdn:{fqdn}>".format(**self.__dict__)


class Vlan(object):
    """
    A minimal data object for containing vlan information.

    This is made as a class in order to make it easier to extend upon it.
    """
    def __init__(self, vlan_id, name, *args, **kwargs):
        self.id = vlan_id
        self.name = name
        self.others_list = args
        self.others_dict = kwargs


class Port(object):
    """
    A minimal data object for containing port information.

    This is made as a class in order to make it easier to extend upon it.
    """
    def __init__(self, name, remote_id, *args, **kwargs):
        self.name = name
        self.remote_id = remote_id
        self.others_list = args
        self.others_dict = kwargs
        self.hosts = {}


class TrunkManager(object):
    """
    An implementation of VTP-features (including pruning)
    It requires that the programmer provides the topology and minimised graphs.
    The cisco_switch.minifier module can generate minimised graphs.
    """
    def __init__(self, vlans, vlan_map, simulate=True):
        """
        :param vlans: Dictionary of vlans, keyed on ID
        :type vlans: dict[int,Vlan]
        :param vlan_map: Map of vlans on a given device. Key is device ID.
        :type vlan_map: dict[int, list[int]]
        :param simulate: Does not apply if set to true.
        :type simulate: bool
        """
        self.vlans = vlans
        self.vlan_map = vlan_map
        self.simulate = simulate

    def get_host(self, host_id):
        """
        Retrieve a host object for any given ID.
        Must be overridden for class to work.

        :param host_id: Id of host
        :type host_id: int
        :return: Host object representing requested object
        :rtype: Host
        """
        return Host(None, host_id, None)

    def test_deploy_to_switch(self, switch):
        """
        Retruns true if we want to deploy to that switch.
        Can be overridden to change criterion.

        :param switch: Host object (assumed to be a switch)
        :type switch: Host
        :return:
        :rtype bool
        """
        if switch.fqdn is None:
            return False
        else:
            return True

    def test_remove_vlan_switch(self, switch, vlan, snmp_vlan):
        """
        Returns True if it's OK to remove that particular vlan from the switch.
        Can be overridden to change criterion.

        :param switch: Host object (assumed to be a switch)
        :type switch: Switch
        :param vlan: Vlan object
        :type vlan: Vlan
        :param snmp_vlan: Snmp proxy for vlan
        :type snmp_vlan: CiscoVlan
        :return:
        """
        return True

    def test_remove_vlan_port(self, switch, port, vlan_id, snmp_switch, snmp_port):
        """
        Returns True if it's OK to remove particular vlan from that port.
        Can be overridden to change criterion.

        :param switch: Host object (assumed to be a switch)
        :type switch: Switch
        :param vlan_id: Vlan ID
        :type vlan_id: int
        :param port: Port object
        :type port: Port
        :param snmp_switch: Snmp proxy for switch
        :type snmp_switch: CiscoSwitch
        :param snmp_port: Snmp proxy for port
        :type snmp_port: CiscoPort
        :return:
        """
        return True

    def test_edit_stuff_on_port(self, switch, port, snmp_switch, snmp_port):
        """
        Returns True if it's OK to edit anything on that port,
        Can be overridden to change criterion.

        :param switch: Host object (assumed to be a switch)
        :type switch: Switch
        :param port: Port object
        :type port: Port
        :param snmp_switch: Snmp proxy for switch
        :type snmp_switch: CiscoSwitch
        :param snmp_port: Snmp proxy for port
        :type snmp_port: CiscoPort
        :return:
        """
        return True

    def test_edit_vlans_on_port(self, switch, port, snmp_switch, snmp_port):
        """
        Returns True if it's OK to edit vlans on that port,
        Can be overridden to change criterion.

        :param switch: Host object (assumed to be a switch)
        :type switch: Switch
        :param port: Port object
        :type port: Port
        :param snmp_switch: Snmp proxy for switch
        :type snmp_switch: CiscoSwitch
        :param snmp_port: Snmp proxy for port
        :type snmp_port: CiscoPort
        :return:
        """
        return snmp_port.trunk_status()

    def test_edit_port_name(self, switch, port, snmp_switch, snmp_port):
        """
        Returns True if it's OK to edit name of that port,
        Can be overridden to change criterion.

        :param switch: Host object (assumed to be a switch)
        :type switch: Switch
        :param port: Port object
        :type port: Port
        :param snmp_switch: Snmp proxy for switch
        :type snmp_switch: CiscoSwitch
        :param snmp_port: Snmp proxy for port
        :type snmp_port: CiscoPort
        :return:
        """
        return False

    def get_new_port_name(self, switch, port, snmp_switch, snmp_port):
        """
        Returns the name (description) to give the port
        Can be overridden to change algorithm.

        :param switch: Host object (assumed to be a switch)
        :type switch: Switch
        :param port: Port object
        :type port: Port
        :param snmp_switch: Snmp proxy for switch
        :type snmp_switch: CiscoSwitch
        :param snmp_port: Snmp proxy for port
        :type snmp_port: CiscoPort
        :return:
        """
        return port.name

    def remap_port_name(self, name):
        """
        Modifies the provided port name to the SNMP name
        Can be overridden to change behaviour.

        :param name: Input name
        :type name: str
        :return: Modified name (equal to SNMP name)
        :rtype: str
        """
        return name

    def get_community(self, host):
        """
        Get the snmp-community for that host.
        Can be overridden to change behaviour.

        :param host: Host object (assumed to be a switch)
        :type host: Host
        :return: Community to use for this host
        :rtype: str
        """
        return "public"

    def _handle_snmp_vlan(self, host, snmp_switch, snmp_vlan, present_vlans):
        """
        Handle a vlan present on the switch

        :param host: Host object (assumed to be a switch)
        :type host: Host
        :param snmp_switch: Snmp proxy for switch
        :type snmp_switch: CiscoSwitch
        :param snmp_vlan: Snmp proxy for vlan
        :type snmp_vlan: CiscoVlan
        :param present_vlans: List of vlans that are present on the switch; bookkeeping for adding missing vlans.
        :type present_vlans: list[int]
        """
        vlan = self.vlans[snmp_vlan.id] if snmp_vlan.id in self.vlans else None
        present_vlans.append(snmp_vlan.id)
        if host.id in self.vlan_map and snmp_vlan.id in self.vlan_map[host.id]:
            oldname = snmp_vlan.get_name()
            if oldname != vlan.name:
                logging.info("Renaming Vlan {id} from {oname} to {nname} on {swname}"
                             .format(id=snmp_vlan.id, oname=oldname, nname=vlan.name, swname=host.name))
                if not self.simulate:
                    snmp_vlan.rename(vlan.name)
                    return True
        elif self.test_remove_vlan_switch(host, vlan, snmp_vlan):
            logging.info("Deleting Vlan {id} from {swname}"
                         .format(id=snmp_vlan.id, swname=host.name))
            if not self.simulate:
                snmp_switch.delete_vlan(snmp_vlan.id)
                return True

    def _handle_port_vlans(self, host, snmp_switch, snmp_port, port):
        """
        Handle a trunk port. Add/remove vlans as necessary.

        :param host: Host object (assumed to be a switch)
        :type host: Host
        :param snmp_switch: Snmp proxy for switch
        :type snmp_switch: CiscoSwitch
        :param snmp_port: Snmp proxy for port
        :type snmp_port: CiscoPort
        :param port: Port object
        :type port: Port
        """
        vlans_local = set(self.vlan_map[host.id])
        vlans_remote = set(self.vlan_map[port.remote_id])
        vlans_current = set(snmp_port.vlans())

        vlans_link = vlans_local & vlans_remote

        vlans_missing = vlans_link - vlans_current
        vlans_redundant = vlans_current - vlans_link

        activate = []
        ud = False
        for vl in vlans_missing:
            logging.info("Adding vlan {id} to trunk {pname} on {swname}"
                         .format(id=vl, pname=port.name, swname=host.name))
            activate.append(vl)
        if not self.simulate and len(activate) > 0:
            snmp_port.activate_vlans(activate)
            ud = True

        remove = []
        for vl in vlans_redundant:
            if self.test_remove_vlan_port(host, port, vl, snmp_switch, snmp_port):
                logging.info("Removing vlan {id} from trunk {pname} on {swname}"
                             .format(id=vl, pname=port.name, swname=host.name))
                remove.append(vl)
                ud = True
        if not self.simulate and len(remove) > 0:
            snmp_port.deactivate_vlans(remove)
            ud = True
        return ud

    def _handle_host(self, host):
        """
        Handle a host, most likely a switch. Add/prune Vlans from switch and trunks.

        :param host: Host object (assumed to be a switch)
        :type host: Host
        """
        snmp_switch = CiscoSwitch(self.get_community(host), host.fqdn)
        snmp_vlans = snmp_switch.get_vlans()
        present_vlans = []
        ud = False
        for snmp_vlan in snmp_vlans:
            ud = self._handle_snmp_vlan(host, snmp_switch, snmp_vlan, present_vlans) or ud
        for vlan_id in self.vlan_map[host.id]:
            if vlan_id not in present_vlans:
                vlan = self.vlans[vlan_id]
                logging.info("Creating vlan {id} ({vlname}) on switch {swname}"
                             .format(id=vlan_id, vlname=vlan.name, swname=host.name))
                if not self.simulate:
                    snmp_switch.create_vlan(vlan.id, vlan.name)
                    ud = True

        ports = {self.remap_port_name(p.name): p for p in host.get_outgoing_links()}
        for snmp_port in snmp_switch.get_ports():
            if snmp_port.name in ports \
                    and ports[snmp_port.name].remote_id in self.vlan_map \
                    and self.test_edit_stuff_on_port(host, ports[snmp_port.name], snmp_switch, snmp_port):
                if self.test_edit_vlans_on_port(host, ports[snmp_port.name], snmp_switch, snmp_port):
                    ud = self._handle_port_vlans(host, snmp_switch, snmp_port, ports[snmp_port.name]) or ud
                if self.test_edit_port_name(host, ports[snmp_port.name], snmp_switch, snmp_port):
                    odesc = snmp_port.get_alias()
                    ndesc = self.get_new_port_name(host, ports[snmp_port.name], snmp_switch, snmp_port)
                    if odesc != ndesc:
                        logging.info("Renaming port {paname} form {odesc} to {ndesc}"
                                     .format(pname=snmp_port.name, odesc=odesc, ndesc=ndesc))
                        if not self.simulate:
                            snmp_port.set_alias(ndesc)
                            ud = True

        if ud and not self.simulate:
            snmp_switch.wr_mem()

    def apply(self):
        """
        Applies the topology to the network
        """
        for host_id in self.vlan_map:
            host = self.get_host(host_id)
            if not self.test_deploy_to_switch(host):
                continue
            try:
                self._handle_host(host)
            except IOError:
                logging.warning("Could not connect to {hname}".format(hname=host.name))
