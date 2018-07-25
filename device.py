#!/usr/bin/env python

import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

# String containing Hostname, Device Id & Device Key in the format:
# "HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>"
CONNECTION_STRING = "[Device Connection String]"

MSG_TXT = "{\"msg\": \"%s\"}"

RECEIVE_CONTEXT = 0
SEND_CONTEXT = 0

SLEEP_TIME = 15

def receive_message_callback(message, user_context):
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "Received Message:  data = \"%s\" size=%d" % (message_buffer[:size].decode('utf-8'), size) )
    return IoTHubMessageDispositionResult.ACCEPTED

def send_confirmation_callback(message, result, user_context):
    print ( "Confirmation received for message with result = %s" % result )

def iothub_client_sample_run():

    try:
        # prepare iothub client
        client = IoTHubClient(CONNECTION_STRING, IoTHubTransportProvider.MQTT)
        # to enable MQTT logging set to 1
        client.set_option("logtrace", 0)
        client.set_message_callback(receive_message_callback, RECEIVE_CONTEXT)

        while True:
            # send a few messages every minute
            print ( "IoTHubClient sending message" )

            msg_txt_formatted = MSG_TXT % "This is a test"
            message = IoTHubMessage(msg_txt_formatted)

            client.send_event_async(message, send_confirmation_callback, SEND_CONTEXT)
            print ( "IoTHubClient.send_event_async accepted message for transmission to IoT Hub." )

            time.sleep(SLEEP_TIME)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "\nPython %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    iothub_client_sample_run()
