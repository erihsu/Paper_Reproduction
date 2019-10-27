*ng_script
* Perform Monte Carlo simulation in ngspice
* script for use with a ispd buffer. BSIM3
* circuit is in buffer.sp
* edit 'set sourcepath' for your path to circuit file
* start script by 'ngspice -o MC_buffer.log MC_buffer.sp'
*
.control 
  let mc_runs = 20
  let run = 1
  set sourcepath = (/Users/mac/Desktop/lut)
  dowhile run <= mc_runs
    set run = $&run               $ create a variable from the vector
    setseed $run                  $ set the rnd seed value to the loop index
    if run = 1
       source buffer.sp        $ load the circuit once from file, including model data
    else
       mc_source                  $ re-load the circuit from internal storage
    end
    save @xbuf[v] all
    tran 1p 4n 
    meas tran delay trig v(pin) val='0.5*vp' rise=2 targ v(pout) val='0.5*vp' rise=2
    meas tran out_slew  trig v(pout) val='0.1*vp' rise=2 targ v(pout) val='0.9*vp' rise=2
    print delay >> delay.log
    print out_slew >> slew.log
    destroy all
    remcirc
    let run = run + 1 
  end
  quit
.endc
.end