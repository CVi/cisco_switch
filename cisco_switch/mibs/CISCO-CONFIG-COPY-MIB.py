# PySNMP SMI module. Autogenerated from smidump -f python CISCO-CONFIG-COPY-MIB
# by libsmi2pysnmp-0.1.3 at Mon Dec  1 16:25:38 2014,
# Python version sys.version_info(major=2, minor=7, micro=6, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( ciscoMgmt, ) = mibBuilder.importSymbols("CISCO-SMI", "ciscoMgmt")
( FcNameIdOrZero, ) = mibBuilder.importSymbols("CISCO-ST-TC", "FcNameIdOrZero")
( InetAddress, InetAddressType, ) = mibBuilder.importSymbols("INET-ADDRESS-MIB", "InetAddress", "InetAddressType")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( ModuleCompliance, NotificationGroup, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup", "ObjectGroup")
( Bits, Integer32, IpAddress, ModuleIdentity, MibIdentifier, NotificationType, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, Unsigned32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "IpAddress", "ModuleIdentity", "MibIdentifier", "NotificationType", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "Unsigned32")
( DisplayString, RowStatus, TextualConvention, TimeStamp, TruthValue, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "RowStatus", "TextualConvention", "TimeStamp", "TruthValue")

# Types

class ConfigCopyFailCause(Integer):
    subtypeSpec = Integer.subtypeSpec+SingleValueConstraint(7,8,2,5,4,1,9,3,6,)
    namedValues = NamedValues(("unknown", 1), ("badFileName", 2), ("timeout", 3), ("noMem", 4), ("noConfig", 5), ("unsupportedProtocol", 6), ("someConfigApplyFailed", 7), ("systemNotReady", 8), ("requestAborted", 9), )
    
class ConfigCopyProtocol(Integer):
    subtypeSpec = Integer.subtypeSpec+SingleValueConstraint(2,1,3,4,5,)
    namedValues = NamedValues(("tftp", 1), ("ftp", 2), ("rcp", 3), ("scp", 4), ("sftp", 5), )
    
class ConfigCopyState(Integer):
    subtypeSpec = Integer.subtypeSpec+SingleValueConstraint(3,2,4,1,)
    namedValues = NamedValues(("waiting", 1), ("running", 2), ("successful", 3), ("failed", 4), )
    
class ConfigFileType(Integer):
    subtypeSpec = Integer.subtypeSpec+SingleValueConstraint(5,4,6,1,3,2,)
    namedValues = NamedValues(("networkFile", 1), ("iosFile", 2), ("startupConfig", 3), ("runningConfig", 4), ("terminal", 5), ("fabricStartupConfig", 6), )
    

# Objects

ciscoConfigCopyMIB = ModuleIdentity((1, 3, 6, 1, 4, 1, 9, 9, 96)).setRevisions(("2005-04-06 00:00","2004-03-17 00:00","2002-12-17 00:00","2002-05-30 00:00","2002-05-07 00:00","2002-03-28 00:00",))
if mibBuilder.loadTexts: ciscoConfigCopyMIB.setOrganization("Cisco Systems, Inc.")
if mibBuilder.loadTexts: ciscoConfigCopyMIB.setContactInfo("Cisco Systems\nCustomer Service\n\nPostal: 170 W. Tasman Drive\nSan Jose, CA  95134\nUSA\n\nTel:    +1 800 553-NETS\n\nE-mail: cs-snmp@cisco.com")
if mibBuilder.loadTexts: ciscoConfigCopyMIB.setDescription("This MIB facilitates writing of configuration files\nof an SNMP Agent running Cisco's IOS in the \nfollowing ways: to and from the net, copying running \nconfigurations to startup configurations and \nvice-versa, and copying a configuration\n(running or startup) to and from the local \nIOS file system.")
ciscoConfigCopyMIBObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 9, 9, 96, 1))
ccCopy = MibIdentifier((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1))
ccCopyTable = MibTable((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1))
if mibBuilder.loadTexts: ccCopyTable.setDescription("A table of config-copy requests.")
ccCopyEntry = MibTableRow((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1)).setIndexNames((0, "CISCO-CONFIG-COPY-MIB", "ccCopyIndex"))
if mibBuilder.loadTexts: ccCopyEntry.setDescription("A config-copy request.\n\nA management station wishing to create an entry \nshould first generate a random serial number to be\nused as the index to this sparse table. The station \nshould then create the associated instance of the\nrow status and row index objects.  It must also, \neither in the same or in successive PDUs, create an\ninstance of ccCopySourceFileType and \nccCopyDestFileType.\n\nAt least one of the file types defined in \nConfigFileType TC must be an agent-config file type\n(i.e. 'startupConfig' or 'runningConfig').\nIf one of the file types is a 'networkFile', a valid\nccCopyFileName and ccCopyServerAddressType and \nccCopyServerAddressRev1 or just ccCopyServerAddress\nmust be created as well. If ccCopyServerAddress is\ncreated then ccCopyServerAddressRev1 will store the\nsame IP address and ccCopyServerAddressType will \ntake the value 'ipv4'.\n\nFor a file type of 'iosFile', only\na valid ccCopyFileName needs to be created as an \nextra parameter.\n\nIt should also modify the default values for the \nother configuration objects if the defaults are not\nappropriate.\n\nOnce the appropriate instance of all the \nconfiguration objects have been created, either by\nan explicit SNMP set request or by default, the row \nstatus should be set to active to initiate the \nrequest. Note that this entire procedure may be \ninitiated via a single set request which specifies\na row status of createAndGo as well as\nspecifies valid values for the non-defaulted \nconfiguration objects.\n\nOnce the config-copy request has been created \n(i.e. the ccCopyEntryRowStatus has been made \nactive), the entry cannot be modified - the only \noperation possible after this is to delete the row.\n\nOnce the request completes, the management station \nshould retrieve the values of the status objects of \ninterest, and should then delete the entry.  In\norder to prevent old entries from clogging the \ntable, entries will be aged out, but an entry will \never be deleted within 5 minutes of completing.")
ccCopyIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: ccCopyIndex.setDescription("Object which specifies a unique entry in the\nccCopyTable.  A management station wishing\nto initiate a config-copy operation should use a\nrandom value for this object when creating\nor modifying an instance of a ccCopyEntry.\nThe RowStatus semantics of the ccCopyEntryRowStatus\nobject will prevent access conflicts.")
ccCopyProtocol = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 2), ConfigCopyProtocol().clone('tftp')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyProtocol.setDescription("The protocol to be used for any copy.\n\nIf the copy operation occurs locally on the SNMP \nagent (e.g. 'runningConfig' to 'startupConfig'),\nthis object may be ignored by the implementation.")
ccCopySourceFileType = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 3), ConfigFileType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopySourceFileType.setDescription("Specifies the type of file to copy from. Either the\nccCopySourceFileType or the ccCopyDestFileType \n(or both) must be of type 'runningConfig' or \n'startupConfig'. Also, the ccCopySourceFileType\nmust be different from the ccCopyDestFileType.\n\nIf the ccCopySourceFileType has the value of \n'networkFile', the ccCopyServerAddress/\nccCopyServerAddressRev1 and ccCopyServerAddressType\nand ccCopyFileName must also be created, and 3 \nobjects together (ccCopySourceFileType,\nccCopyServerAddressRev1, ccCopyFileName) will \nuniquely identify the source file. If \nccCopyServerAddress is created then \nccCopyServerAddressRev1 will store the\nsame IP address and ccCopyServerAddressType will \ntake the value 'ipv4'. \n\nIf the ccCopySourceFileType is 'iosFile', the \nccCopyFileName must also be created, and the \n2 objects together (ccCopySourceFileType,\nccCopyFileName) will uniquely identify the source \nfile.")
ccCopyDestFileType = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 4), ConfigFileType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyDestFileType.setDescription("specifies the type of file to copy to. Either the\nccCopySourceFileType or the ccCopyDestFileType \n(or both) must be of type 'runningConfig' or \n'startupConfig'. Also, the ccCopySourceFileType \nmust be different from the ccCopyDestFileType.\n\nIf the ccCopyDestFileType has the value of \n'networkFile', the \nccCopyServerAddress/ccCopyServerAddressType and\nccCopyServerAddressRev1 and ccCopyFileName must\nalso be created, and 3 objects together\n(ccCopyDestFileType, ccCopyServerAddressRev1,  \nccCopyFileName) will uniquely identify the \ndestination file. If ccCopyServerAddress is created\nthen ccCopyServerAddressRev1 will store the same IP\naddress and ccCopyServerAddressType will take the \nvalue 'ipv4'. \n\nIf the ccCopyDestFileType is 'iosFile', the \nccCopyFileName must also be created, and the 2\nobjects together (ccCopyDestFileType, \nccCopyFileName) will uniquely identify the \ndestination file.")
ccCopyServerAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 5), IpAddress()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyServerAddress.setDescription("The IP address of the TFTP server from (or to)\nwhich to copy the configuration file. This object \nmust be created when either the \nccCopySourceFileType or ccCopyDestFileType has the\nvalue 'networkFile'. \nValues of 0.0.0.0 or FF.FF.FF.FF for\nccCopyServerAddress are not allowed.\n\nSince this object can just hold only IPv4 Transport\ntype, it is deprecated and replaced by \nccCopyServerAddressRev1.")
ccCopyFileName = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 6), DisplayString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyFileName.setDescription("The file name (including the path, if applicable)\nof the file. This object must be created when either\nthe ccCopySourceFileType or ccCopyDestFileType has\nthe value 'networkFile' or 'iosFile'.")
ccCopyUserName = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 7), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 40))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyUserName.setDescription("Remote username for copy via FTP, RCP, SFTP or\nSCP protocol.\nThis object must be created when the ccCopyProtocol\nis 'rcp', 'scp', 'ftp', or 'sftp'.\nIf the protocol is RCP, it will override the remote \nusername configured through the \n        rcmd remote-username <username>\nconfiguration command. \nThe remote username is sent as the server username \nin an RCP command request sent by the system to a\nremote RCP server.")
ccCopyUserPassword = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 8), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 40))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyUserPassword.setDescription("Password used by FTP, SFTP or SCP for copying a\nfile to/from an FTP/SFTP/SCP server. This object \nmust be created when the ccCopyProtocol is FTP or\nSCP. \nReading it returns a zero-length string for security \nreasons.")
ccCopyNotificationOnCompletion = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 9), TruthValue().clone('false')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyNotificationOnCompletion.setDescription("Specifies whether or not a ccCopyCompletion\nnotification should be issued on completion of the\nTFTP transfer. If such a notification is desired, \nit is the responsibility of the management entity to\nensure that the SNMP administrative model is \nconfigured in such a way as to allow the \nnotification to be delivered.")
ccCopyState = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 10), ConfigCopyState()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ccCopyState.setDescription("Specifies the state of this config-copy request.\nThis value of this object is instantiated only after \nthe row has been instantiated, i.e. after the \nccCopyEntryRowStatus has been made active.")
ccCopyTimeStarted = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 11), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ccCopyTimeStarted.setDescription("Specifies the time the ccCopyState last\ntransitioned to 'running', or 0 if the state has \nnever transitioned to 'running'(e.g., stuck in\n'waiting' state).\n\nThis object is instantiated only after the row has \nbeen instantiated.")
ccCopyTimeCompleted = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 12), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ccCopyTimeCompleted.setDescription("Specifies the time the ccCopyState last\ntransitioned from 'running' to 'successful' or \n'failed' states. This object is instantiated only \nafter the row has been instantiated.\nIts value will remain 0 until the request has \ncompleted.")
ccCopyFailCause = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 13), ConfigCopyFailCause()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ccCopyFailCause.setDescription("The reason why the config-copy operation failed.\nThis object is instantiated only when the \nccCopyState for this entry is in the \n'failed' state.")
ccCopyEntryRowStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 14), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyEntryRowStatus.setDescription("The status of this table entry. Once the entry\nstatus is set to active, the associated entry cannot \nbe modified until the request completes \n(ccCopyState transitions to 'successful'\nor 'failed' state).")
ccCopyServerAddressType = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 15), InetAddressType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyServerAddressType.setDescription("This object indicates the transport type of the\naddress contained in ccCopyServerAddressRev1 object.\n\nThis must be created when either the\nccCopySourceFileType or ccCopyDestFileType has the\nvalue 'networkFile'.")
ccCopyServerAddressRev1 = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 1, 1, 16), InetAddress()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: ccCopyServerAddressRev1.setDescription("The IP address of the TFTP server from (or to)\nwhich to copy the configuration file. This object\nmust be created when either the \nccCopySourceFileType or ccCopyDestFileType has the\nvalue 'networkFile'.  \n\nAll bits as 0s or 1s for ccCopyServerAddressRev1 are\nnot allowed.\n\nThe format of this address depends on the value of \nthe ccCopyServerAddressType object.")
ccCopyErrorTable = MibTable((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 2))
if mibBuilder.loadTexts: ccCopyErrorTable.setDescription("A table containing information about the failure\ncause of the config copy operation. An entry is\ncreated only when the value of ccCopyState changes\nto 'failed' for a config copy operation.\n\nNot all combinations of ccCopySourceFileType and\nccCopyDestFileType need to be supported.  For\nexample, an implementation may choose to support\nonly the following combination:\nccCopySourceFileType = 'runningConfig'\nccCopyDestFileType = 'fabricStartupConfig'. \n\nIn the case where a fabric wide config copy \noperation is being performed, for example by\nselecting ccCopyDestFileType value to be\n'fabricStartupConfig', it is possible that the\nfabric could have more than one device. In such\ncases this table would have one entry for each\ndevice in the fabric. In this case even if the \noperation succeeded in one device and failed in \nanother, the operation as such has failed, so the\nglobal state  represented by ccCopyState 'failed',\nbut for the device on which it was success, \nccCopyErrorDescription would have the \ndistinguished value, 'success'. \n\nOnce the config copy operation completes and if an\nentry gets instantiated, the management station \nshould retrieve the values of the status objects of \ninterest. Once an entry in ccCopyTable is deleted\nby management station, all the corresponding entries\nwith the same ccCopyIndex in this table are also \ndeleted. \n\nIn order to prevent old entries from clogging the \ntable, entries age out at the same time as the \ncorresponding entry with same ccCopyIndex in \nccCopyTable ages out.")
ccCopyErrorEntry = MibTableRow((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 2, 1)).setIndexNames((0, "CISCO-CONFIG-COPY-MIB", "ccCopyIndex"), (0, "CISCO-CONFIG-COPY-MIB", "ccCopyErrorIndex"))
if mibBuilder.loadTexts: ccCopyErrorEntry.setDescription("An entry containing information about the\noutcome at one destination of a failed config\ncopy operation.")
ccCopyErrorIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 2, 1, 1), Unsigned32()).setMaxAccess("noaccess")
if mibBuilder.loadTexts: ccCopyErrorIndex.setDescription("A monotonically increasing integer for the sole\npurpose of indexing entries in this table.\nWhen a config copy operation has multiple \ndestinations, then this index value is used to \ndistinguish between those multiple destinations.")
ccCopyErrorDeviceIpAddressType = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 2, 1, 2), InetAddressType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ccCopyErrorDeviceIpAddressType.setDescription("The type of Internet address for this destination\ndevice on which config copy operation is performed.")
ccCopyErrorDeviceIpAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 2, 1, 3), InetAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ccCopyErrorDeviceIpAddress.setDescription("The IP address of this destination device on which\nconfig copy operation is performed.\nThe object value has to be consistent with the type\nspecified in ccCopyErrorDeviceIpAddressType.")
ccCopyErrorDeviceWWN = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 2, 1, 4), FcNameIdOrZero()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ccCopyErrorDeviceWWN.setDescription("The World Wide Name (WWN) of this destination\ndevice on which config copy operation is performed.\nThe value of this object is zero-length string if \nWWN is unassigned or unknown. For example, devices \nwhich do not support fibre channel would not\nhave WWN.")
ccCopyErrorDescription = MibTableColumn((1, 3, 6, 1, 4, 1, 9, 9, 96, 1, 1, 2, 1, 5), SnmpAdminString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: ccCopyErrorDescription.setDescription("The error description for the error happened\nfor this destination of this config copy \noperation.")
ciscoConfigCopyMIBTrapPrefix = MibIdentifier((1, 3, 6, 1, 4, 1, 9, 9, 96, 2))
ccCopyMIBTraps = MibIdentifier((1, 3, 6, 1, 4, 1, 9, 9, 96, 2, 1))
ciscoConfigCopyMIBConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 9, 9, 96, 3))
ccCopyMIBCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 1))
ccCopyMIBGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 2))

