Circuit to perform Monte Carlo simulation in ngspice
* the buffer is construct by two inverters as common structure
.param capload = 45fF
.param slew_in = 80ps
.param vp = 0.55v
.param drise  = 1200ps
.param dfall  = 400ps
.param period = 2ns

* slew time is use the definition of 0.1*vp to 0.9*vp or 0.9*vp to 0.1*vp
.param trise  = '1.25*slew_in'
.param tfall  = '1.25*slew_in'


.include "./PTM45/tuned_45nm_HP.pm"
* vsrc with repeat
v1 pin 0 pwl
+ 0ns                       'vp'
+ 'dfall'                   'vp'
+ 'dfall+tfall'             0v
+ 'drise'                   0v
+ 'drise+trise'             'vp'
+ 'period'                  'vp'
+ r='0' DC 0
v2 vdd 0 DC vp
.subckt inv1 in out vdd
mp1  out in  vdd vdd   pmos l=45n w=2u
mn1  out in  0   0     nmos l=45n w=1.37u 
.ends inv1

.subckt buf1 in out vdd
xinv1 in tmp vdd inv1 
xinv2 tmp out vdd inv1
.ends buf1

xbuf pin pout vdd buf1
c1 pout 0 capload

.options noacct
.end