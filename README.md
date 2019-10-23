# txtpms

txtpms is a set of tools to generate IQ records that simulate TPMS sensors. The implementation is inspired from the tpms device source code available in [**rtl_433**](https://github.com/merbanan/rtl_433).

### supported sensors

At the moment only one sensor is supported:

 - Toyota TPMS sensors: FSK 9-byte Differential Manchester encoded TPMS data with CRC-8. Pacific Industries Co.Ltd. PMV-C210 (`rtl_433/src/devices/tpms_toyota.c`)

### installation

The tools can be downloaded from Github:

	git clone https://github.com/cdeletre/txtpms.git

Then it's needed to update your PATH:

	cd txtpms
	echo 'export PATH="$PATH:'`pwd`'/modulations:'`pwd`'/tpms"' >> ~/.bashrc
	export PATH="$PATH:`pwd`/modulations:`pwd`/tpms"

### dependencies

The FSK tool has dependencies to GNURadio that can be installed on Ubuntu with

	apt-get install gnuradio

### usage

#### generate symbols

Use the scripts available in `tpms` to generate the symbol file

_Example:_

	toyota.py -i cafebabe -s 128 -p 40 -t 25

It will create `cafebabe_128_40.0_25_tpms_toyota_manch_20k.u8` that contains the symbols for Toyota TPMS sensor.

#### generate the IQ record

Use `fsk.py` tool to generate the IQ record of the FSK modulated signal.

_Example:_

	fsk.py -r cafebabe_128_40.0_25_tpms_toyota_manch_20k.u8 -w cafebabe_128_40.0_25_tpms_toyota_250k.cu8

It will create `cafebabe_128_40.0_25_tpms_toyota_250k.cu8` that contains the FSK signal (25kHz deviation, 20kbauds)

#### test with rtl\_433

You can test the simulated tpms sensors with [**rtl_433**](https://github.com/merbanan/rtl_433). To do so you need to add dummy signal `txtpms/iq/zero_1s_250k.cu8` before and after the generated record to let the trigger of rtl\_433 have the time to wake-up:

	cat ./iq/zero_1s_250k.cu8 cafebabe_128_40.0_25_tpms_toyota_250k.cu8 ./iq/zero_1s_250k.cu8 > simu_tpms.cu8
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