# Augmentions

# Notifications

ccCopyCompletion = NotificationType((1, 3, 6, 1, 4, 1, 9, 9, 96, 2, 1, 1)).setObjects(*(("CISCO-CONFIG-COPY-MIB", "ccCopyServerAddress"), ("CISCO-CONFIG-COPY-MIB", "ccCopyTimeCompleted"), ("CISCO-CONFIG-COPY-MIB", "ccCopyState"), ("CISCO-CONFIG-COPY-MIB", "ccCopyFailCause"), ("CISCO-CONFIG-COPY-MIB", "ccCopyTimeStarted"), ("CISCO-CONFIG-COPY-MIB", "ccCopyFileName"), ) )
if mibBuilder.loadTexts: ccCopyCompletion.setDescription("A ccCopyCompletion trap is sent at the completion\nof a config-copy request. The ccCopyFailCause is not\ninstantiated, and hence not included in a trap, when \nthe ccCopyState is success.")

# Groups

ccCopyGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 2, 1)).setObjects(*(("CISCO-CONFIG-COPY-MIB", "ccCopyUserPassword"), ("CISCO-CONFIG-COPY-MIB", "ccCopyNotificationOnCompletion"), ("CISCO-CONFIG-COPY-MIB", "ccCopyTimeCompleted"), ("CISCO-CONFIG-COPY-MIB", "ccCopyDestFileType"), ("CISCO-CONFIG-COPY-MIB", "ccCopySourceFileType"), ("CISCO-CONFIG-COPY-MIB", "ccCopyFailCause"), ("CISCO-CONFIG-COPY-MIB", "ccCopyTimeStarted"), ("CISCO-CONFIG-COPY-MIB", "ccCopyProtocol"), ("CISCO-CONFIG-COPY-MIB", "ccCopyFileName"), ("CISCO-CONFIG-COPY-MIB", "ccCopyState"), ("CISCO-CONFIG-COPY-MIB", "ccCopyUserName"), ("CISCO-CONFIG-COPY-MIB", "ccCopyEntryRowStatus"), ("CISCO-CONFIG-COPY-MIB", "ccCopyServerAddress"), ) )
if mibBuilder.loadTexts: ccCopyGroup.setDescription("A collection of objects providing the ability to\ncopy an agent-configuration file.\n\nThis Group is deprecated and new group is defined.")
ccCopyNotificationsGroup = NotificationGroup((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 2, 2)).setObjects(*(("CISCO-CONFIG-COPY-MIB", "ccCopyCompletion"), ) )
if mibBuilder.loadTexts: ccCopyNotificationsGroup.setDescription("The notification used to indicate that a config-copy\noperation to or from the agent has been completed.")
ccCopyGroupRev1 = ObjectGroup((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 2, 3)).setObjects(*(("CISCO-CONFIG-COPY-MIB", "ccCopyUserPassword"), ("CISCO-CONFIG-COPY-MIB", "ccCopyNotificationOnCompletion"), ("CISCO-CONFIG-COPY-MIB", "ccCopyTimeCompleted"), ("CISCO-CONFIG-COPY-MIB", "ccCopyDestFileType"), ("CISCO-CONFIG-COPY-MIB", "ccCopySourceFileType"), ("CISCO-CONFIG-COPY-MIB", "ccCopyFailCause"), ("CISCO-CONFIG-COPY-MIB", "ccCopyTimeStarted"), ("CISCO-CONFIG-COPY-MIB", "ccCopyProtocol"), ("CISCO-CONFIG-COPY-MIB", "ccCopyFileName"), ("CISCO-CONFIG-COPY-MIB", "ccCopyServerAddressRev1"), ("CISCO-CONFIG-COPY-MIB", "ccCopyServerAddressType"), ("CISCO-CONFIG-COPY-MIB", "ccCopyState"), ("CISCO-CONFIG-COPY-MIB", "ccCopyUserName"), ("CISCO-CONFIG-COPY-MIB", "ccCopyEntryRowStatus"), ) )
if mibBuilder.loadTexts: ccCopyGroupRev1.setDescription("A collection of objects providing the ability to\ncopy an agent-configuration file.\n\nThis group deprecates the old group ccCopyGroup.")
ccCopyErrorGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 2, 4)).setObjects(*(("CISCO-CONFIG-COPY-MIB", "ccCopyErrorDeviceIpAddress"), ("CISCO-CONFIG-COPY-MIB", "ccCopyErrorDescription"), ("CISCO-CONFIG-COPY-MIB", "ccCopyErrorDeviceWWN"), ("CISCO-CONFIG-COPY-MIB", "ccCopyErrorDeviceIpAddressType"), ) )
if mibBuilder.loadTexts: ccCopyErrorGroup.setDescription("A collection of objects providing the result\nof a config copy operation when the value of\nccCopyDestFileType is 'fabricStartupConfig' and \nvalue of ccCopyState is 'failed'.")

