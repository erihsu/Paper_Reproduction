import numpy as np 
import os

slew_in_list = [14,20]
cap_load_list = [35,40]

lut_rise = np.zeros((len(slew_in_list),len(cap_load_list),4),dtype=np.float32)
lut_fall = np.zeros((len(slew_in_list),len(cap_load_list),4),dtype=np.float32)

def main():
	for i,slew_in in enumerate(slew_in_list):
		for j,cap_load in enumerate(cap_load_list):

			string1 = "sed -i -e 's/capload = [0-9]\+fF/capload = {}fF/g' -e 's/slew_in = [0-9]\+ps/slew_in = {}ps/g' buffer.sp".format(cap_load,slew_in)
			os.system(string1)

			string2 = "ngspice -o MC_buffer.log MC_buffer.sp"
			os.system(string2)

			result1 = np.loadtxt('delay.log',delimiter=' ',usecols=(2)).astype(np.float32)
			result2 = np.loadtxt( 'slew.log',delimiter=' ',usecols=(2)).astype(np.float32)

			string3 = "rm delay.log slew.log"
			os.system(string3)

			lut_fall[i,j,0] = np.mean(result1).astype(np.float32) 
			lut_fall[i,j,1] = np.std(result1).astype(np.float32) 
			lut_fall[i,j,2] = np.mean(result2).astype(np.float32)
			lut_fall[i,j,3] = np.std(result2).astype(np.float32)

	with open('lut_fall.txt','w') as f1:
		f1.write("delay(miu){}delay(sigma){}slew(miu){}slew(sigma)\n".format(' '*12,' '*12,' '*12,' '*12))
		for i in range(len(slew_in_list)):
			for j in range(len(cap_load_list)):
				f1.write("{} {} {} {}\n".format(lut_fall[i,j,0],lut_fall[i,j,1],lut_fall[i,j,2],lut_fall[i,j,3]))

if __name__ == '__main__':
	main()
