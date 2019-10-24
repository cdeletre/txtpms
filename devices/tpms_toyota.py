#!/usr/bin/env python

"""
Coding based on rtl_433 device source code from  https://github.com/merbanan/rtl_433
rtl_433/src/devices/tpms_toyota.c
"""

from binascii import unhexlify,hexlify
from struct import pack,unpack_from
import argparse

"""
 Default values
 based on test file: https://github.com/merbanan/rtl_433_tests/raw/master/tests/Toyota_TPMS/gfile006.cu8
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
time      : @0.214176s
model     : Toyota       type      : TPMS          id        : fb0a43e7
status    : 128          pressure_PSI: 36.750      temperature_C: 29.000     mic       : CRC
"""

SENSORID=int('fb0a43e7',16)
TEMPERATURE=29
PRESSURE=36.750
STATUS=128

# Manchester levels
HIGH = 0xff
LOW = HIGH ^ HIGH

def crc8(message,nBytes,polynomial=0x07,init=0x00):

  """
  Port of C crc8 function from rtl_433 util
  https://github.com/merbanan/rtl_433/blob/master/src/util.c
  """

  remainder = init
  
  for byte in range(nBytes):
    remainder ^= ord(message[byte])
    for bit in range(8):
      if(remainder & 0x80):
        remainder = (remainder << 1)  ^ polynomial
      else:
        remainder = (remainder << 1)
    remainder = remainder & 0xff

  return remainder

def get_payload(sensorid=SENSORID,pressure=PRESSURE,temperature=TEMPERATURE,state=STATUS):

  int_payload = 0x00

  int_payload = int_payload << 32

  int_payload += sensorid & 0xffffffff

  int_payload = int_payload << 1

  int_payload += (state & 0x80) >> 7

  int_payload = int_payload << 8

  int_payload += int( 4 * ( pressure + 7 ) ) & 0xff

  int_payload = int_payload << 8

  int_payload += int( temperature + 40 ) & 0xff

  int_payload = int_payload << 7

  int_payload += state & 0x7f

  int_payload = int_payload << 8

  int_payload += int( 4 * ( pressure + 7 ) ) ^ 0xff

  payload = pack('>Q',int_payload)

  crc = crc8(payload,8,0x07,0x80)

  payload += pack('<B',crc)

  return payload

def get_differential_manchester(payload):

  # sync '01010101001111'
  differential_manchester = pack('<14B', * [LOW,HIGH] * 4 + [LOW,LOW,HIGH,HIGH,HIGH,HIGH])

  last = HIGH

  #for i,c in enumerate(payload):
  #  byte = ord(c)
  for byte in unpack_from('<9B',payload):
    for i in range(8):
      if byte & 0x80:
        last = last ^ HIGH
        differential_manchester += pack('<2B', last, last)
      else:
        differential_manchester += pack('<2B', last ^ HIGH, last)

      byte = (byte << 1) & 0xff
  last = last ^ HIGH
  differential_manchester += pack('<3B', last, last, last)

  return differential_manchester

def main():

  parser = argparse.ArgumentParser(description='Generate Toyota TPMS symbols (differential manchester)')

  parser.add_argument('-i','--sensor-id',metavar='SENSOR-ID',default=hex(SENSORID)[2:],
                      help='Sensor ID, 4 bytes id, hex string (default: %s )' % hex(SENSORID)[2:])

  parser.add_argument('-p','--pressure',metavar='PRESSURE',default=PRESSURE,type=float,
                      help='Pressure, PSI (default: %s)' % PRESSURE)

  parser.add_argument('-t','--temperature',metavar='TEMPERATURE',default=TEMPERATURE,type=int,
                      help='Temperature, Celcius, -40 to 215 (default: %d)' % TEMPERATURE)

  parser.add_argument('-s','--status',metavar='STATUS',default=STATUS,type=int,
                      help='Status, 8 bits unsigned integer (default: %d)' % STATUS)

  args = parser.parse_args()

  payload = get_payload(int(args.sensor_id,16),args.pressure,args.temperature,args.status)

  print('payload = %s' % hexlify(payload))

  differential_manchester = get_differential_manchester(payload)

  print( 'differential manchester = %s' % differential_manchester.replace('\xff','1').replace('\x00','_') )

  iq=open('%s_%d_%s_%d_tpms_toyota_diffmanch_20k.u8' % (args.sensor_id,args.status,args.pressure,args.temperature),b'w+')
  iq.write(differential_manchester)
  iq.close()

if __name__ == '__main__':
    exit(main())