# Compliances

ccCopyMIBCompliance = ModuleCompliance((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 1, 1)).setObjects(*(("CISCO-CONFIG-COPY-MIB", "ccCopyNotificationsGroup"), ("CISCO-CONFIG-COPY-MIB", "ccCopyGroup"), ) )
if mibBuilder.loadTexts: ccCopyMIBCompliance.setDescription("The compliance statement for Cisco agents which\nimplement the Cisco ConfigCopy MIB. This MIB should \nbe implemented on all Cisco agents that support \ncopying of configs via the CLI.\n\nThis compliance is deprecated and new compliance\nccCopyMIBComplianceRev1 is defined.")
ccCopyMIBComplianceRev1 = ModuleCompliance((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 1, 2)).setObjects(*(("CISCO-CONFIG-COPY-MIB", "ccCopyNotificationsGroup"), ("CISCO-CONFIG-COPY-MIB", "ccCopyGroupRev1"), ) )
if mibBuilder.loadTexts: ccCopyMIBComplianceRev1.setDescription("The compliance statement for Cisco agents which\nimplement the Cisco ConfigCopy MIB. This MIB should \nbe implemented on all Cisco agents that support \ncopying of configs via the CLI.\n\nThis compliance module deprecates\nccCopyMIBCompliance.")
ccCopyMIBComplianceRev2 = ModuleCompliance((1, 3, 6, 1, 4, 1, 9, 9, 96, 3, 1, 3)).setObjects(*(("CISCO-CONFIG-COPY-MIB", "ccCopyNotificationsGroup"), ("CISCO-CONFIG-COPY-MIB", "ccCopyGroupRev1"), ("CISCO-CONFIG-COPY-MIB", "ccCopyErrorGroup"), ) )
if mibBuilder.loadTexts: ccCopyMIBComplianceRev2.setDescription("The compliance statement for Cisco agents which\nimplement the Cisco ConfigCopy MIB. This MIB should \nbe implemented on all Cisco agents that support \ncopying of configs via the CLI.\n\nThis compliance module deprecates\nccCopyMIBComplianceRev1.")

