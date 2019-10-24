#!/usr/bin/env python

"""
Coding based on rtl_433 device source code from  https://github.com/merbanan/rtl_433
rtl_433/src/devices/tpms_renault.c
"""

from binascii import unhexlify,hexlify
from struct import pack,unpack_from
import argparse
from lib.crc import crc8

"""
 Default values
 based on test file: https://github.com/merbanan/rtl_433_tests/raw/master/tests/Renault_TPMS/gfile070.cu8
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
time      : @0.214588s
model     : Renault      type      : TPMS          id        : 87f293
flags     : 34           pressure_kPa: 202.5 kPa   temperature_C: 25 C       mic       : CRC
"""
MODEL='Renault'

SENSORID=int('87f293',16)
PRESSURE=202.5
TEMPERATURE=25
FLAGS=int('34',16)
UNKNOWN=0xffff

# Manchester levels
HIGH = 0xff
LOW = HIGH ^ HIGH
MMODE='manch' # diffmanch | manch
NBYTES=9

def get_payload(sensorid=SENSORID,pressure=PRESSURE,temperature=TEMPERATURE,flags=FLAGS,unknown=UNKNOWN):

  int_payload = 0x00

  int_payload = int_payload << 6

  int_payload += flags & 0x7f

  int_payload = int_payload << 2

  int_payload += (int(pressure / 0.75) >> 8) & 0x3

  int_payload = int_payload << 8

  int_payload += int(pressure / 0.75) & 0xff

  int_payload = int_payload << 8

  int_payload += int( temperature + 30 ) & 0xff

  int_payload = int_payload << 24

  int_payload += sensorid & 0xffffff

  int_payload = int_payload << 16

  int_payload += unknown & 0xffff

  payload = pack('>Q',int_payload)

  crc = crc8(payload,8)

  payload += pack('<B',crc)

  return payload

def get_manchester(payload):

  # sync '0101 0101  0101 0101  0101 0101  0101 0110'
  manchester = pack('<32B',* [LOW,HIGH] * 14 + [LOW,HIGH,HIGH,LOW] )

  #for i,c in enumerate(payload):
  #  byte = ord(c)
  for byte in unpack_from('<%dB' % NBYTES,payload):
    for i in range(8):
      if byte & 0x80:
        manchester += pack('<2B', HIGH, LOW)
      else:
        manchester += pack('<2B', LOW, HIGH)

      byte = (byte << 1) & 0xff

  # trailing '0000'
  manchester += pack('<4B', *[LOW]*4)

  return manchester

def main():

  parser = argparse.ArgumentParser(description='Generate Renault TPMS symbols (manchester)')
  parser.add_argument('-i','--sensor-id',metavar='SENSOR-ID',default=hex(SENSORID)[2:],
                      help='Sensor ID, 4 bytes id, hex string (default: %s )' % hex(SENSORID)[2:] )

  parser.add_argument('-p','--pressure',metavar='PRESSURE',default=PRESSURE,type=float,
                      help='Pressure, PSI (default: %s)' % PRESSURE)

  parser.add_argument('-t','--temperature',metavar='TEMPERATURE',default=TEMPERATURE,type=int,
                      help='Temperature, Celcius, -50 to 205 (default: %d)' % TEMPERATURE)

  parser.add_argument('-f','--flags',metavar='FLAGS',default=FLAGS,type=int,
                      help='6 bits Flags (default: %d)' % FLAGS)

  parser.add_argument('-u','--unknown',metavar='UNKNOWN',default=UNKNOWN,type=int,
                      help='2 bytes Unknown (default: %d)' % UNKNOWN )

  args = parser.parse_args()

  payload = get_payload(int(args.sensor_id,16),args.pressure,args.temperature,args.flags,args.unknown)

  print('payload = %s' % hexlify(payload))

  manchester = get_manchester(payload)

  print( 'manchester = %s' % manchester.replace('\xff','1').replace('\x00','_') )

  iq=open('%s_i%s_p%s_t%d_f%s_u%s_tpms_%s.u8' % (MODEL,args.sensor_id,args.pressure,args.temperature,hex(args.flags),hex(args.unknown),MMODE),b'w+')
  iq.write(manchester)
  iq.close()

if __name__ == '__main__':
    exit(main())
