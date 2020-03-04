import base64
# Adeunis decoder, code hasn't been fully converted yet
loaded="ADEUNIS"

def bin8dec(bin):
    num=bin&0xFF
    if (0x80 & num): 
        num = - (0x0100 - num)
    return num

def bin16dec(bin):
    num=bin&0xFFFF
    if (0x8000 & num):
        num = - (0x010000 - num)
    return num

def b64toBytes(b64):
    return base64.b64decode(b64)

def decodePayload(bytes):
    decoded={}
    decoded["device"]= "adeunis_test"
    
    offset = 1# index into payload for next field
    
    #// Temperature
    if (bytes[0] & 0x80):  #// temperature present
        decoded['temperature'] = bytes[offset+1]# // note only works for positive temps
    
    
    #// Button press
    if (bytes[0] & 0x20): # // Button was pressed
        decoded['button'] = True
    
    #// GPS
    if (bytes[0] & 0x10): # // gps present
        degrees = (bytes[offset] >> 4) * 10 + (bytes[offset] & 0x0F) 
      #//decoded['lat_deg'] = degrees;
      
        minutes = (bytes[offset+1] >> 4) * 10 + (bytes[offset+1] & 0x0F) +(bytes[offset+2] >> 4) / 10 + (bytes[offset+2] & 0x0F) / 100 + (bytes[offset+3] >> 4) / 1000
          #//decoded['lat_mins'] = minutes;
      
        lat_south = bytes[offset+3] & 0x01
        decoded['latitude'] = (-1 if lat_south  else 1) * degrees + minutes / 60
        offset += 4
      
        degrees = (bytes[offset] >> 4) * 100 + (bytes[offset] & 0x0F) * 10 + (bytes[offset+1] >> 4) 
          #//decoded['lng_deg'] = degrees;
      
        minutes = (bytes[offset+1] & 0x0F) * 10 + (bytes[offset+2] >> 4) + (bytes[offset+2] & 0x0F) / 10 + (bytes[offset+3] >> 4) / 100
          #//decoded['lng_mins'] = minutes;
      
        lng_west = bytes[offset+3] & 0x01
        decoded['longitude'] = (-1 if lng_west else 1) * degrees + minutes / 60
        decoded['gps_reception'] = bytes[offset+4] >> 4
        decoded['gps_satellites'] = bytes[offset+4] & 0x0F
        offset += 5
    
    
    if (bytes[0] & 0x08):  #// Uplink count present
        decoded['uplink_counter'] = bytes[offset+1]
    
    
    if (bytes[0] & 0x04): #// Downlink count present
        decoded['downlink_counter'] = bytes[offset+1]
    
    
    # battery voltage in mV
    if (bytes[0] & 0x02):  #// battery mV present
        decoded['battery'] = (bytes[offset] * 256 + bytes[offset+1]) / 1000
        offset += 2
    
    
    if (bytes[0] & 0x01):  #// RSSI and SNR present
        decoded['rssi'] = -bytes[offset+1]; #// rssi always negative
        decoded['snr'] =   bytes[offset] if (bytes[offset] < 128) else -(256 - bytes[offset]); #// snr in 2's complement
    

    return decoded
# end Adeunis