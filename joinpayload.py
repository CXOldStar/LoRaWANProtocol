from .lora_crypto import LoRaCrypto
from .assert_judge import AssertJudge


class JoinRequest:
    def __init__(self, app_eui, dev_eui, dev_nonce):
        """
        dev_nonce:it  must not repeat in the same join request.
            And server will ignore the request containing any past
            dev_nonce.The dev_nonce can be reset after the device
            join success.
        """
        self.app_eui = app_eui
        self.dev_eui = dev_eui
        self.dev_nonce = dev_nonce

    @staticmethod
    def get(join_payload):
        app_eui = join_payload[:8]
        dev_eui = join_payload[8:16]
        dev_nonce = join_payload[16:18]
        return JoinRequest(app_eui=app_eui, dev_eui=dev_eui, dev_nonce=dev_nonce)


class JoinAccept:
    def __init__(self, app_nonce, net_id, dev_addr, rx1_droffset,
                 rx2_datarate, rx_delay, cf_list, nwkskey, appskey):
        self.app_nonce = app_nonce
        self.net_id = net_id
        self.dev_addr = dev_addr
        self.rx1_droffset = rx1_droffset
        self.rx2_datarate = rx2_datarate
        self.rx_delay = rx_delay
        self.cf_list = cf_list
        self.appskey = appskey
        self.nwkskey = nwkskey

    @staticmethod
    def get(join_payload, appkey, dev_nonce):
        """"
        Each device should have a unique set of NwkSKey and AppSKey.Also as the appkey.
        """
        app_nonce = join_payload[:3]
        net_id = join_payload[3:6]
        dev_addr = join_payload[6:10]
        dl_settings = join_payload[10]
        rx_delay = join_payload[11]
        cf_list = join_payload[12:]

        rx1_droffset = (dl_settings >> 4) & 0x07
        rx2_datarate = dl_settings & 0x0F

        nwkskey, appskey = LoRaCrypto.join_compute_skey(key=appkey, appNonce=app_nonce + net_id, devNonce=dev_nonce)
        return JoinAccept(app_nonce=app_nonce, net_id=net_id, dev_addr=dev_addr, rx1_droffset=rx1_droffset,
                          rx2_datarate=rx2_datarate, rx_delay=rx_delay, cf_list=cf_list, 
                          nwkskey=nwkskey, appskey=appskey)
