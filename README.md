# iot-device-python
The minimal code for an IoT device to connect to an Azure IoTHub in python

## Setup

For Python 2.7 run the following:

```bash
$ pip install azure-iothub-device-client
```

For Python3 run the following:

```bash
$ pip3 install azure-iothub-device-client
```

finally, run the following to get a copy of this code

```bash
$ git clone https://github.com/seank-com/iot-device-python.git
$ cd iot-device-python
```

## Run

To run first edit the device.py file in your favorite editor to set the connection string then run the following

```bash
$ python device.py
```

If you see an error like the following 

```bash
$ python device.py
Traceback (most recent call last):
  File "device.py", line 5, in <module>
    import iothub_client
  File "/home/ubuntu/.local/lib/python2.7/site-packages/iothub_client/__init__.py", line 1, in <module>
    from .iothub_client import *
ImportError: libboost_python-py27.so.1.58.0: cannot open shared object file: No such file or directory
```

run

```bash
$ sudo apt-get install libboost-all-dev curl libcurl3
```

## Notes

if you would like to install python3 run the following:

```bash
$ sudo apt-get install python3=3.5.1*
```
