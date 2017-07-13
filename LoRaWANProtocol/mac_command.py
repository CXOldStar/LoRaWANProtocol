from .const import MacCID, MType

class MacCommand:
    _receiver_dev_cid_map = {
        MacCID.Server.LinkCheckAns: LinkCheckAns.analysis,
        MacCID.Server.LinkADRReq: LinkADRReq.analysis,
        MacCID.Server.DutyCycleReq: DutyCycleReq.analysis,
        MacCID.Server.RXParamSetupReq: RXParamSetupReq.analysis,
        MacCID.Server.DevStatusReq: DevStatusReq.analysis,
        MacCID.Server.NewChannelReq: NewChannelReq.analysis,
        MacCID.Server.RXTimingSetupReq: RXTimingSetupReq.analysis,
        MacCID.Server.TxParamSetupReq: TxParamSetupReq.analysis,
        MacCID.Server.DlChannelReq: DlChannelReq.analysis
    }
    _receiver_server_cid_map = {
        MacCID.Dev.LinkCheckReq: LinkCheckReq.analysis,
        MacCID.Dev.LinkADRAns: LinkADRAns.analysis,
        MacCID.Dev.DutyCycleAns: DutyCycleAns.analysis,
        MacCID.Dev.RXParamSetupAns: RXParamSetupAns.analysis,
        MacCID.Dev.DevStatusAns: DevStatusAns.analysis,
        MacCID.Dev.NewChannelAns: NewChannelAns.analysis,
        MacCID.Dev.RXTimingSetupAns: RXTimingSetupAns.analysis,
        MacCID.Dev.TxParamSetupAns: TxParamSetupAns.analysis,
        MacCID.Dev.DlChannelAns: DlChannelAns.analysis
    }
    _receiver_classb_dev_cid_map = {
        MacCID.Server.PingSlotInfoAns: ,
        MacCID.Server.PingSlotChannelReq: ,
        MacCID.Server.BeaconFreqReq: ,
        MacCID.Server.BeaconTimingAns: 
    }
    _receiver_classb_server_cid_map = {
        MacCID.Dev.PingSlotInfoReq: ,
        MacCID.Dev.PingSlotChannelAns: ,
        MacCID.Dev.BeaconFreqAns: ,
        MacCID.Dev.BeaconTimingReq: 
    }

    def __init(self, mac_command_cid, mac_command_init):
        self.mac_command_cid = mac_command_cid
        self.mac_command_init = mac_command_init

    @staticmethod
    def analysis(msg_type, mac_command_data):
        cid = mac_command_data[0]
        mac_command = mac_command_data[1:]
        if msg_type == MType.CONFIRMED_DATA_UP or msg_type == MType.UNCONFIRMED_DATA_UP:
            deal_cid = MacCommand._receiver_server_cid_map.get(cid, '')
            if deal_cid:
                deal_cid(cid, mac_command)
            else:
                return None
        elif msg_type == MType.CONFIRMED_DATA_DOWN or msg_type == MType.UNCONFIRMED_DATA_DOWN:
            deal_cid = MacCommand._receiver_dev_cid_map.get(cid, '')
            if deal_cid:
                deal_cid(cid, mac_command)
            else:
                return None
        else:
            return None


"""
Below Mac Command is belong to Class A, B, C device.
"""



class LinkCheckReq:
    """docstring for LinkCheckReq"""
    def __init__(self):
        pass
        
    @staticmethod
    def analysis(mac_command_data):
        return None

    @staticmethod
    def generate(obj):
        return None


class LinkCheckAns:
    """docstring for LinkCheckAns"""
    def __init__(self, margin, gwcnt):
        self.margin = margin
        self.gwcnt = gwcnt
        
    @staticmethod
    def analysis(mac_command_data):
        margin = mac_command_data[0]
        gwcnt = mac_command_data[1]
        return LinkCheckAns(margin, gwcnt)

    @staticmethod
    def generate(obj):
        pass


