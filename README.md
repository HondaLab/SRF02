# SRF02
Python code for reading distance from SRF02

SRF02 is a ultrasonic sensor ranging distance from 20cm upto 600cm.
Power supply is given by 5V and the data read through I2C.

It can be connected to Raspberry Pi 3 I2C pins. 
Data about distance can be read from register 0x02 and 0x03.
But formats of these data are different from those in the case of BeagleBone Black.

Therefore, in this repository I put a example of python code in order to read
the distance data from SRF02

![snapthot](https://github.com/HondaLab/SRF02/blob/master/23244200_540219726313824_5582184282879226965_n.jpg?raw=true)

Yasushi Honda 2017 11/9
