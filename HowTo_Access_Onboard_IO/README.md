# Direct Access to Onboard I/O Channels

This HowTo shows how to access the onboard IOs of the CC100.
Access to the onboard I/O channels requires a functioning SSH connection.

## PREREQUISITES
You need minimum FW Version 21 (03.09.04) and python3 installed (refer to
[HowTo_AddPython3](https://github.com/WAGO/cc100-howtos/tree/main/HowTo_AddPython3))

## 1. Digital Channels
### 1.1 Digital Outputs
With a single access attempt to the following file, all outputs are addressed:
```
/sys/kernel/dout_drv/DOUT_DATA

```
The LSB corresponds to DO1.
The driver independently manages control of the corresponding LEDs.

### 1.2 Digital Inputs
With a single access attempt to the following file, all inputs are addressed

```
/sys/devices/platform/soc/44009000.spi/spi_master/spi0/spi0.0/din
```

The LSB corresponds to DI1. The driver independently manages control of the corre-
sponding LEDs.


```
 $ cat /sys/devices/platform/soc/44009000.spi/spi_master/spi0/spi0.0/din
 5
```

## 2. Analog Channels

The level of the analog signals is adjusted. The associated external circuitry changes the
quantification characteristics, which then requires each channel to be calibrated. The cali-
bration is done once during production. The calibration results are written into the file /etc/
calib. Because a two-point calibration is used, two points and their coordinates are
needed for each channel.

![equation](http://www.sciweavers.org/tex2img.php?eq=value_%7Bcalibrated%7D%3D%20%5Cfrac%7B%20y_%7B2%7D%20-%20y_%7B1%7D%20%7D%7Bx_%7B2%7D%20-%20x_%7B1%7D%7D%2A%20%5Cbig%28value_%7Buncalibrated%7D-x_%7B1%7D%5Cbig%29%2By_%7B1%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

The first line in the file /etc/calib contains a list of the available analog channels. Each fol-
lowing line contains the coordinates of the two calibration points and is assigned to a
channel. The order of the these lines corresponds to the order of the listed channels.

```
$cat /etc/calib
PT1 PT2 AI1 AI2 A01 A02
12452 1182 21785 1777
12402 1179 21767 1788
5898 1025 50375 9022
5698 990 50205 8997
1064 350 8976 3000
1053 350 8966 3000
```

For a better representation see the table below.

|   | x1 | y1 | x2 | y2|
|---|---:|---:|---:|---:|
|PT1|12452|1182|21785|1777|
|PT2|12402|1179|21767|1788|
|AI1|5698|990|50205|8997|
|AI2|5698|990|50205|8997|
|AO1|1064|350|8976|3000|
|AO2|1053|350|8966|3000|

## 2.1 Analog Outputs
The analog outputs must be switched on before the desired voltage is read out. To switch
on the outputs, enter 0 in the corresponding file:

AO1:
```
/sys/bus/iio/devices/iio:device0/out_voltage1_powerdown
```

A02:
```
/sys/bus/iio/devices/iio:device1/out_voltage2_powerdown
```

The necessary voltage [mV] at the output is set by entering a calibrated value in the
corresponding file:

AO1:
```
/sys/bus/iio/devices/iio:device0/out_voltage1_raw
```
AO2:
```
/sys/bus/iio/devices/iio:device1/out_voltage2_raw
```

## 2.2 Analog Inputs
The uncalibrated values [mV] are delivered through the readout of the following files:

AI1:
```
/sys/bus/iio/devices/iio:device3/in_voltage3_raw
```
AI2:
```
/sys/bus/iio/devices/iio:device3/in_voltage0_raw
```
## 2.4 Pt1000 Analog Input
This channel is an analog input that is wired to deliver a connected resistance value
[ohms]. The value readout must also be calibrated.

PT1:
```
/sys/bus/iio/devices/iio:device2/in_voltage13_raw
```
PT2:
```
/sys/bus/iio/devices/iio:device2/in_voltage1_raw
```

# 3. Python example
You will find a python example which will allow you to manipulate the outputs and
read the inputs.

```
$python3 accessIO_CC100.py
██     ██  █████   ██████   ██████  
██     ██ ██   ██ ██       ██    ██ 
██  █  ██ ███████ ██   ███ ██    ██ 
██ ███ ██ ██   ██ ██    ██ ██    ██ 
 ███ ███  ██   ██  ██████   ██████  


 ***************************************
 ** HowTo Access Onboard IO for CC100 **
 ***************************************
 Menu:
   [1] Digital Inputs
   [2] Digital Outputs
   [3] Analog Inputs
   [4] Analog Outputs
   [5] PT1000 Inputs
   [Q] Quit

   Choose:
```

## 3.1 Digitial Inputs
It will read out the input file and print it out in a more user friendly style
```
Digital Inputs:
================
Digital inputs value:5[dec] 00000101[bin]
D0: ON
D1: OFF
D2: ON
D3: OFF
D4: OFF
D5: OFF
D6: OFF
D7: OFF
================
```

## 3.2 Digital Output
This will allow you to manipulate the digital output. It will require a input value.
The value has to be in the range of [0-255] and to be enterd as decimal value.
```
Digital Outputs:
================
Enter Value for digital output:5
Setting outputs:
D0: ON
D1: OFF
D2: ON
D3: OFF
D4: OFF
D5: OFF
D6: OFF
D7: OFF
================
```
## 3.3 Analog Inputs
It will read out the raw input and transforms it with the help of the calibration 
table to the real input voltage.
```
Analog Inputs:
===============
AI1: 2998 [mv]
AI2: 3000 [mv]
===============
```

## 3.4 Analog Input
This will allow you to manipulate the analog output. It will require a input value
for each channel. The value has to be in the range of [0-10000][mv] and to be enterd as 
decimal value. 
It will be transformed according to the calibration table to the corresponding input values.
```
Analog Out
===========
AO1 [mv]:2500
AO2 [mv]:1000
Power Off AO1
Set AO1 Value 830 wich will result in 2500 [mV]
Power Off AO2
Set AO1 Value 332 wich will result in 1000 [mV]
===========
```
## 3.5 PT1000
It will read out the raw input and transforms it with the help of the calibration
table to the corresponding resistor value.
```
PT1000 Inputs
==============
PT1: 996[Ohm] - 9543[raw]
PT2: 688[Ohm] - 4853[raw]
==============
```

