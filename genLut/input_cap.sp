Input Capacitance Obtainment

.param freq = 1Meg
.param vp = 1v
.csparam freq = {freq}
.include "./tuned_45nm_HP.pm"

mp1  0 pin 0 0 pmos l=45n w=2.0u
mn1  0 pin 0 0 nmos l=45n w=1.37u

V1 in 0 vp ; pwl (0.0 -1.8 1u 1.8)
VAC in pin dc 0 ac 1
.ac lin 1 {freq} {freq}

.control
  run
  let capacitance = -imag(VAC#branch)/(2*PI*freq)
  print capacitance >> input_cap.log
.endc
.end