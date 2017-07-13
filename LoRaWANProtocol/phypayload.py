from .lora_crypto import LoRaCrypto
from .const import Const, MType
from .macpayload import MACPayload
from .mac_command import MacCommand
from .customer_error import MHDRError, MICError, DeCryptoError
from .assert_judge import AssertJudge
from . import AbsortObject
from .joinpayload import JoinAccept, JoinRequest


class PHYPayload:

    def __init__(self, mhdr, mic, dir_value=None, check_mic_msg=None,
                 mac_payload=None, join_request=None, join_accept=None,
                 do_mic_check=None, do_decrypto_check=None):
        self.mhdr = mhdr
        self.mic = mic
        self.mac_payload = mac_payload
        self.join_request = join_request
        self.join_accept = join_accept
        self.dir_value = dir_value
        self.check_mic_msg = check_mic_msg
        # self.decrypto_data = decrypto_data
        self.do_mic_check = do_mic_check
        self.do_decrypto_check = do_decrypto_check

    @staticmethod
    def analysis(phypayload, NwkSKey=None, AppSKey=None, AppKey=None, dev_nonce=None):
        mhdr = phypayload[0]
        mic = phypayload[-4:]
        mhdr_init =  MHDR.get(mhdr)
        if mhdr_init.mtype == MType.JOIN_REQUEST:
            join_payload = phypayload[1:-4]
            mic = phypayload[-4:]
            check_mic_msg = phypayload[:-4]
            join_request_init = JoinRequest.get(join_payload)
            return_init = PHYPayload(mhdr=mhdr_init, mic=mic, check_mic_msg=check_mic_msg,
                                     join_request=join_request_init)
        elif mhdr_init.mtype == MType.JOIN_ACCEPT:
            AssertJudge.assert_appkey(AppKey)
            decrypto_data = LoRaCrypto.join_decrypt(phypayload[1:], AppKey)
            join_payload = decrypto_data[:-4]
            mic = decrypto_data[-4:]
            check_mic_msg = decrypto_data[:-4]
            join_accept_init = JoinAccept.get(join_payload, AppKey, dev_nonce)
            return_init = PHYPayload(mhdr=mhdr_init, mic=mic, check_mic_msg=check_mic_msg,
                                     join_accept=join_accept_init)
        elif mhdr_init.mtype == MType.CONFIRMED_DATA_UP or mhdr_init.mtype == MType.UNCONFIRMED_DATA_UP:
            dir_value = Const.DIR_UP

            # macpayload_init = MACPayload.get_up(phypayload[:-4])
            macpayload_init = MACPayload.get(mhdr_init.mtype, phypayload[:-4])
            # In down link, the adr_ack_req of fpending is RFU.
            macpayload_init.fhdr.fctrl.rename_attribute('fpending', 'rfu')
            
            return_init = PHYPayload(mhdr=mhdr_init, mic=mic, mac_payload=macpayload_init,
                                     dir_value=dir_value, check_mic_msg=phypayload[:-4])
        elif mhdr_init.mtype == MType.CONFIRMED_DATA_DOWN or mhdr_init.mtype == MType.UNCONFIRMED_DATA_DOWN:
            dir_value = Const.DIR_DOWN

            # macpayload_init = MACPayload.get_down(phypayload[:-4])
            macpayload_init = MACPayload.get(mhdr_init.mtype, phypayload[:-4])
            # In down link, the adr_ack_req of fctrl is RFU.
            macpayload_init.fhdr.fctrl.rename_attribute('adr_ack_req', 'rfu')
            
            return_init = PHYPayload(mhdr=mhdr_init, mic=mic, mac_payload=macpayload_init,
                                     dir_value=dir_value, check_mic_msg=phypayload[:-4])
        elif mhdr_init.mtype == MType.PTY:
            pass
        if NwkSKey is not None:
            return_init.check_mic(NwkSKey)
            if return_init.do_mic_check and return_init.mac_payload is not None:
                # The join request or join accept do not use this decrypto and mac command.
                return_init.decrypto_payload(NwkSKey=NwkSKey, AppSKey=AppSKey)
                return_init.deal_frmpayload_mac_command()
        return return_init
        
    def check_mic(self, NwkSKey):
        AssertJudge.assert_nwkskey(NwkSKey)
        if self.mac_payload:
            # dev_addr = int.to_bytes(int.from_bytes(self.mac_payload.fhdr.dev_addr, byteorder='little'),
            #                         length=4, byteorder='big')
            dev_addr = int.from_bytes(self.mac_payload.fhdr.dev_addr, byteorder='big')
            fcnt = self.mac_payload.fhdr.fcnt
            c_mic = LoRaCrypto.compute_mic(
                msg=self.check_mic_msg, key=NwkSKey, address=dev_addr, 
                dir=self.dir_value, sequenceCounter=fcnt
            )
        elif self.join_request is not None or self.join_accept is not None:
            c_mic = LoRaCrypto.join_compute_mic(self.check_mic_msg, key=NwkSKey)
        if c_mic != self.mic:
            self.do_mic_check = False
            raise MICError('mic', 'compute mic is not equal with the mic in phypayload.')
        else:
            self.do_mic_check = True

    def decrypto_payload(self, NwkSKey=None, AppSKey=None):
        if AppSKey is None or AppSKey is None:
            self.do_decrypto_check = False
            return False
        if self.mac_payload.frmpayload is not None and self.mac_payload.frmpayload.data is not None:
            if self.mac_payload.fport == 0:
                AssertJudge.assert_nwkskey(NwkSKey)
                key = NwkSKey
            else:
                AssertJudge.assert_appskey(AppSKey)
                key = AppSKey
            decry_data = LoRaCrypto.payload_decrypt(
                encbuffer=self.mac_payload.frmpayload.data,
                key=key,
                address=int.from_bytes(self.mac_payload.fhdr.dev_addr, byteorder='big'),
                dir=self.dir_value,
                sequenceCounter=self.mac_payload.fhdr.fcnt
                )
            self.mac_payload.frmpayload.data = decry_data
            self.do_decrypto_check = True
        else:
            self.do_decrypto_check = True
        return True

    def deal_frmpayload_mac_command(self):
        if self.do_decrypto_check and self.mac_payload.frmpayload.data is not None and self.mac_payload.frmpayload.mac_command is not None:
            mac_command_init = MacCommand.analysis(
                    msg_type=self.mhdr.mtype,
                    mac_command_data=self.mac_payload.frmpayload.data
            )
            self.mac_payload.frmpayload.data = mac_command_init
        # the mac command in mac_payload.fhdr.fopts has switch to object in the macpayload.py
        # elif self.mac_payload.fhdr.fopts is not None:
        #     mac_command_init = MacCommand.analysis(
        #             msg_type=self.mhdr.mtype,
        #             mac_command_data=self.mac_payload.fhdr.fopts
        #     )
        #     self.mac_payload.fhdr.fopts = mac_command_init

    def absort(self):
        absort_data = AbsortObject.generate(self,
                                            do_mic_check=self.do_mic_check,
                                            do_decrypto_check=self.do_decrypto_check)
        return absort_data


class MHDR:
    def __init__(self, mtype, rfu, major):
        self.mtype = mtype
        self.rfu = rfu
        self.major = major

    @staticmethod
    def get(mhdr):
        major = mhdr & 0b11
        if major != 0:
            raise MHDRError('major', 'value(%s) error.Must be 0.' % major)
        mtype = mhdr >> 5
        rfu = (mhdr & 0x1C) >> 2
        return MHDR(mtype=mtype, rfu=rfu, major=major)


