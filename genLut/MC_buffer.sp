*****************   ng_script    ******************
* Perform Monte Carlo simulation in ngspice
* script for use with a ispd buffer. BSIM3
* circuit is in buffer.sp
* edit 'set sourcepath' for your path to circuit file
* start script by 'ngspice -o MC_buffer.log MC_buffer.sp'
***************************************************
.control 
  let mc_runs = 4
  let run = 1
  set sourcepath = (/Users/mac/Desktop/lut)
  source buffer.sp 

* max power dissipation during charge and discharge in a clock period
  tran 10p 4n 
  let power_dissipation = (i(v2)*v(vdd))
  meas tran mos_power MAX power_dissipation from=1n to=2n
  print mos_power >> power.log
  destroy all



* define distributions for random numbers:
* gauss: Gaussian distribution, deviation relativ to nominal value
* agauss: Gaussian distribution, deviation absolut
  define gauss(nom, var, sig) (nom + (nom*var)/sig * sgauss(0))
  define agauss(nom, avar, sig) (nom + avar/sig * sgauss(0))
*
* We want to vary the model parameters vth0, u0 and tox
* of the BSIM3 model for the NMOS and PMOS transistors.
* We may obtain the nominal values (nom) by manually extracting them from
* the parameter set. Here we get them automatically and store them into
* vectors. This has the advantage that you may change the parameter set
* without having to look up the values again.
  let n1vth0=@nmos[vth0]
  let n1u0=@nmos[u0]
  let n1tox=@nmos[toxref]
  let p1vth0=@pmos[vth0]
  let p1u0=@pmos[u0]
  let p1tox=@pmos[toxref]

  * Perform 80 times Monte Carlo Simulation 
  * More times, the simulation result is closer to the Gaussian distribution
  dowhile run <= mc_runs
    if run > 1
      altermod @nmos[vth0] = gauss(n1vth0, 0.1, 3)
      altermod @nmos[u0] = gauss(n1u0, 0.05, 3)
      altermod @nmos[toxref] = gauss(n1tox, 0.05, 3)
      altermod @pmos[vth0] = gauss(p1vth0, 0.1, 3)
      altermod @pmos[u0] = gauss(p1u0, 0.05, 3)
      altermod @pmos[toxref] = gauss(p1tox, 0.05, 3 )
    end
    save @xbuf[v] all
    tran 10p 4n 
    meas tran delay trig v(pin) val='0.5*vp' fall=1 targ v(pout) val='0.5*vp' fall=1
    meas tran out_slew  trig v(pout) val='0.7*vp' fall=1 targ v(pout) val='0.3*vp' fall=1
    print delay >> delay.log
    print out_slew >> slew.log
    destroy all
    let run = run + 1 
  end
  rusage
  quit
.endc
.end