class LinkADRReq:
    """docstring for LinkADRReq"""
    def __init__(self, datarate, txpower, chmask, chmaskcntl, nbtrans):
        self.datarate = datarate
        self.txpower = txpower
        self.chmask = chmask
        self.chmaskcntl = chmaskcntl
        self.nbtrans = nbtrans
        
    @staticmethod
    def analysis(mac_command_data):
        datarate_txpower = mac_command_data[0]
        datarate = datarate_txpower >> 4
        txpower = datarate_txpower & 0x0F
        
        chmask = mac_command_data[1:3]
        chmask_channel_list = []
        for i in range(16):
            bit = (chmask >> i) & 0x01 
            chmask_channel_list.append(bit)

        redundancy = mac_command_data[3]
        chmaskcntl = (redundancy & 0x70) >> 4
        nbtrans = redundancy & 0x0F


    @staticmethod
    def generate(obj):
        pass


class LinkADRAns:
    """docstring for LinkADRAns"""
    def __init__(self, power_ack, datarate_ack, channel_mask_ack):
        self.power_ack = power_ack
        self.datarate_ack = datarate_ack
        self.channel_mask_ack = channel_mask_ack
        
    @staticmethod
    def analysis(mac_command_data):
        power_ack = (mac_command_data >> 2) & 0x01
        datarate_ack = (mac_command_data >> 1) & 0x01
        channel_mask_ack = mac_command_data & 0x01
        return LinkADRReq(power_ack, datarate_ack, channel_mask_ack)

    @staticmethod
    def generate(obj):
        pass


class DutyCycleReq:
    """docstring for DutyCycleReq"""
    def __init__(self, max_dcycle):
        self.max_dcycle = max_dcycle
        
    @staticmethod
    def analysis(mac_command_data):
        max_dcycle = mac_command_data & 0x0f
        return DutyCycleReq(max_dcycle=max_dcycle)

    @staticmethod
    def generate(obj):
        pass


class DutyCycleAns:
    """docstring for DutyCycleAns"""
    def __init__(self):
        pass
        
    @staticmethod
    def analysis(mac_command_data):
        return None

    @staticmethod
    def generate(obj):
        return None


class RXParamSetupReq:
    """docstring for RXParamSetupReq"""
    def __init__(self, rx1droffset, rx2datarate, frequency):
        """
        rx1droffset: The RX1DRoffset field sets the offset between the uplink data rate and the downlink data
        rate used to communicate with the end-device on the first reception slot (RX1)

        frequency: corresponds the channel of device's second receive window.
        """
        self.rx1droffset = rx1droffset
        self.rx2datarate = rx2datarate
        self.frequency = frequency
        
    @staticmethod
    def analysis(mac_command_data):
        dlsettings = mac_command_data[0]
        frequency = mac_command_data[1:]

        rx1droffset = (dlsettings >> 4) & 0x07
        rx2datarate = dlsettings & 0x0F

    @staticmethod
    def generate(obj):
        pass


class RXParamSetupAns:
    """docstring for RXParamSetupAns"""
    def __init__(self, rx1droffset_ack, rx2datarate_ack, channel_ack):
        self.rx1droffset_ack = rx1droffset_ack
        self.rx2datarate_ack = rx2datarate_ack
        self.channel_ack = channel_ack
        
    @staticmethod
    def analysis(mac_command_data):
        rx1droffset_ack = (mac_command_data >> 2) & 0x01
        rx2datarate_ack = (mac_command_data >> 1) & 0x01
        channel_ack = mac_command_data & 0x01
        return RXParamSetupAns(rx1droffset_ack, rx2datarate_ack, channel_ack)

    @staticmethod
    def generate(obj):
        pass


class DevStatusReq:
    """docstring for DevStatusReq"""
    def __init__(self):
        pass
        
    @staticmethod
    def analysis(mac_command_data):
        return None

    @staticmethod
    def generate(obj):
        pass


