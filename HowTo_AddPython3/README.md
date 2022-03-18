# Adding Python3 to CC100

This HowTo shows how to add python3 to the CC100

## PREREQUISITES
You need minimum FW Version 21 (03.09.04)
This HowTo is based on a clean installation of Ubuntu LTS, with an installed and working 
WAGO Board-Support Package for CC100.
Working means that you successfully built the standard image “sd.hdimg”.

## Installation and usage

### 1)  On development host (Ubuntu)
#### 1.1) Select package "python3" for build in ptxdist
```
>cd ~/<ptxproj>/
>ptxdist menuconfig
```

```
 Scripting Languages             --->[Enter]
 <*> python3                         --->[SPACE][SPACE]

 [Exit][Exit], and save configuration [Yes]
```

#### 1.2) Clean "python3" package
```
>cd ~/<ptxproj>/
>ptxdist clean python3
```

#### 1.3) Build the "python3" package
```
>cd ~/<ptxproj>/
>ptxdist targetinstall python3
```

If you see the "finished target python3.targetinstall" at the end of the run,it is time for a :)
You will find the needed IPKG packege here:
```
~/<ptxproj>/plattform-cc100/packages/python3_3.7.6_armhf.ipk
```

#### 1.4) Build complete firmware image "sd.hdimg" which includes python3 package (optional)
You can build a complete image if you like. If you like follow these commands:
```
>cd ~/<ptxproj>/
>ptxdist images
```

As usual, you can:
- copy image file "sd.hdimg" with command "dd" to SD-Card and boot the CC100 from it.
- transfer packags into CC100 filesystem and call "opkg install python3_3.7.6_armhf.ipk"
- utilize Web-Based-Management(WBM) feature "Software-Upload"

### 2) Installing package via SSH
#### 2.1) Copy IPK to CC100 via ssh-copy

```
>cd ~/<ptxproj>/plattform-cc100/packages/
>scp python3_3.7.6_armhf.ipk root@<IP-CC100>:/root
```

#### 2.2) Installing IPKG package by commandline
Open a terminal session via SSH.
Login as "root" with password "wago" (default)

```
>cd /root
>opkg install python3_3.7.6_armhf.ipk
```

---
### Testing the installation
#### 3.1) Open a ssh terminal session to CC100
Login as "root" with password "wago" (default)

```
> python3 --version
Python 3.7.6
```

Python3 is installed successfully installed.

---
### NOTE:
Check your needed modules and bindings and reinstall if needed:
```
>cd ~/<ptxproj>/
>ptxdist menuconfig
```

For bindings:
```
 Scripting Languages             --->[Enter]
 <*> python3                         --->[Enter]
```

For extra modules:
```
Scripting Languages             --->[Enter]
python3 Extra Modules           --->[Enter]
```
