from .customer_error import AssertError

class AssertJudge:
    @staticmethod
    def assert_nwkskey(nwkskey):
        if not (isinstance(nwkskey, bytes) and len(nwkskey) == 16):
            raise AssertError('NwkSKey', 'NwkSKey must be a 16 bytes data.')

    @staticmethod
    def assert_appskey(appskey):
        if not (isinstance(appskey, bytes) and len(appskey) == 16):
            raise AssertError('AppSKey', 'AppSKey must be a 16 bytes data.')

    @staticmethod
    def assert_appkey(appkey):
        if not (isinstance(appkey, bytes) and len(appkey) == 16):
            raise AssertError('AppKey', 'AppKey must be a 16 bytes data.')