class DevStatusAns:
    """docstring for DevStatusAns"""
    def __init__(self, battery, margin):
        """
        battery: 
            0 means that device is connected to an external power source.
            1-254: means that the battery level of device, 1 being at minimun and 254 is maximun.
            255: means that device is not able to measure the battery level.
        margin: It is a signed integer of 6 bits with a minimum value of -32 
            and a maximum value of 31.
        """
        self.battery = battery
        self.margin = margin
        
    @staticmethod
    def analysis(mac_command_data):
        battery = mac_command_data[0]
        margin = -(mac_command_data[1] & 0x1F) if mac_command_data[1] & 0x20 else mac_command_data[1] & 0x1F
        return DevStatusAns(battery=battery, margin=margin)

    @staticmethod
    def generate(obj):
        pass


class NewChannelReq:
    """docstring for NewChannelReq"""
    # CONST_CHLNDEX_START must according to the chapter 6
    CONST_CHLNDEX_START = int(n) 
    def __init__(self, chlndex, freq, maxdr, mindr):
        """
        chlndex: 
            the index of channels from 0 to CONST_CHLNDEX_START-1 is the default 
            channels which must not be modified and create.Only the index of channels 
            from CONST_CHLNDEX_START to 16 can be modified.
        freq: Here the value is the actual value in packet, still do not *100Hz.
            1.set the channel of the index(chlndex) to the frequency number. The actual
            channel frequency is 100*freq Hz. And the frequency can be set anywhere between
            from 100Mhz to 1.67Ghz in 100Hz step.The frequency below 100Mhz are reserved for
            the furture use.So the range of freq is from 0x0F7270 to 0xFFFFFF.
            2.if the freq num is 0, it means to disable the channel of the index chlndex.
        dr_range: The data-rate range (DrRange) field specifies the uplink data-rate range 
            allowed for this channel.

        """
        self.chlndex = chlndex
        self.freq = freq
        self.maxdr = maxdr
        self.mindr = mindr
        
    @staticmethod
    def analysis(mac_command_data):
        chlndex = mac_command_data[0]
        freq = mac_command_data[1:4]
        dr_range = mac_command_data[4]
        assert NewChannelReq.CONST_CHLNDEX_START <= chlndex <=16,
            'NewChannelReq.chlndex must in the range [%s, 16]' % NewChannelReq.CONST_CHLNDEX_START
        assert 0x0F7270 <= freq <= 0xFFFFFF, 
            'NewChannelReq.freq must in the range [0x0F7270, 0xFFFFFF]'
        maxdr = (dr_range << 4) & 0x0F
        mindr = dr_range & 0x0F
        assert maxdr >= mindr, 'NewChannelReq.maxdr must be more than NewChannelReq.mindr.'
        return NewChannelReq(chlndex=chlndex, freq=freq, maxdr=maxdr, mindr=mindr)

    @staticmethod
    def generate(obj):
        pass


class NewChannelAns:
    """docstring for NewChannelAns"""
    def __init__(self, datarate_range_ack, channel_frequency_ack):
        self.datarate_range_ack = datarate_range_ack
        self.channel_frequency_ack = channel_frequency_ack
        
    @staticmethod
    def analysis(mac_command_data):
        datarate_range_ack = (mac_command_data >> 1) 0x01
        channel_frequency_ack = mac_command_data 0x01
        return NewChannelAns(datarate_range_ack=datarate_range_ack,
                             channel_frequency_ack=channel_frequency_ack)

    @staticmethod
    def generate(obj):
        pass


class DlChannelReq:
    """docstring for DlChannelReq"""
    CONST_CHLNDEX_START = 0
    def __init__(self, chlndex, freq):
        self.chlndex = chlndex
        self.freq = freq
        
    @staticmethod
    def analysis(mac_command_data):
        chlndex = mac_command_data[0]
        freq = mac_command_data[1:4]
        assert DlChannelReq.CONST_CHLNDEX_START <= chlndex <=16,
            'DlChannelReq.chlndex must in the range [%s, 16]' % DlChannelReq.CONST_CHLNDEX_START
        assert 0x0F7270 <= freq <= 0xFFFFFF, 
            'DlChannelReq.freq must in the range [0x0F7270, 0xFFFFFF]'
        return DlChannelReq(chlndex=chlndex, freq=freq)

    @staticmethod
    def generate(obj):
        pass


