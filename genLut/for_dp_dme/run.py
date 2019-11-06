import numpy as np 
import os

slew_in_list =  [50,55,60,65,70,75,80] #ps
slew_out_list = [50,55,60,65,70,75,80] #ps

lut_rise = np.zeros((len(slew_in_list),len(slew_out_list)),dtype=np.float32)
lut_fall = np.zeros((len(slew_in_list),len(slew_out_list)),dtype=np.float32)


def get_lut(slin,slout,option="fall",i=0,j=0):

	string1 = "sed -i -e 's/let slew_out = [0-9]\+ps/let slew_out = {}ps/g' -e 's/slew_in = [0-9]\+ps/slew_in = {}ps/g' load_cap_{}.sp".format(slout,slin,option)
	os.system(string1)
	string2 = "ngspice load_cap_{}.sp".format(option,option)
	os.system(string2)

	result = np.loadtxt('loadcap.log',delimiter=' ',usecols=(2)).astype(np.float32)

	string3 = "rm bsim4v5.out *.log"
	os.system(string3)
	if option == "fall":
		lut_fall[i,j] = float(result) 
	else:
		lut_rise[i,j] = float(result)

def main():
	for i,slew_in in enumerate(slew_in_list):
		for j,slew_out in enumerate(slew_out_list):
			get_lut(slew_in,slew_out,"fall",i,j)
			get_lut(slew_in,slew_out,"rise",i,j)

	with open('lut_fall.txt','w') as f1, open('lut_rise.txt','w') as f2:
		f1.write("buffer_load(fF){}input_slew{}output_slew\n".format(' '*12,' '*12))
		f2.write("buffer_load(fF){}input_slew{}output_slew\n".format(' '*12,' '*12))
		for i in range(len(slew_in_list)):
			for j in range(len(slew_out_list)):
				f1.write("{} {} {}\n".format(lut_fall[i,j],slew_in_list[i],slew_out_list[j]))
				f2.write("{} {} {}\n".format(lut_rise[i,j],slew_in_list[i],slew_out_list[j]))

if __name__ == '__main__':
	main()
