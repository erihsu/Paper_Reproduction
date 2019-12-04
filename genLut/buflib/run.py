import numpy as np 
import os

slew_in_list =  [50,55,60,65,70,75,80] #ps
cap_load_list = [15,20,25,30,35,40,45] #fF

lut_rise = np.zeros((len(slew_in_list),len(cap_load_list),5),dtype=np.float32)
lut_fall = np.zeros((len(slew_in_list),len(cap_load_list),5),dtype=np.float32)

buffer_size_lib = {'X1':[2,1.37],'X2':[4,2.74],
				   'X3':[8,5.48],'X4':[16,10.96],
				   'X5':[32,21.92]}

def get_lut(option="fall",i=0,j=0):
	string2 = "ngspice -o MC_buffer_{}.log MC_buffer_{}.sp".format(option,option)
	os.system(string2)

	result1 = np.loadtxt('delay.log',delimiter=' ',usecols=(2)).astype(np.float32)
	result2 = np.loadtxt( 'slew.log',delimiter=' ',usecols=(2)).astype(np.float32)
	result3 = np.loadtxt( 'power.log',delimiter=' ',usecols=(2)).astype(np.float32)

	string3 = "rm bsim4v5.out *.log"
	os.system(string3)
	if option == "fall":
		lut_fall[i,j,0] = np.mean(result1).astype(np.float32) #mu of delay
		lut_fall[i,j,1] = np.std(result1).astype(np.float32)  #sigma of delay
		lut_fall[i,j,2] = np.mean(result2).astype(np.float32) #mu of output slew
		lut_fall[i,j,3] = np.std(result2).astype(np.float32)  #sigma of output slew
		lut_fall[i,j,4] = result3.astype(np.float32)          #power dissiption
	else:
		lut_rise[i,j,0] = np.mean(result1).astype(np.float32) #mu of delay
		lut_rise[i,j,1] = np.std(result1).astype(np.float32)  #sigma of delay
		lut_rise[i,j,2] = np.mean(result2).astype(np.float32) #mu of output slew
		lut_rise[i,j,3] = np.std(result2).astype(np.float32)  #sigma of output slew
		lut_rise[i,j,4] = result3.astype(np.float32)          #power dissiption

def main():
	for key,value in buffer_size_lib.items():
		os.system("sed -i -e 's/pmos l=45n w=[0-9]*\.?[0-9]+u/pmos l=45n w={}u/g' \
						  -e 's/nmos l=45n w=[0-9]*\.?[0-9]+u/nmos l=45n w={}u/g' buffer.sp".format(value[0],value[1]))
		for i,slew_in in enumerate(slew_in_list):
			for j,cap_load in enumerate(cap_load_list):
				os.system("sed -i -e 's/capload = [0-9]\+fF/capload = {}fF/g' \
								  -e 's/slew_in = [0-9]\+ps/slew_in = {}ps/g' buffer.sp".format(cap_load,slew_in))
				get_lut("fall",i,j)
				get_lut("rise",i,j)

		os.mkdir("./{}".format(key))
		with open('./{}/lut_fall.txt'.format(key),'w') as f1, open('./{}/lut_rise.txt'.format(key),'w') as f2:
			f1.write("delay(miu){}delay(sigma){}slew(miu){}slew(sigma){}power{}input_slew{}output_cap\n".format(' '*12,' '*12,' '*12,' '*12,' '*12,' '*12,' '*12))
			f2.write("delay(miu){}delay(sigma){}slew(miu){}slew(sigma){}power{}input_slew{}output_cap\n".format(' '*12,' '*12,' '*12,' '*12,' '*12,' '*12,' '*12))
			for i in range(len(slew_in_list)):
				for j in range(len(cap_load_list)):
					f1.write("{} {} {} {} {} {} {}\n".format(lut_fall[i,j,0],lut_fall[i,j,1],lut_fall[i,j,2],lut_fall[i,j,3],lut_fall[i,j,4],slew_in_list[i],cap_load_list[j]))
					f2.write("{} {} {} {} {} {} {}\n".format(lut_rise[i,j,0],lut_rise[i,j,1],lut_rise[i,j,2],lut_rise[i,j,3],lut_rise[i,j,4],slew_in_list[i],cap_load_list[j]))


if __name__ == '__main__':
	main()
