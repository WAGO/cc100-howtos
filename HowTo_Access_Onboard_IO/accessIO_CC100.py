#!/usr/bin/python3

####################################################################################
# MIT License

# Copyright (c)2022 WAGO GmbH & Co. KG - Thomas.Brandt@wago.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# Of this software and associated documentation files (the "Software"), to deal
# In the Software without restriction, including without limitation the rights
# To use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# Copies of the Software, and to permit persons to whom the Software is
# Furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# Copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####################################################################################

####################################################################################
# WagoLogo
####################################################################################
def printLogo():
  print ('\x1b\033c' + '\x1b[1;32m' +
  "██     ██  █████   ██████   ██████  " + '\n' +
  "██     ██ ██   ██ ██       ██    ██ " + '\n' +
  "██  █  ██ ███████ ██   ███ ██    ██ " + '\n' +
  "██ ███ ██ ██   ██ ██    ██ ██    ██ " + '\n' +
  " ███ ███  ██   ██  ██████   ██████  " + '\n' +
  '\n' + '\x1b[0m' )


####################################################################################
# Menu printing
####################################################################################
def menuSelection():
  print ("Menu:\n" +
         "  [1] Digital Inputs \n" +
         "  [2] Digital Outputs \n" +
         "  [3] Analog Inputs \n" +
         "  [4] Analog Outputs \n" +
         "  [5] PT1000 Inputs \n" +
         "  [Q] Quit \n")
  ret = input("  Choose:")
  return ret

####################################################################################
# Read complete calibration settings from file
# will be stored in global variable 'calib_data'
####################################################################################
def readCalibriationData():
  global calib_data
  fname="/etc/calib"
  f = open(fname, "r")
  #Read data but skip the header
  calib_data=f.readlines()[1:]
  f.close()

####################################################################################
# Getting specific calibration data from calibration array
# param[in] value - select specific calibration set
#                   0 for PT1
#                   1 for PT2
#                   2 for AI1
#                   3 for AI2
#                   4 for AO1
#                   5 for AO2
####################################################################################
def getCalibartionData(value):
  return calib_data[value].rstrip().split(' ', 4)

####################################################################################
# Calculation of raw input values to calibrated values
# param[in] val_uncal - raw input
# param[in] calib - array of calibration values
# return calibrated values
####################################################################################
def calcCalibrate(val_uncal, calib):
  x1=int(calib[0])
  y1=int(calib[1])
  x2=int(calib[2])
  y2=int(calib[3])

  val_cal=(y2-y1)*int(val_uncal-x1)
  val_cal=val_cal/(x2-x1)
  val_cal=val_cal+y1

  return int(val_cal)

####################################################################################
# digital inputs
####################################################################################
def digiInp():
  print ("Digital Inputs:")
  print ("================")
  #Read file
  fname="/sys/devices/platform/soc/44009000.spi/spi_master/spi0/spi0.0/din"
  f = open (fname, "r")
  dig = f.readline();
  f.close()
  dig = int (dig)
  digbin=format(dig, "08b")
  print("Digital inputs value:"+str(dig)+"[dec] "+digbin+"[bin]")

  for i in range(8):
    print ("D",i,": ", end='',sep='')
    if dig & (1 << i):
      print("ON")
    else:
      print("OFF")

  print ("================\n")

####################################################################################
# Digital Output
####################################################################################
def digiOut():
  print ("Digital Outputs:")
  print ("================")
  dig=int (input("Enter Value for digital output:"))

  #Check borders
  if dig > 255:
    dig=255
  if dig < 0:
    dig=0

  print("Setting outputs:")
  for i in range(8):
    print ("D",i,": ", end='',sep='')
    if dig & (1 << i):
      print("ON")
    else:
      print("OFF")

  # Write file
  fname="/sys/kernel/dout_drv/DOUT_DATA"
  f = open(fname, "w")
  f.write(str(dig))
  f.close
  print ("================\n")

