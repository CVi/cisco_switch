from functools import wraps

__author__ = 'CVi'


def get_port(func):
    @wraps(func)
    def func_wrapper(self, portindex=0, port=None, **kwags):
        if portindex == 0 and port is not None:
            portindex = self._get_port(port)
        return func(self, portindex=portindex, port=port, **kwags)
    return func_wrapper


def get_vlan(func):
    @wraps(func)
    def func_wrapper(self, vlanid=0, vlan=None, **kwags):
        if vlanid == 0 and vlan is not None:
            vlanid = self._get_vlan(vlan)
        return func(self, vlanid=vlanid, vlan=vlan, **kwags)
    return func_wrapper


class SwitchBase(object):
    def _get_vlan(self, vlan):
        """
        Fetches VlanID and name from a vlan object

        :param vlan:
        :type vlan: CiscoVlan
        :return:
        """
        return vlan.id

    def _get_vlan_name(self, vlan):
        """
        Fetches VlanID and name from a vlan object

        :param vlan:
        :type vlan: CiscoVlan
        :return:
        """
        return vlan.id, vlan.get_name()

    def _get_port(self, port):
        """
        Fetches Portindex form a port object
        :param port:
        :type port: CiscoPort
        :return:
        """
        return port.portindex

    def _extract_vlan_ids(self, vlans):
        return [self._get_vlan(vlan)[0] if isinstance(vlan, SwitchBase) else vlan for vlan in vlans]
