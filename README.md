# lorawanprotocol
The package can analysis parameter of the standard lorawan protocol(1.02) from lorawan data，including mac command, payload and so on.
The input data are bytes and output is a PHYPayload object.

# Install
1. Download the package.
2. To use the ASE128 encrypto function, you need to run below command to generate the libloraCrypto.so:
    ```
    $ cd lora_encrypt
    $ make so
    ```
3. Run the below command after generate the libloraCrypto.so:
    ```
    $ python3 setup.py install
    ```

# Usage

## Simple example:
```
>>> from lorawanprotocol.phypayload import PHYPayload
>>> phypayload = PHYPayload.analysis(your_phypaylaod_data)
>>> absort_data = phypayload.absort()
```

## Description
### class PHYPayload
- Fields:
    - mdhr
        - Defined in lorawan protocol.
        - 1 bytes data.

    - mic
        - Used to check phypayload.
        - 4 Bytes data.

    - mac_payload
        - Default is None.
        - If the message is confirm/unconfirm data, it is a MACPayload object.

    - join_request
        - Default is None.
        - If the message is a join request data, it is a JoinRequest object.

    - join_accept
        - Default is None
        - If the message is a join accept data, it is a JoinAccept object.

    - dir_value
        - Define in lorawan protocol.
        - Uplink data is 0, downlink is 1.

    - do_mic_check
        - Default is None.
        - None value means that it still does not check the phypayload.
        - True value means the mic is right.
        - False value means that the mic is error and will raise a MICError.

    - do_decrypto_check
        - Default is None.
        - None value means that frmpayload still does not decrypto the data in frmpayload.
        - True value means that frmpayload decrypto successful.
        - False value means that frmpayload needs session keys.

- analysis(phypayload, NwkSKey=None, AppSKey=None, AppKey=None, dev_nonce=None):
    - Return a PHYPayload object.
    - phypayload is the bytes data and must not be None.
    - NwkSKey, AppSKey, AppKey, dev_nonce should be special values according different situation.And all of them are bytes data.

- absort()
    - Return AbsortObject object
    - To generate AbsortObject which only has common data.

### class AbsortObject:
- Fields:
    - mtype
        - message type 
        - Value is defined in lorawan protocol.

    - dev_addr
        - device address
        - 4 bytes data.
    - mac_command
        - Default None.
        - If the message contains a mac command, it is a MacCommand object.

    - lorawan_mac_test
        - Default None.
        - Defined in lorawan protocol.
        - If the message contains a lorawan_mac_test, there are bytes data.

    - app_payload
        - Default None.
        - If the message contains the data of application layer, there are bytes data for application layer.
    - fcnt
        - the fcnt_up/fcnt_down of the current message.
        - Int type.
    - ack
        - Signal this is an ack message.
    - class_b
        - Signal the message is sent by a class B device.
    - do_mic_check
        - Same as in class PHYPayload
    - do_decrypto_check
        - Same as in class PHYPayload

