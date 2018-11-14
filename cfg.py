import os
import datetime as dt

configuration = {
"label" : "Flipkart_",
"reportable" : "1",
"tune" : "all",
"size" : "ref",
"iterations": "3",
"copies" : "1",
"threads" : "1",
"hw_vendor" : "HW_VENDOR",
"tester" : "Flipkart",
"test_sponsor" : "Flipkart",
"license_num" : "LIC-xxxx-xxxx-xxxx-xxxx",
"hw_avail" : "SEPT-2018",
"sw_avail" : "SEPT-2018",
"hw_cpu_nominal_mhz" : "2600 MHz",
"hw_cpu_max_mhz" : "3600 MHz",
"hw_model" : "XEON",
"hw_ncores" : "36",
"hw_ncpuorder" : "0-71",
"hw_nthreadspercore" : "2",
"hw_pcache" : "1200 KB",
"hw_scache" : "1500 KB",
"hw_tcache" : "104800 MB",
"fw_bios" : "INSYDE CORP."
}

tags = {
"label" : "set_name",
"reportable" : "set_report",
"tune" : "set_tune",
"size" : "set_size",
"iterations": "set_iterations",
"copies" : "set_copies",
"threads" : "set_threads",
"hw_vendor" : "set_hw",
"tester" : "set_tester",
"test_sponsor" : "set_sponser",
"license_num" : "LIC-xxxx-xxxx-xxxx-xxxx",
"hw_avail" : "set_availability",
"sw_avail" : "set_availability",
"hw_cpu_nominal_mhz" : "set_mhz",
"hw_cpu_max_mhz" : "set_mhz",
"hw_model" : "set_hw",
"hw_ncores" : "set_hw",
"hw_ncpuorder" : "set_hw",
"hw_nthreadspercore" : "set_hw",
"hw_pcache" : "set_hw",
"hw_scache" : "set_hw",
"hw_tcache" : "set_hw",
"fw_bios" : "set_hw"
}

def print_configuration():
	print("\nCURRENT CONFIGURATION:\n")
	for k,v in configuration.items():
		print(k,v)

def set_default():
	# keys = [val for val in tags.keys() if val.find("hw_") != -1 ]
	
	# for k in keys:
	# 	print(k,tags[k])

	print("\nRetrieving Hardware Info....\n")
	hw_info=os.popen('./get_hw_info.sh')
	info = hw_info.read().split('\n')

	print("Following configuration will be updated:\n")
	for i in info:
		print(i)
	update=input("Update the above configuraion(y/n)?\n")	

	if update == 'y':
		print("\nUpdating the configuration with collected Hardware Info...\n")
		for i in info:
			if i is not "":
				div=i.split('=')
		
				configuration[div[0]] = div[1].lstrip()
		print_configuration()

	else:
		print("Retaining original configuration...")
		print_configuration()

def review_conf():
	#print_configuration()
	
	print("Current configuration:\n[id] [Parameter] [Current Value]\n")
	for idx,k in enumerate(configuration.keys()):
		print(idx,k,"["+configuration[k]+"]")

	confirm = input("Any values to be modified(y/n)?\n") #+str([print(i,k) for i,k in enumerate(configuration.keys())])+"\n")
	if confirm == 'y':
		change = input("Enter comma separated values:\n")

		for i in change.split(','):
			print("Selected:",i)
			for idx,k in enumerate(configuration.keys()):
				if int(i) == idx:
					value=input("Enter value for: "+k+"\n")
					configuration[k] = value

def confirm_copiesNthreads():
	print("\nCurrent configuration:\n[id] [Parameter] [Current Value]\n")
	
	ids,ks = [],[]
	for idx,k in enumerate(configuration.keys()):
		ids.append(idx)
		ks.append(k)
		print(idx,k,"["+configuration[k]+"]")

	change=input("You want to edit no.of copies/threads/iterations(y/n)? ")
	if change == 'y':
		c=input("Enter value for copies: ")
		t=input("Enter value for threads: ")
		i=input("Enter value for iterations: ")

		print("\nUpdating with your values..\n")
		configuration['copies'] = c
		configuration['threads'] = t
		configuration['iterations'] = i
	else:
		print("Retaining(copies,threads,iterations):\n",configuration['copies'], configuration['threads'], configuration['iterations'])


def use_lines():
	
	print("\nSetting default values...\n")
	set_default()

	ln_num = [int(x) for x in "41 50 300 310 311 317 318 330 331 332 335".split()]
	
	cfg_file='/home/aic/spec2017_install/config/test_x86.cfg'

	genfile = 'genfile.txt'
	fp2 = open(genfile,'w')
	kv = {}
	with open(cfg_file) as fp:
		
		for i,line in enumerate(fp):
			
			if i+1 in ln_num:
				
				def_idx = line.find("define")
				if def_idx != -1:
					#print("define")
					parts = line.split("define ")
					key = parts[1].split()[0].replace(" ","")

					if key in configuration:
						print(key,"- Using ["+configuration[key]+"] from available values...")
						val = configuration[key]
					else:
						print(key,"Not present.");
						val,configuration[key] = input("Enter value for: "+key+"\n")

					parts = line.split(key)
					#new_def = parts[0]+key+" "+val
					new_def = parts[0]+key+" "+str(configuration[key])
					#print("NEW_DEF:",new_def)
					fp2.write(new_def)

				eq_idx = line.find("=")
				if eq_idx != -1:
					
					parts = line.split("=")
					key = parts[0].replace(" ","")
					if key in configuration:
						print(key,"- Using ["+configuration[key]+"] from available values...")
						val = configuration[key]
					else:
						print(key,"Not present.");
						val,configuration[key] = input("Enter value for: "+key+"\n")

					new_eq = parts[0]+"= "+val+"\n"

					fp2.write(new_eq)
			else:
				fp2.write(line)
	print("Using following configuration:")
	for k,v in kv.items():
		print(k,v) 
	print("Generated: ",genfile)
	fp2.close()

def read_conf_from_user():
	for k in configuration.keys():
		print("Enter value for:",k)
		configuration[k] = input()


###--------- SPECJBB 2015 -------

jbb_conf={
	"date":""+str(dt.datetime.now().strftime("%b-%Y")),
	"testSponsor":"TEST_SPONSOR",
	"hwVendor":"HW_VENDOR",
	"hwVendorUrl":"www.hwvendorurl.com"

}

def set_multijvm_conf():
	print()