# Exports

# Module identity
mibBuilder.exportSymbols("CISCO-CONFIG-COPY-MIB", PYSNMP_MODULE_ID=ciscoConfigCopyMIB)

# Types
mibBuilder.exportSymbols("CISCO-CONFIG-COPY-MIB", ConfigCopyFailCause=ConfigCopyFailCause, ConfigCopyProtocol=ConfigCopyProtocol, ConfigCopyState=ConfigCopyState, ConfigFileType=ConfigFileType)

# Objects
mibBuilder.exportSymbols("CISCO-CONFIG-COPY-MIB", ciscoConfigCopyMIB=ciscoConfigCopyMIB, ciscoConfigCopyMIBObjects=ciscoConfigCopyMIBObjects, ccCopy=ccCopy, ccCopyTable=ccCopyTable, ccCopyEntry=ccCopyEntry, ccCopyIndex=ccCopyIndex, ccCopyProtocol=ccCopyProtocol, ccCopySourceFileType=ccCopySourceFileType, ccCopyDestFileType=ccCopyDestFileType, ccCopyServerAddress=ccCopyServerAddress, ccCopyFileName=ccCopyFileName, ccCopyUserName=ccCopyUserName, ccCopyUserPassword=ccCopyUserPassword, ccCopyNotificationOnCompletion=ccCopyNotificationOnCompletion, ccCopyState=ccCopyState, ccCopyTimeStarted=ccCopyTimeStarted, ccCopyTimeCompleted=ccCopyTimeCompleted, ccCopyFailCause=ccCopyFailCause, ccCopyEntryRowStatus=ccCopyEntryRowStatus, ccCopyServerAddressType=ccCopyServerAddressType, ccCopyServerAddressRev1=ccCopyServerAddressRev1, ccCopyErrorTable=ccCopyErrorTable, ccCopyErrorEntry=ccCopyErrorEntry, ccCopyErrorIndex=ccCopyErrorIndex, ccCopyErrorDeviceIpAddressType=ccCopyErrorDeviceIpAddressType, ccCopyErrorDeviceIpAddress=ccCopyErrorDeviceIpAddress, ccCopyErrorDeviceWWN=ccCopyErrorDeviceWWN, ccCopyErrorDescription=ccCopyErrorDescription, ciscoConfigCopyMIBTrapPrefix=ciscoConfigCopyMIBTrapPrefix, ccCopyMIBTraps=ccCopyMIBTraps, ciscoConfigCopyMIBConformance=ciscoConfigCopyMIBConformance, ccCopyMIBCompliances=ccCopyMIBCompliances, ccCopyMIBGroups=ccCopyMIBGroups)

# Notifications
mibBuilder.exportSymbols("CISCO-CONFIG-COPY-MIB", ccCopyCompletion=ccCopyCompletion)

# Groups
mibBuilder.exportSymbols("CISCO-CONFIG-COPY-MIB", ccCopyGroup=ccCopyGroup, ccCopyNotificationsGroup=ccCopyNotificationsGroup, ccCopyGroupRev1=ccCopyGroupRev1, ccCopyErrorGroup=ccCopyErrorGroup)

# Compliances
mibBuilder.exportSymbols("CISCO-CONFIG-COPY-MIB", ccCopyMIBCompliance=ccCopyMIBCompliance, ccCopyMIBComplianceRev1=ccCopyMIBComplianceRev1, ccCopyMIBComplianceRev2=ccCopyMIBComplianceRev2)
