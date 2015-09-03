__author__ = 'CVi'
__all__ = ['get_devices', 'NetMatrix']
"""
A depth first search algorithm for vlans.
Generates minimised path graphs. (Not minimal spanning trees)
Including all optional paths to any location.
"""


def _dfs_step(devs, done, chain, dev, matrix):
    """
    Does DFS iterations on the dataset

    :param devs: Devices found to be in set
    :type devs: list[int]
    :param done: Devices where search is completed
    :type done: list[int]
    :param chain: Chain of devices in current search
    :type chain: tuple[int]
    :param dev: Devce to do in this step
    :type dev: int
    :param matrix: neighbour matrix, dictionary style
    :type matrix: dict[int, list[int]|set[int]]
    :return:
    """
    part_of = False
    for s in matrix[dev]:
        if s in chain or s == dev:
            continue
        elif s in devs:
            if dev not in devs:
                devs.append(dev)
            part_of = True

        if s in done:
            continue
        else:
            part_of_temp = _dfs_step(devs, done, chain + (dev,), s, matrix)
            part_of = part_of or part_of_temp

    if part_of and (dev not in devs):
        devs.append(dev)
    done.append(dev)
    return part_of


def get_devices(matrix, reqs):
    """
    Prepares and runs DFS on

    :param matrix: neighbour matrix, dictionary style
    :type matrix: dict[int, list[int]|set[int]]
    :param reqs: required devices (devices that "need" this vlan)
    :type reqs: list[int]
    :return:
    """
    devs = list(reqs)
    done = []
    for d in devs:
        if d in matrix:
            _dfs_step(devs, done, (), d, matrix)
    return list(devs)


class NetMatrix(object):
    """
    The prefered way of interacting with network minifier.

    It has features to build the matrix as the minifier requires.
    Also provided is a reverser to apply the minified tree using the trunk-manager.
    """
    def __init__(self):
        self._matrix = {}
        self._devices = {}

    def add_device(self, dev_id, name=""):
        """
        Add a device to the matrix

        :param dev_id: Device ID
        :type dev_id: int
        :param name: Name of device
        :type name: str
        """
        if dev_id not in self._devices:
            self._devices[dev_id] = name
            self._matrix[dev_id] = set()

    def add_connection(self, a, b):
        """
        Adds a link between device A and B

        Silently fails if ID of A or B is unknown.
        :param a: ID of one device
        :type a: int
        :param b: ID of the other device
        :type b: int
        """
        if a in self._devices and b in self._devices:
            self._matrix[a].add(b)
            self._matrix[b].add(a)

    def get_devices(self, reqs):
        """
        Returns a list of all the devices in the minimised graph.

        :param reqs: Required devices
        :type reqs: list[int]
        :return:
        :rtype: list[int]
        """
        return get_devices(self._matrix, reqs)

    def make_vlanmap(self, req_map):
        """
        Option, instead of calling get_devices multiple times.

        Parses a dictionary of required-lists (key on vlanid)
        :param req_map:
        :type req_map: dict[int, list[int]]
        :return:
        :rtype: dict[int, list[int]]
        """
        vlmap = {}

        for vlan_id, req in req_map.items():
            vlmap[vlan_id] = self.get_devices(req)
        return vlmap

    @staticmethod
    def reverse_map(vmap):
        """
        Reverses the map to vlans on device instead of devices on vlan

        :param vmap: Vlanmap (same format as make_vlanmap)
        :type vmap: dict[int, list[int]]
        :return: Dict, keyed on device_id, with list of vlans
        :rtype: dict[int, list[int]]
        """
        remap = {}
        for k, vl in vmap.items():
            for v in vl:
                if v in remap:
                    remap[v].add(k)
                else:
                    remap[v] = {k}
        return remap
