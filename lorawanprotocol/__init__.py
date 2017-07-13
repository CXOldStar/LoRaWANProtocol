

class AbsortObject:
    def __init__(self, mtype, dev_addr, mac_command, lorawan_mac_test, app_payload, fcnt, ack, class_b
        do_mic_check=None, do_decrypto_check=None):
        self.mtype = mtype
        self.dev_addr = dev_addr
        self.mac_command = mac_command
        self.lorawan_mac_test = lorawan_mac_test
        self.app_payload = app_payload
        self.fcnt = fcnt
        self.ack = ack
        self,class_b = class_b
        self.do_mic_check = do_mic_check
        self.do_decrypto_check = do_decrypto_check

    @staticmethod
    def generate(phypayload_init, do_mic_check=None, do_decrypto_check=None):
        mtype = phypayload_init.mhdr.mtype
        dev_addr = phypayload_init.mac_payload.fhdr.dev_addr
        fcnt = phypayload_init.mac_payload.fhdr.fcnt
        mac_command = None
        app_payload = None
        lorawan_mac_test = None
        if phypayload_init.mac_payload.fhdr.fopts is not None:
            mac_command = phypayload_init.mac_payload.fhdr.fopts
        if not phypayload_init.mac_payload.frmpayload:
            pass
        else:
            payload = phypayload_init.mac_payload.frmpayload.data
            if phypayload_init.mac_payload.frmpayload.mac_command is not None:
                mac_command = payload
            elif phypayload_init.mac_payload.frmpayload.lorawan_mac_test is not None:
                lorawan_mac_test = payload
            elif phypayload_init.mac_payload.frmpayload.app_payload is not None:
                app_payload = payload
            else:
                app_payload = None
        ack = phypayload_init.mac_payload.fhdr.fctrl.ack
        class_b = phypayload_init.mac_payload.fhdr.fctrl.class_b
        return AbsortObject(mtype=mtype, dev_addr=dev_addr, mac_command=mac_command,
            lorawan_mac_test=lorawan_mac_test, app_payload=app_payload, fcnt=fcnt, ack=ack, class_b=class_b
            do_mic_check=do_mic_check, do_decrypto_check=do_decrypto_check)

