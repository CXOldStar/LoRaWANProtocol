from .customer_error import FHDRError
from .mac_command import MacCommand
from .const import MacCID, MType

class MACPayload:
    def __init__(self, fhdr, fport, frmpayload):
        self.fhdr = fhdr
        self.fport = fport
        self.frmpayload = frmpayload

    @staticmethod
    def get(msg_type, macpayload_data):
        # The first octets of macpayload_data is MHDR.
        fhdr_init = FHDR.get_fhdr(msg_type, macpayload_data)
        data = FPort.get(macpayload_data, fhdr_init)
        if data is None:
            fport = None
            frmpayload = None
        elif isinstance(data, list):
            fport = data[0]
            frmpayload = data[1]
        else:
            fport = None
            frmpayload = None
            raise MacRepeatError
        return MACPayload(fhdr=fhdr_init, fport=fport, frmpayload=frmpayload)


class FHDR:
    def __init__(self, dev_addr, fctrl, fcnt, fopts):
        self.dev_addr = dev_addr
        self.fctrl = fctrl
        self.fcnt = fcnt
        self.fopts = fopts

    @staticmethod
    def get_fhdr(msg_type, fhdr_data):
        dev_addr = int.to_bytes(int.from_bytes(fhdr_data[1:5], byteorder='little'),
                                length=4, byteorder='big')
        fctrl = fhdr_data[5]
        fcnt = int.from_bytes(fhdr_data[6:8], byteorder='little')
        fctrl_init = FHDR.FCtrl.get_fctrl(msg_type, fctrl)
        if fctrl_init.foptslen <= 16 and fctrl_init.foptslen >= 0:
            if fctrl_init.foptslen == 0:
                fopts = None
            else:
                fopts_data = fhdr_data[8:(8 + int(fctrl_init.foptslen))]
                fopts = MacCommand.analysis(
                    msg_type=msg_type,
                    mac_command_data=fopts_data
                )
        else:
            raise FHDRError('foptslen', 'foptslen must be in [0, 16]')
        return FHDR(dev_addr=dev_addr, fctrl=fctrl_init, fcnt=fcnt,
                    fopts=fopts)

    class FCtrl:
        def __init__(self, adr, ack, adr_ack_req, fpending, class_b, foptslen):
            """
            fpending is only can be used in downlink message.
            In uplink, fpending means the class b signal bit.
            adr_ack_req is  RFU in downlink and only can be used in uplink message.
            
            If foptslen > 0, FPort must different from 0 or not present and there is mean
            that mac command exist.
            If foptslen = 0, fopts is empty and mac command can only exist in FRMPayload, 
            because mac command cannot be simultaneously present in the payload field(FRMPayload) 
            and the frame options field(FOpts).
            """
            self.adr = adr
            self.ack = ack
            self.adr_ack_req = adr_ack_req
            self.fpending = fpending
            self.class_b = class_b
            self.foptslen = foptslen

        @staticmethod
        def get_fctrl(msg_type, fctrl_data):
            adr = (fctrl_data & 0x80) >> 7
            # adr_ack_req = (fctrl_data & 0x40) >> 6
            ack = (fctrl_data & 0x20) >> 5
            # fpending = (fctrl_data & 0x10) >> 4
            foptslen = (fctrl_data & 0x0f)
            adr_ack_req = None
            class_b = None
            fpending = None
            if msg_type == MType.CONFIRMED_DATA_UP or msg_type == MType.UNCONFIRMED_DATA_UP:
                adr_ack_req = (fctrl_data & 0x40) >> 6
                class_b = (fctrl_data & 0x10) >> 4
            else:
                fpending = (fctrl_data & 0x10) >> 4
            return FHDR.FCtrl(adr=adr, adr_ack_req=adr_ack_req, ack=ack, fpending=fpending, class_b=class_b, foptslen=foptslen)

        def rename_attribute(self, old_name, new_name):
            self.__dict__[new_name] = self.__dict__.pop(old_name)

    
class FPort:
    def __init__(self, fport):
        """
        FRMPayload is empty or not decides that wheter FPort exist or not .
        If fport is 0, it means that FRMPayload contains MAC command only.
        If fport is [1, 233] (0x01..0xDF) , it means that FRMPayload is application specific.
        If fport is 244(0xE0), it means that LoRaWAN Mac layer test protocol.
        If fport is [225, 255](0xE1..0xFF), it means that RFU.
        """
        self.fport = fport

    @staticmethod
    def get(macpayload_data, fhdr_init):
        fhdr_len = fhdr_init.fctrl.foptslen + 7 + 1
        if len(macpayload_data) > fhdr_len:
            fport = macpayload_data[fhdr_len]
            if fport == 0:
                if fhdr_init.fopts is not None:
                    # ignore the message.
                    raise MacRepeatError
                mac_command = macpayload_data[fhdr_len+1:]
                return [fport, FRMPayload(data=mac_command, mac_command=True)]
            elif 1 <= fport <= 233:
                app_payload = macpayload_data[fhdr_len+1:]
                return [fport, FRMPayload(data=app_payload, app_payload=True)]
            elif fport == 244:
                lorawan_mac_test = macpayload_data[fhdr_len+1:]
                return [fport, FRMPayload(data=lorawan_mac_test, lorawan_mac_test=True)]
            else:
                payload = None
                return [fport, FRMPayload(data=payload)]
        else:
            return None


class FRMPayload:
    def __init__(self, data, mac_command=None, app_payload=None, lorawan_mac_test=None):
        self.data = data
        self.mac_command = mac_command
        self.app_payload = app_payload
        self.lorawan_mac_test = lorawan_mac_test


class MacRepeatError(Exception):

    def __str__(self):
        return 'Mac command can not exist in FRMPayload and FOpts at the same time.\n'