class DlChannelAns:
    """docstring for DlChannelAns"""
    # The DlChannelReq command allows the network to associate a different downlink
    # frequency to the RX1 slot. 
    def __init__(self, uplink_frequency_ack, channel_frequency_ack):
        self.uplink_frequency_ack = uplink_frequency_ack
        self.channel_frequency_ack = channel_frequency_ack
        
    @staticmethod
    def analysis(mac_command_data):
        uplink_frequency_ack = (mac_command_data >> 1) & 0x01
        channel_frequency_ack = mac_command_data & 0x01
        return DlChannelAns(uplink_frequency_ack=uplink_frequency_ack,
                            channel_frequency_ack=channel_frequency_ack)

    @staticmethod
    def generate(obj):
        pass


class RXTimingSetupReq:
    """
    docstring for RXTimingSetupReq
    The RXTimingSetupReq command allows configuring the delay between the end of
    the TX uplink and the opening of the first reception slot. The second 
    reception slot opens one second(fixed) after the first reception slot.

    """
   
    def __init__(self, delay):
        """
        delay: The value of 0 is 1 seconds. The value of [1,15] is map to 1-15 seconds.
        """
        self.delay = delay
        
    @staticmethod
    def analysis(mac_command_data):
        delay = mac_command_data & 0x0F
        return RXTimingSetupReq(delay=delay)

    @staticmethod
    def generate(obj):
        pass


class RXTimingSetupAns:
    """
    docstring for RXTimingSetupAns
    The RXTimingSetupAns command should be added in the FOpt field of all uplinks until a
    class A downlink is received by the end-device. This guarantees that even in presence of
    uplink packet loss, the network is always aware of the downlink parameters used
    by the end-device.

    """
    def __init__(self):
        pass
        
    @staticmethod
    def analysis(mac_command_data):
        return None 

    @staticmethod
    def generate(obj):
        pass


class TxParamSetupReq:
    """docstring for TxParamSetupReq"""
    MAXEIRP_DBM_LIST = [8, 10, 12, 13, 14, 16, 18, 20, 21, 24, 26, 27, 29, 30, 33, 36]
    MAXEIRP_CODE2DBM_MAP = dict(zip(list(range(16)), MAXEIRP_DBM_LIST))
    def __init__(self, downlink_dwell_time, uplink_dwell_time, max_eirp):
        """
        downlink_dwell_time and uplink_dwell_time define Uplink and downlink dwell time:
            0: dwell time is no limit
            1: dwell time is 400ms
        """
        self.downlink_dwell_time = downlink_dwell_time
        self.uplink_dwell_time = uplink_dwell_time
        self.max_eirp = max_eirp
        
    @staticmethod
    def analysis(mac_command_data):
        downlink_dwell_time = (mac_command_data >> 5) & 0x01
        uplink_dwell_time = (mac_command_data >> 4) & 0x01
        max_eirp = mac_command_data & 0x0F
        return TxParamSetupReq(downlink_dwell_time=downlink_dwell_time,
                               uplink_dwell_time=uplink_dwell_time,
                               max_eirp=max_eirp)

    @staticmethod
    def generate(obj):
        pass


class TxParamSetupAns:
    """
    docstring for TxParamSetupAns
    When this TxParamSetupReq MAC command is used in a region where it is not required,
    the device does not process it and shall not transmit an acknowledgement.
    """
    def __init__(self):
        pass
        
    @staticmethod
    def analysis(mac_command_data):
        return None

    @staticmethod
    def generate(obj):
        pass


"""
Below Mac Command is belong to Class B device.
"""

