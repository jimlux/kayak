#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
model ocean waves with kayak sitting on top.

Created on Sat Sep  4 15:59:49 2021

@author: jimlux
"""
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

Earthg = 9.8

""" define swells
period in seconds
height in feet (because that's what the reports give)
direction is "from" in degrees """

swells = [{"period":5,"height":.9,"direction":250},
          {"period":13,"height":.8,"direction":210},
          {"period":16,"height":.9,"direction":215}]

nswells = len(swells)

""" calculate wavelength (lambda) and speed
    and convert height to meters, and unipolar
    and convert direction to radians"""
for swell in swells:
   swell["speed"] = Earthg/(2. * np.pi) *swell["period"]
   swell["wavelength"] = swell["speed"] *swell["period"]
   swell["height"] = swell["height"]/3.28/2
   swell["direction"] = (90-swell["direction"])*np.pi/180.
   

gridspacing = 2.0
gridsize = 400
xrange = np.arange(0,gridsize*gridspacing,gridspacing)
yrange = np.arange(0,gridsize*gridspacing,gridspacing)
X,Y = np.meshgrid(xrange,yrange)

phases = np.zeros((gridsize,gridsize,nswells))

for idx,swell in enumerate(swells):
    swellcos = np.cos(swell["direction"])
    swellsin = np.sin(swell["direction"])
    wavelength = swell["wavelength"]
    print(wavelength)
    """ there's got to be a better way to do this """
    dswell1 = X*swellcos + Y*swellsin
    phases[:,:,idx]=np.pi*2.0 * dswell1/wavelength
    
    """for i in range(gridsize):
        for j in range(gridsize):
            dx = i*gridspacing
            dy = j*gridspacing
            dswell = dx * swellcos + dy*swellsin
            phases[i,j,idx]=np.pi * 2 * dswell/wavelength
    """
    #fig,ax = plt.subplots(subplot_kw={"projection": "3d"})
    #plt.figure()
    #plt.title("swell #%d"%idx)
    #surf = ax.plot_surface(xrange, yrange, phases[:,:,idx], cmap=cm.coolwarm,
    #                   linewidth=0, antialiased=False)
    #seaheight = np.cos(phases[:,:,idx])
    #img = plt.imshow(seaheight)


makefigs = True
for t in np.arange(0,60,step=1):
    sumheight = np.zeros((gridsize,gridsize))
    for idx,swell in enumerate(swells):
        seaheight = swell["height"] * np.cos(t/swell["period"]*2*np.pi+phases[:,:,idx])
        #plt.figure()
        #img = plt.imshow(seaheight)
        sumheight += seaheight
    
    #plt.figure()
    #plt.title('total %3d secs'%t)
    #img = plt.imshow(sumheight, origin='lower')
    #plt.savefig("P%03d.png"%t)
    if makefigs:
        fig = plt.figure(1, figsize=(16./2,9./2))
        ax = fig.subplots()

        fig.suptitle('water surface height %3d secs'%t)
        im=ax.imshow(sumheight,origin='lower')
        
        #fig.subplots_adjust(0.8)
        #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        #fig.colorbar(im,cax=cbar_ax)
        fig.colorbar(im,ax=ax)
        plt.savefig("P%03d.png"%t)
        plt.clf()



fig,ax = plt.subplots(subplot_kw={"projection": "3d"})

surf = ax.plot_surface(X,Y, sumheight, cmap=cm.coolwarm,linewidth=0,antialiased=False)
ax.set_zlim(-100,100)

print ("convert with")
print ("ffmpeg -r 30 -f image2 -i temp%03d.png -vcodec libx264 test.mp4")

"""
BSD 3-Clause License

Copyright (c) 2021, jimlux
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
