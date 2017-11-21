#!/usr/bin/python
# -*- coding: utf8 -*-

# 2us1.py copied from srf02_test2.py
# Yasushi Honda 2017 11/12
# Ctrl+C to STOP

import time
import pigpio
import numpy as np

BUS=1
SRF02_I2C_ADDR=0x7c
SRF02_I2C_ADDR2=0x70
SLEEP=0.07 #(sec), 読み取りに必要な最低時間は65msec(0.065sec)
VS=80
WALL=30
GAIN_DIFF=0.18
GAIN_WALL=0.15
a_diff=5
a_wall=5

NUM_GPIO=32

MIN_WIDTH=1000
MID_WIDTH=1500
MAX_WIDTH=2000

width = [0]*NUM_GPIO

def srf02_read(h):
   # レジスタ 0x02, 0x03 の値を読み取る
   high = pi.i2c_read_word_data(h,0x02)
   low = pi.i2c_read_word_data(h,0x03)

   ll=int(bin(low&0b1111111),2)  # lowの下位7bitを抜き出して10進に変換
                                 # 0-128cmの値が入る．
   lh=int(bin(low>>15),2)  # lowを15bit右にシフトして10進に変換
                           # 128-255cmの時に0b1になる
   hl=int(bin(high&0b11),2)  # highの下位2bitを抜き出す
                             # 256cm:0b01, 512cm:0b10
   d =hl*255+lh*128+ll
   return d

def srf02_fake_mesure(h):
   pi.i2c_write_device(h,[0x00,0x57]);

def srf02_burst(h):
   pi.i2c_write_device(h,[0x00,0x5C]);

def srf02_mesure(h):
   pi.i2c_write_device(h,[0x00,0x51]);

def left_wheel(val):
   pi.set_servo_pulsewidth(17, MID_WIDTH+val)

def right_wheel(val):
   pi.set_servo_pulsewidth(18, MID_WIDTH-val)


pi = pigpio.pi()

if not pi.connected:
   exit()

h = pi.i2c_open(BUS, SRF02_I2C_ADDR)
h2 = pi.i2c_open(BUS, SRF02_I2C_ADDR2)

G=[17,18] # list of gpio number that servo are connected to

if h>=0:
   while(1):

      try:
         srf02_mesure(h)
         time.sleep(SLEEP)
         dist_f=srf02_read(h)
         time.sleep(SLEEP)
         srf02_mesure(h2)
         time.sleep(SLEEP)
         dist_r=srf02_read(h2)
         diff=dist_f - dist_r
         dist_ave=(dist_f+dist_r)/2.0
         print (dist_f, dist_r)

         left=VS
         left+=a_diff*np.tanh(GAIN_DIFF*diff)
         left+=a_wall*np.tanh(GAIN_WALL*(dist_ave-WALL))
         right=VS
         right-=a_diff*np.tanh(GAIN_DIFF*diff)
         right-=a_wall*np.tanh(GAIN_WALL*(dist_ave-WALL))

         #left=VS
         #right=VS
         left_wheel(left)
         right_wheel(right-3)


      except KeyboardInterrupt:
         for g in G:
            pi.set_servo_pulsewidth(g, MID_WIDTH)
         break

   pi.i2c_close(h)
   pi.i2c_close(h2)

print("\nTidying up")
for g in G:
   pi.set_servo_pulsewidth(g, MID_WIDTH)

pi.stop()
