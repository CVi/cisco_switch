__author__ = 'CVi'

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.smi import builder, instrum
from pysnmp.entity import engine
from pysnmp.proto.rfc3412 import MsgAndPduDispatcher
from functools import wraps
import os


__all__ = ['snmp_get', 'snmp_set', 'snmp_next', 'fetch_binds', 'set_vals', 'mibBuilder']

# Some background, mibs etc.
mibBuilder = builder.MibBuilder()
mibBuilder.setMibPath(os.path.dirname(os.path.realpath(__file__))+'/mibs', *mibBuilder.getMibPath())
mibBuilder.loadModules('SNMPv2-MIB', 'IF-MIB', 'CISCO-VTP-MIB', 'CISCO-CONFIG-COPY-MIB', 'CISCO-VLAN-MEMBERSHIP-MIB')

# The engine; I don't know how it works anymore, but it works.
mibInstrumController = instrum.MibInstrumController(mibBuilder)
msgAndPduDsp = MsgAndPduDispatcher(mibInstrumController=mibInstrumController)
eg = engine.SnmpEngine(msgAndPduDsp=msgAndPduDsp)
cmdGen = cmdgen.CommandGenerator(snmpEngine=eg)

def snmp_get(community, server, *items):
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((server, 161)),
        *items
    )

    if errorIndication:
        raise IOError(errorIndication)
    elif errorStatus:
        err = '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex)-1] or '?')
        raise IOError(err)
    else:
        return varBinds


def snmp_set(community, server, *pairs):
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((server, 161)),
        *pairs
    )

    if errorIndication:
        raise IOError(errorIndication)
    elif errorStatus:
        err = '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex)-1] or '?')
        raise IOError(err)
    else:
        return varBinds


def snmp_next(community, server, item, max_rows=0):
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.nextCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((server, 161)),
        item,
        maxRows=max_rows
    )

    if errorIndication:
        raise IOError(errorIndication)
    elif errorStatus:
        err = '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex)-1] or '?')
        raise IOError(err)
    else:
        return map(lambda x: x[0], varBinds)


def fetch_binds(*items):
    def fetch_binds_decorator(func):
        @wraps(func)
        def func_wrapper(community, server, **kwargs):
            binds = snmp_get(community, server, *map(lambda item: item.format(**kwargs), items))
            kwargs['binds'] = binds
            return func(community, server, **kwargs)

        return func_wrapper
    return fetch_binds_decorator


def set_vals(*items):
    def fetch_binds_decorator(func):
        @wraps(func)
        def func_wrapper(community, server, **kwargs):
            values = func(community=community, server=server, items=items, **kwargs)
            snmp_set(community, server, *map(lambda item, value: (item.format(**kwargs), value), items, values))

        return func_wrapper
    return fetch_binds_decorator

