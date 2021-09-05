# kayak
Codes for modeling motion of kayak(s) on ocean

So far, there's just code to model the sea surface as a 2d array, given swell inputs

kayak1.py 
 generates matrices of phase offsets for eacy x,y position, for each swell
 Then generates component sea heights for each swell, at each position, and sums it
 
 generates a .png image for each frame, stepping for t=0..59 seconds.
 
 Afterwards, the .pngs can be animated with ffmpeg.
