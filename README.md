# txtpms

![txtpms_logo](https://raw.githubusercontent.com/cdeletre/txtpms/master/pics/txtpms_logo.png)

**txtpms** is a set of tools to generate IQ records that simulate TPMS sensors. The implementation is inspired from the tpms device source code available in [**rtl_433**](https://github.com/merbanan/rtl_433).

### supported sensors

At the moment following sensors are supported:

 - **Toyota** FSK 9-byte Differential Manchester encoded TPMS data with CRC-8. Pacific Industries Co.Ltd. PMV-C210 (`rtl_433/src/devices/tpms_toyota.c`)
 - **Citroën** FSK 10 byte Manchester encoded checksummed TPMS data. Also Peugeot and likely Fiat, Mitsubishi, VDO-types (`rtl_433/src/devices/tpms_citroen.c`)
 - **Renault** FSK 9 byte Manchester encoded TPMS with CRC. Seen on Renault Clio, Renault Captur and maybe Dacia Sandero (`rtl_433/src/devices/tpms_renault.c`)
 - **Ford** FSK 8 byte Manchester encoded TPMS with simple checksum. Seen on Ford Fiesta, Focus. (`rtl_433/src/devices/tpms_ford.c`)

### installation

The tools can be downloaded from Github:

	git clone https://github.com/cdeletre/txtpms.git

Then it's needed to update your PATH:

	cd txtpms
	echo 'export PATH="$PATH:'`pwd`'/modulations:'`pwd`'/devices"' >> ~/.bashrc
	export PATH="$PATH:`pwd`/modulations:`pwd`/devices"

### dependencies

The FSK tool has dependencies to GNURadio that can be installed on Ubuntu with

	apt-get install gnuradio

### usage

#### generate symbols

Use the scripts available in `devices` to generate the symbol file

 - tpms_toyota.py

```
usage: tpms_toyota.py [-h] [-i SENSOR-ID] [-p PRESSURE] [-t TEMPERATURE]
                      [-s STATUS]

Generate Toyota TPMS symbols (differential manchester)

optional arguments:
  -h, --help            show this help message and exit
  -i SENSOR-ID, --sensor-id SENSOR-ID
                        Sensor ID, 4 bytes id, hex string (default: fb0a43e7 )
  -p PRESSURE, --pressure PRESSURE
                        Pressure, PSI (default: 36.75)
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature, Celcius, -40 to 215 (default: 29)
  -s STATUS, --status STATUS
                        Status, 8 bits unsigned integer (default: 128)
  -o OUTPUT-FILE, --output-file OUTPUT-FILE
                        Output file. Will be automatically genereated if not
                        provided
```

 - tpms_citroen.py

```
usage: tpms_citroen.py [-h] [-i SENSOR-ID] [-p PRESSURE] [-t TEMPERATURE]
                       [-s STATUS] [-f FLAGS] [-r REPEAT] [-b BATTERY]

Generate Citroen TPMS symbols (manchester)

optional arguments:
  -h, --help            show this help message and exit
  -i SENSOR-ID, --sensor-id SENSOR-ID
                        Sensor ID, 4 bytes id, hex string (default: 8add48d4 )
  -p PRESSURE, --pressure PRESSURE
                        Pressure, PSI (default: 289)
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature, Celcius, -50 to 205 (default: 23)
  -s STATUS, --status STATUS
                        Status, 8 bits unsigned integer (default: 210)
  -f FLAGS, --flags FLAGS
                        4 bits Flags (default: 0)
  -r REPEAT, --repeat REPEAT
                        Repeat counter 0 to 4 (default: 1)
  -b BATTERY, --battery BATTERY
                        Battery (default: 14)
  -o OUTPUT-FILE, --output-file OUTPUT-FILE
                        Output file. Will be automatically genereated if not
                        provided
```

 - tpms_renault.py

```
usage: tpms_renault.py [-h] [-i SENSOR-ID] [-p PRESSURE] [-t TEMPERATURE]
                       [-f FLAGS] [-u UNKNOWN] [-o OUTPUT-FILE]

Generate Renault TPMS symbols (manchester)

optional arguments:
  -h, --help            show this help message and exit
  -i SENSOR-ID, --sensor-id SENSOR-ID
                        Sensor ID, 4 bytes id, hex string (default: 87f293 )
  -p PRESSURE, --pressure PRESSURE
                        Pressure, PSI (default: 202.5)
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature, Celcius, -50 to 205 (default: 25)
  -f FLAGS, --flags FLAGS
                        6 bits Flags (default: 52)
  -u UNKNOWN, --unknown UNKNOWN
                        2 bytes Unknown (default: 65535)
  -o OUTPUT-FILE, --output-file OUTPUT-FILE
                        Output file. Will be automatically genereated if not
                        provided
```

 - tpms_ford.py

```
usage: tpms_ford.py [-h] [-i SENSOR-ID] [-p PRESSURE] [-t TEMPERATURE]
                    [-f FLAGS]

Generate Renault TPMS symbols (manchester)

optional arguments:
  -h, --help            show this help message and exit
  -i SENSOR-ID, --sensor-id SENSOR-ID
                        Sensor ID, 4 bytes id, hex string (default: 6ad446 )
  -p PRESSURE, --pressure PRESSURE
                        RAW pressure (default: 0x6a)
  -t TEMPERATURE, --temperature TEMPERATURE
                        RAW temperature (default: 0xd4)
  -f FLAGS, --flags FLAGS
                        RAW flags (default: 0x46)
  -o OUTPUT-FILE, --output-file OUTPUT-FILE
                        Output file. Will be automatically genereated if not
                        provided
```

_Example:_

	tpms_toyota.py -i cafebabe -s 128 -p 40 -t 25

It will create `Toyota_icafebabe_s128_p40.0_t25_tpms_diffmanch.u8` that contains the symbols for Toyota TPMS sensor.  It will also display the calculated raw payload and its corresponding differential manchester coding:


	payload = cafebabede2080430c
	differential manchester = _1_1_1_1__1111__11_1_1__1_11_1__11__11__11__1_11_1__11__1_11_1__1_11__11__11_1__11_1__11__11_1_1_1__1_1_1_1_1_11_1_1_1_1_1_1_1_1__1_1_1_1_11__1_1_1_1_11__1_1_111

#### generate the IQ record

Use `tpms_fsk.py` tool to generate the IQ record of the FSK modulated signal.

```
Usage: tpms_fsk.py: [options]

Options:
  -h, --help            show this help message and exit
  -d DEVIATION, --deviation=DEVIATION
                        Set Deviation [default=25000]
  -s FREQUENCY_SHIFT, --frequency-shift=FREQUENCY_SHIFT
                        Set Frequency Shift [default=0]
  -r READ_FILE, --read-file=READ_FILE
                        Set Symbol file [default=]
  -w WRITE_FILE, --write-file=WRITE_FILE
                        Set cu8 file [default=]
  -b BAUD, --baud=BAUD  Set Baud [default=20000]

```

_Example:_

	tpms_fsk.py -r Toyota_icafebabe_s128_p40.0_t25_tpms_diffmanch.u8 -w Toyota_icafebabe_s128_p40.0_t25_tpms_250k.cu8

It will create `Toyota_icafebabe_s128_p40.0_t25_tpms_250k.cu8` that contains the FSK signal (25 kHz deviation, 20 kbauds).

#### test with rtl\_433

You can test the simulated tpms sensors with [**rtl_433**](https://github.com/merbanan/rtl_433). To do so you need to add dummy signal before and after the generated record to let the trigger of rtl\_433 have the time to wake-up:

	dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> simu_tpms.cu8
	cat Toyota_icafebabe_s128_p40.0_t25_tpms_250k.cu8 >> simu_tpms.cu8
	dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> simu_tpms.cu8
	rtl_433 -r simu_tpms.cu8

It should output the following decoding:

	_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
	time      : @1.000000s
	model     : Toyota       type      : TPMS          id        : cafebabe
	status    : 128          pressure_PSI: 40.000      temperature_C: 25.000     mic       : CRC

#### analyze the generated signal

The signal can be analyzed with [**inspectrum**](https://github.com/miek/inspectrum):

	inspectrum simu_tpms.cu8

![inspectrum](https://raw.githubusercontent.com/cdeletre/txtpms/master/pics/inspectrum.png)