class PingSlotInfoReq:
    """
    Before device can switch A to B, the answer pingslotinfoans must be received by device.
    And to change its ping slot scheduling or data rate a device should first revert to 
    Class A , send the new parameters through a PingSlotInfoReq command and get an 
    acknowledge from the server through a PinSlotInfoAns . It can then switch back to 
    Class B with the new parameters

    This command must only be used to inform the server of the parameters of 
    a UNICAST ping slot. A multicast slot is entirely defined by the application 
    and should not use this command.
    
    """
    def __init__(self, periodicty, datarate):
        self.periodicty = periodicty
        self.datarate = datarate

    @staticmethod
    def analysis(mac_command_data):
        periodicty = (mac_command_data >> 4) & 0x07
        datarate = mac_command_data & 0x0F
        return PingSlotInfoReq(periodicty, datarate)

    @staticmethod
    def generate(obj):
        pass

class PingSlotInfoAns:
    def __init__(self):
        pass

    @staticmethod
    def analysis(mac_command_data):
        return None

    @staticmethod
    def generate(obj):
        pass

class BeaconFreqReq:
    def __init__(self, frequency):
        """
        frequency: 
            0: use the default beacon frequency plan .
        """
        self.frequency = frequency

    @staticmethod
    def analysis(mac_command_data):
        assert len(mac_command_data) == 3, 'BeaconFreqReq.frequency must be 3 bytes data.'
        frequency = mac_command_data
        assert 0x0F7270 <= frequency <= 0xFFFFFF, 
            'BeaconFreqReq.frequency must in the range [0x0F7270, 0xFFFFFF]'
        return BeaconFreqReq(frequency)

    @staticmethod
    def generate(obj):
        pass


class PingSlotChannelReq:
    def __init__(self, frequency, max_data_rate, min_data_rate):
        self.frequency = frequency
        self.max_data_rate = max_data_rate
        self.min_data_rate = min_data_rate

    @staticmethod
    def analysis(mac_command_data):
        frequency = mac_command_data[:3]
        DrRange = mac_command_data[3]
        max_data_rate = (DrRange >> 4) & 0x0F
        min_data_rate = DrRange & 0x0F
        return PingSlotChannelReq(frequency=frequency)

    @staticmethod
    def generate(obj):
        pass


class PingSlotChannelAns:
    def __init__(self, datarate_range_ack, channel_frequency_ack):
        self.datarate_range_ack = datarate_range_ack
        self.channel_frequency_ack = channel_frequency_ack

    @staticmethod
    def analysis(mac_command_data):
        datarate_range_ack = (mac_command_data >> 1) & 0x01
        channel_frequency_ack = mac_command_data & 0x01
        return PingSlotChannelAns(datarate_range_ack=datarate_range_ack,
                                  channel_frequency_ack=channel_frequency_ack)

    @staticmethod
    def generate(obj):
        pass


class BeaconTimingReq:
    """
    This command is sent by the end-device to request the next beacon timing and channel.
    This MAC command has no payload.
     An end-device must not expect that BeaconTimingReq is answered immediately with a BeaconTimingAns

    """
    def __init__(self):
        pass

    @staticmethod
    def analysis(mac_command_data):
        return None

    @staticmethod
    def generate(obj):
        pass


class BeaconTimingAns:
    def __init__(self, delay, channel):
        """
        delay: 16 bits unsigned data. 
            RTime: the remaining time between the end of the current downlink frame(carrying 
            BeaconTimingAns mac command ) and the start of the next beacon frame.
            It will 30 ms x (Delay+1) > RTime >= 30 ms x Delay.
        channel: 
            0: fixed channel.
            other int number: the next beacon will be sent by other channel 
                and the number is the index of the beacon broadcast channel.

        """
        self.delay = delay
        self.channel = channel

    @staticmethod
    def analysis(mac_command_data):
        delay = mac_command_data[:2]
        channel = mac_command_data[2]
        return BeaconTimingAns(delay, channel)

    @staticmethod
    def generate(obj):
        pass

