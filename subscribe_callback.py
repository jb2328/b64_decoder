#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation

# This shows an example of using the subscribe.callback helper function.

#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.subscribe as subscribe
import decoder
import json
import importlib

DEBUG=False

def printf(a):
    if(DEBUG):
        print(a)

def importNewLibs():
    tree = os.listdir('modules')
    for i in tree:
        importlib.import_module(i)

def print_msg(client, userdata, message):
    #print("%s : %s" % (message.topic, message.payload))

    printf("\nincoming\n")

    dict_obj={}

    try:
        printf(message)
        inc_msg=str(message.payload,'utf-8')
        printf(inc_msg)

        msg_json=json.loads(inc_msg)

        printf(msg_json)
        printf("\nDECODED:\n")

        rawb64=msg_json["payload_raw"]
        decoded=decoder.DecodeElsysPayload(decoder.b64toBytes(rawb64))

        printf(rawb64)
        printf(decoded)

        dev_id=msg_json["dev_id"]

        printf(dev_id)

        time=msg_json["metadata"]["time"]

        printf(time)
        
        printf("\nFINITO:\n")

        dict_obj["time"]=time
        dict_obj["dev_id"]=dev_id
        dict_obj["payload"]=decoded

        print(json.dumps(dict_obj))

    except:

        printf("\nfailed with the following:\n")
        print(json.dumps(msg_json))
        printf("\n")
        printf(rawb64)
        printf(dev_id)
        printf(time)

subscribe.callback(print_msg, "cambridge-sensor-network/devices/elsys-eye-044501/#", hostname="eu.thethings.network", auth={'username':"cambridge-sensor-network", 'password':"ttn-account-v2.7Bg6NW0rWeNwgkhyVfKmutJx3nDwR-R_SoLpB9KyzE4"})
