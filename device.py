#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

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

SLEEP_TIME = 5000

def receive_message_callback(message, counter):
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "Received Message [%d]:" % counter )
    print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    return IoTHubMessageDispositionResult.ACCEPTED

def send_confirmation_callback(message, result, user_context):
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    print ( "    message_id: %s" % message.message_id )
    print ( "    correlation_id: %s" % message.correlation_id )
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )

def print_last_message_time(client):
    try:
        last_message = client.get_last_message_receive_time()
        print ( "Last Message: %s" % time.asctime(time.localtime(last_message)) )
        print ( "Actual time : %s" % time.asctime() )
    except IoTHubClientError as iothub_client_error:
        if iothub_client_error.args[0].result == IoTHubClientResult.INDEFINITE_TIME:
            print ( "No message received" )
        else:
            print ( iothub_client_error )

def iothub_client_sample_run():

    try:

        # prepare iothub client
        client = IoTHubClient(CONNECTION_STRING, IoTHubTransportProvider.MQTT)
        # to enable MQTT logging set to 1
        client.set_option("logtrace", 0)
        client.set_message_callback(receive_message_callback, RECEIVE_CONTEXT)

        while True:
            # send a few messages every minute
            print ( "IoTHubClient sending %d messages" % MESSAGE_COUNT )

            msg_txt_formatted = MSG_TXT % "This is a test"
            message = IoTHubMessage(msg_txt_formatted)

            client.send_event_async(message, send_confirmation_callback, message_counter)
            print ( "IoTHubClient.send_event_async accepted message for transmission to IoT Hub." )

            time.sleep(SLEEP_TIME)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

    print_last_message_time(client)

if __name__ == '__main__':
    print ( "\nPython %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    iothub_client_sample_run()
