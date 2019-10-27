Circuit to perform Monte Carlo simulation in ngspice at rise_edge

.param capload = 3fF
.param slew_in = 50ps

.param vp = 1v
.param drise  = 400ps
.param dfall  = 60ps
.param trise  = '1.25*slew_in'
.param tfall  = 60ps
.param period = 1ns

.include "./tuned_45nm_HP.pm"
* vsrc with repeat
v1 pin 0 pwl
+ 0ns                       'vp'
+ 'dfall-0.8*tfall'         'vp'
+ 'dfall-0.4*tfall'         '0.9*vp'
+ 'dfall+0.4*tfall'         '0.1*vp'
+ 'dfall+0.8*tfall'         0v
+ 'drise-0.8*trise'         0v
+ 'drise-0.4*trise'         '0.1*vp'
+ 'drise+0.4*trise'         '0.9*vp'
+ 'drise+0.8*trise'         'vp'
+ 'period+dfall-0.8*tfall'  'vp'
+ r='dfall-0.8*tfall'

v2 vdd 0 DC vp
.subckt inv1 in out vdd
m1  out in  vdd vdd   pmos l=45n w=2.0u
m2  out in  0   0     nmos l=45n w=1.37u 
.ends inv1

.subckt buf1 in out vdd
xinv1 in tmp vdd inv1 
xinv2 tmp out vdd inv1
.ends buf1

xbuf pin pout vdd buf1
c1 pout 0 capload

.options noacct
.end