class MHDRError(Exception):
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message

    def __str__(self):
        return 'MHDR Error.\n' +\
               '%s : %s' % (self.field_name, self.message)


class MICError(Exception):
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message

    def __str__(self):
        return 'MIC Error.\n' +\
               '%s : %s' % (self.field_name, self.message)

class FHDRError(Exception):
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message

    def __str__(self):
        return 'FHDRError Error.\n' +\
               '%s : %s' % (self.field_name, self.message)


class DeCryptoError(Exception):
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message

    def __str__(self):
        return 'DeCrypto Error.\n' +\
               '%s : %s' % (self.field_name, self.message)

class AssertError:
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message

    def __str__(self):
        return 'AssertError:\n' +\
                '%s : %s' % (self.field_name, self.message)