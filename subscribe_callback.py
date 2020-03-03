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
#import elsysDecoder as decoder
import json
import secrets
import importlib
import time
import os

DEBUG=True

def printf(a):
    if(DEBUG):
        print(a)


def save_to_file(data):

    ts=str(time.strftime("%H:%M-%d-%m-%Y"))
    unix_ts=str(int(time.time()))
    filename=unix_ts+"_"+ts+".json"

    # define the name of the directory to be created
    path = str(os.getcwd())+str(time.strftime("/data_bin/%Y/%m/%d/"))
    printf("Attempting to save in %s" %path)
    try:
        os.makedirs(path)
    except OSError:
        printf ("Creation of the directory %s failed" % path)
    else:
        printf ("Successfully created the directory %s" % path)

    f= open(path+filename,"w+")
    f.write(str(data))
    f.close()
    printf("File was written %s" %(path+filename))

def import_all_libs():
    tree = os.listdir('modules')
    print(tree)
    for i in tree:
        path=str(os.getcwd())+"/modules/"+str(i)
        print("attempting ",path)
        newpath="modules."+i.split('.')[0]
        importlib.import_module(newpath, package=None)
    #return importlib.import_module(tree[1], package=None) 

def dynamic_import(lib):
    tree = os.listdir('modules')
    print(tree)
    for i in tree:
        i=i.split('.')[0]
        newpath="modules."+i
        print("attempting ",newpath)

        if(i==lib):
            return importlib.import_module(newpath, package=None)
    #return importlib.import_module(tree[1], package=None) 

def print_msg(client, userdata, message):
    #print("%s : %s" % (message.topic, message.payload))

    printf("\n------------------INCOMING-----------------\n")

    dict_obj={}

    try:
        inc_msg=str(message.payload,'utf-8')

        msg_json=json.loads(inc_msg)
        printf(msg_json)
        
        dev_id=msg_json["dev_id"]
        printf(dev_id)

        time=msg_json["metadata"]["time"]
        printf(time)

        printf("\n------------------DECODED------------------\n")

        rawb64=msg_json["payload_raw"]
        decoded=decoder.decodeElsysPayload(decoder.b64toBytes(rawb64))

        printf(rawb64)
        printf("\n")
        printf(decoded)
        
        printf("\n------------------FINITO------------------\n")

        dict_obj["acp_ts"]=time
        dict_obj["dev_id"]=dev_id
        dict_obj["payload_cooked"]=decoded

        cleaned_data=json.dumps(dict_obj)

        print(cleaned_data)
        save_to_file(cleaned_data)
        printf("\n-------------------------------------------\n")

    except:
        printf("----------------EXCEPTION-----------------\n")
        printf("\nfailed with the following:\n")
        print(json.dumps(msg_json))
        printf("\n",rawb64,"\n", dev_id,"\n",time)
        printf("-------------------------------------------\n")
    
def main():
    #topic="cambridge-sensor-network/devices/#"                     #"cambridge-sensor-network/devices/elsys-eye-044501/#"
    #printf("Starting MQTT subscription for %s" %topic)
    #subscribe.callback(print_msg, topic, hostname="eu.thethings.network", auth={'username':secrets.username, 'password':secrets.password})
    decoder=dynamic_import("elsys_module")
    print("done")
    print(decoder.hi)
if __name__ == "__main__":
    main()

