
class LoraProtocol:


    class Method:
        @staticmethod
        def analysis(data_dict):
            major = data[0] & 0b11
            if major != 0:
                Logger.error(action=Action.uplink, msg='ERROR: Major != 0, Major = %s' % major)
                continue
            mtype = data[0] >> 5
            if mtype == MType.JOIN_REQUEST:
                # try:
                #     otaa = OTAAJoin(request_msg=data, trans_params=data_raw, gateway=gateway)
                #     otaa.start()
                # except Exception as error:
                #     Logger.error(action=Action.otaa, msg='REQUEST: %s; ERROR: %s' % (data, error))
                pass
            elif mtype == MType.UNCONFIRMED_DATA_UP or mtype == MType.CONFIRMED_DATA_UP:
                # dev_addr = endian_reverse(data[1:5])
                # device = Device.objects.get_device_by_addr(dev_addr)
                # if device is None:
                #     Logger.error(action=Action.data_up, type=IDType.dev_addr, id=hexlify(dev_addr).decode(), msg='Can\'t Find Device for this DevAddr')
                #     continue
                # if gateway.public is not True and device.app.user_id != gateway.user_id:
                #     Logger.error(action=Action.data_up, msg='Gateway %s is not Public and device % s is not belong to the same user' % (gateway.mac_addr, device.dev_eui))
                #     continue
                # ReadDataUp(device.dev_eui, gateway, data_raw, mtype, data, *args).start()
                pass
            elif mtype == MType.UNCONFIRMED_DATA_DOWN or mtype == MType.CONFIRMED_DATA_DWON:
                # dev_addr = endian_reverse(data[1:5])
                # device = Device.objects.get_device_by_addr(dev_addr)
                # if device is None:
                #     Logger.error(action=Action.data_up, type=IDType.dev_addr, id=hexlify(dev_addr).decode(), msg='Can\'t Find Device for this DevAddr')
                #     continue
                # if gateway.public is not True and device.app.user_id != gateway.user_id:
                #     Logger.error(action=Action.data_up, msg='Gateway %s is not Public and device % s is not belong to the same user' % (gateway.mac_addr, device.dev_eui))
                #     continue
                # ReadDataUp(device.dev_eui, gateway, data_raw, mtype, data, *args).start()
                
            elif mtype == MType.PTY:
                # dev_addr == endian_reverse(data[1:5])
                # device = Device.objects.get_device_by_addr(dev_addr)
                # if device is None:
                #     Logger.error(action=Action.proprietary, type=IDType.dev_addr, id=hexlify(dev_addr).decode(), msg='Can\'t Find Device for this DevAddr')
                # ReadPTY(dev_eui=device.dev_eui, gateway=gateway, trans_params=data_raw, mtype=mtype, data=data).start()
                pass




class Fields:
    class Major:
        LoRaWAN_R1 = 'LoRaWAN_R1'
        rfu = 'rfu'  # from 0x01 - 0x03
        map_dict = {
            0x00: LoRaWAN_R1
        }
    
    class MType:
        join_request = 'join_request'
        join_accept = 'join_accept'
        unconfirmed_data_up = 'unconfirmed_data_up'
        unconfirmed_data_down  = 'unconfirmed_data_down'
        confirmed_data_up = 'confirmed_data_up'
        confirmed_data_down = 'confirmed_data_down'
        rfu = 'rfu'
        proprietary = 'proprietary'
        map_dict = {
                0x00: join_request,
                0x01: join_accept,
                0x02: unconfirmed_data_up,
                0x03: unconfirmed_data_down,
                0x04: confirmed_data_up,
                0x05: confirmed_data_downS
            }
        @staticmethod
        def get_deal_method(mtype_data):
            return dealfun[Fields.MType.map_dict[mtype_data]] 

dealfun = {
    Fields.MType.join_request: , 
    Fields.MType.join_accept: ,   
}

class Const:

    JOIN_SERVER_ADDR = ('localhost', 8800)
    DIR_UP = 0
    DIR_DOWN = 1

    GATEWAY_CONFIG_IDENTIFIER = b'\x05'
    GATEWAY_CONFIG_RESQ_IDENTIFIER = b'\x06'

    # PROTOCOL_VERSION = b'\x01'
    PUSH_DATA_IDENTIFIER = 0x00
    PUSH_ACK_IDENTIFIER = b'\x01'
    PULL_DATA_IDENTIFIER = 0x02
    PULL_RESP_IDENTIFIER = b'\x03'
    PULL_ACK_IDENTIFIER = b'\x04'
    TX_ACK_IDENTIFIER = 0X05

    UNUSED_BYTE = b'\x00'

    MHDR_RFU = 0B000

    MAJOR_LORA = 0B00

    MAX_FCNT_GAP = 16384

    MTypes = {0b000: 'Join Request',
              0b001: 'Join Accept',
              0b010: 'Unconfirmed Data Up',
              0b011: 'Unconfirmed Data Dwon',
              0b100: 'Confirmed Data Up',
              0b101: 'Confirmed Data Down',
              0b110: 'RFU',
              0b111: 'Proprietary'}

    Major = {0b00: 'LoRaWAN R1',
             0b01: 'RFU',
             0b10: 'RFU',
             0b11: 'RFU'}

    MAX_RESEND_NUM = 8

    IGNORE_DATA = b'\x00'
    PROCESS_DATA = b'\x01'

    EU868_MAX_PAYLOAD_LEN = 51

    CONNECTION_TIMEOUT = 60


class MType(IntEnum):
    JOIN_REQUEST = 0B000
    JOIN_ACCEPT = 0B001
    UNCONFIRMED_DATA_UP = 0B010
    UNCONFIRMED_DATA_DOWN = 0B011
    CONFIRMED_DATA_UP = 0B100
    CONFIRMED_DATA_DOWN = 0B101
    RFU = 0B110
    PTY = 0B111  # Proprietary


class EU863_870:
    DataRate = {
        0: 'SF12BW125',
        1: 'SF11BW125',
        2: 'SF10BW125',
        3: 'SF9BW125',
        4: 'SF8BW125',
        5: 'SF7BW125',
        6: 'SF7BW250',
    }
    BEACON_FREQ = 869.525