####################################################################################
# Analog Input
####################################################################################
def anaInp():
  print ("Analog Inputs:")
  print ("===============")
  cal_ai1=getCalibartionData(2)
  cal_ai2=getCalibartionData(3)

  #print("AI1: ",cal_ai1)
  #print("AI2: ",cal_ai2)

  ai1fname="/sys/bus/iio/devices/iio:device3/in_voltage3_raw"
  ai2fname="/sys/bus/iio/devices/iio:device3/in_voltage0_raw"

  f=open(ai1fname, "r")
  ai1_value=int(f.readline())
  f.close()
  val=calcCalibrate(ai1_value, cal_ai1)
  print("AI1:",val, "[mv]")

  f=open(ai2fname, "r")
  ai2_value=int(f.readline())
  f.close()
  val=calcCalibrate(ai2_value, cal_ai2)
  print("AI2:",val,"[mv]")
  print ("===============\n")

####################################################################################
# Analog Output
####################################################################################
def anaOut():
  print ("Analog Out")
  print ("===========")

  #AO1
  valao1=int (input("AO1 [mv]:") or "3000")
  valao1=int(valao1)
  #Check bounds
  if valao1 > 10000:
    valao1=10000
    print("Maximum value is 10000")
  elif valao1 < 0:
    valao1=0
    print("No negative value allowed")

  cal_ao1=getCalibartionData(4)
  set_valao1=calcCalibrate(valao1, cal_ao1)

  #A02
  valao2=int (input("AO2 [mv]:") or "4500")
  valao2=int(valao2)
  #Check bounds
  if valao2 > 10000:
    valao2=10000
    print("Maximum value is 10000")
  elif valao2< 0:
    valao2=0
    print("No negative value allowed")
  cal_ao2=getCalibartionData(5)
  set_valao2=calcCalibrate(valao2, cal_ao2)

  print("Power Off AO1")
  AO1_POWER_FILE="/sys/bus/iio/devices/iio:device0/out_voltage1_powerdown"
  f=open(AO1_POWER_FILE, "w")
  f.write("0")
  f.close()
  print("Set AO1 Value {} wich will result in {} [mV]".format(set_valao1, valao1))
  AO1_VOLTAGE_FILE="/sys/bus/iio/devices/iio:device0/out_voltage1_raw"
  f=open(AO1_VOLTAGE_FILE, "w")
  f.write(str(set_valao1))
  f.close

  print("Power Off AO2")
  AO2_POWER_FILE="/sys/bus/iio/devices/iio:device1/out_voltage2_powerdown"
  f=open(AO2_POWER_FILE, "w")
  f.write("0")
  f.close()
  print("Set AO1 Value {} wich will result in {} [mV]".format(set_valao2, valao2))
  AO2_VOLTAGE_FILE="/sys/bus/iio/devices/iio:device1/out_voltage2_raw"
  f=open(AO2_VOLTAGE_FILE, "w")
  f.write(str(set_valao2))
  f.close
  print ("===========\n")

####################################################################################
# PT1000 - Inputs
####################################################################################
def pt100():
  print ("PT1000 Inputs")
  print ("==============")

  PT1_FILENAME="/sys/bus/iio/devices/iio:device2/in_voltage13_raw"
  f=open(PT1_FILENAME, "r")
  pt1_val=f.readline().rstrip()
  f.close()

  cal_pt1=getCalibartionData(0)
  pt1_val_cal=calcCalibrate(int(pt1_val), cal_pt1)
  print("PT1: {}[Ohm] - {}[raw]".format(pt1_val_cal, pt1_val))

  PT2_FILENAME="/sys/bus/iio/devices/iio:device2/in_voltage1_raw"
  f=open(PT2_FILENAME, "r")
  pt2_val=f.readline().rstrip()
  f.close()

  cal_pt2=getCalibartionData(1)
  pt2_val_cal=calcCalibrate(int(pt2_val), cal_pt2)
  print("PT2: {}[Ohm] - {}[raw]".format(pt2_val_cal, pt2_val))
  print ("==============\n")

def switchMenu(arg):
  switcher = {
    '1': digiInp,
    '2': digiOut,
    '3': anaInp,
    '4': anaOut,
    '5': pt100
  }
  func = switcher.get(arg, lambda:"Invalid choise")
  func()

####################################################################################
# Main 
####################################################################################
def main():
  printLogo()

  print ("***************************************")
  print ("** HowTo Access Onboard IO for CC100 **")
  print ("***************************************")

  #Read calibrationData from file and store global
  readCalibriationData()

  inp = '' 
  while inp.upper() != 'Q':
    inp = menuSelection()
    inp = inp.upper()
    if inp != 'Q':
      switchMenu(inp)
    else:
      print ("..:: Goodbye ::..")


if __name__ == "__main__":
      main()
