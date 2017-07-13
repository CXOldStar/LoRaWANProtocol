from distutils.core import setup

setup(
    name='lorawanprotocol',
    version='0.0.1',
    packages=['', 'lorawanprotocol'],
    url='https://github.com/CXOldStar/lorawanprotocol',
    license='MIT',
    author='ChenXing',
    author_email='cxoldstar@gmail.com',
    description='The package can analysis parameter of the standard lorawan protocol(Now support 1.02 version) from lorawan data，including mac command, payload and so on. The input data are bytes and output is a PHYPayload object.'
)
