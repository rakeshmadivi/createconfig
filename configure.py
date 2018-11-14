from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import psutil
import re
import webbrowser
import requests as req
from bs4 import BeautifulSoup as BS
import time

from cfg import *

# test_listing_cfg

#from echo_config import *
import echo_config as ec
manual = ""
 
raw_dmi = r"""0   BIOS
1   System
2   Baseboard
3   Chassis
4   Processor
5   Memory Controller
6   Memory Module
7   Cache
8   Port Connector
9   System Slots
10   On Board Devices
11   OEM Strings
12   System Configuration Options
13   BIOS Language
14   Group Associations
15   System Event Log
16   Physical Memory Array
17   Memory Device
18   32-bit Memory Error
19   Memory Array Mapped Address
20   Memory Device Mapped Address
21   Built-in Pointing Device
22   Portable Battery
23   System Reset
24   Hardware Security
25   System Power Controls
26   Voltage Probe
27   Cooling Device
28   Temperature Probe
29   Electrical Current Probe
30   Out-of-band Remote Access
31   Boot Integrity Services
32   System Boot
33   64-bit Memory Error
34   Management Device
35   Management Device Component
36   Management Device Threshold Data
37   Memory Channel
38   IPMI Device
39   Power Supply
40   Additional Information
41   Onboard Devices Extended Information
42   Management Controller Host Interface"""

raw_runcpu = r"""
action allow_label_overrideNew backup_config basepeak bind check_version command_add_redirect copies current_range delay deletework difflines enable_monitorNew env_vars expand_notes expid fail fail_build fail_run feedback flagsurl force_monitorNew http_proxy http_timeout idle_current_range ignore_errors ignore_sigint info_wrap_columns iterations keeptmp line_width labelNew locking log_line_width log_timestamp mail_reports mailcompress mailmethod mailport mailserver mailto make make_no_clobber makeflags mean_anyway minimize_builddirs minimize_rundirs no_input_handler no_monitor nobuild notes_wrap_columns notes_wrap_indent output_format output_root parallel_test parallel_test_submit parallel_test_workloadsNew plain_train powerNew power_analyzer preenv rebuild reportable runlist save_build_filesNew section_specifier_fatal setprocgroup size src.alt strict_rundir_verify sysinfo_program table teeout temp_meter train_single_threadNew train_with tune use_submit_for_compareNew use_submit_for_speed verbose verify_binariesNew version_url voltage_range
"""

readers_full = r"""
fw_biosNew hw_avail hw_cpu_max_mhzNew hw_cpu_name hw_cpu_nominal_mhzNew hw_disk hw_memory hw_model hw_nchips hw_ncores hw_ncpuorder hw_nthreadspercore hw_ocache hw_other hw_pcache hw_power_{id}_cal_dateNew hw_power_{id}_cal_label hw_power_{id}_cal_org hw_power_{id}_met_inst hw_power_{id}_connection hw_power_{id}_label hw_power_{id}_model hw_power_{id}_serial hw_power_{id}_setup hw_power_{id}_vendor hw_psu hw_psu_info hw_scache hw_tcache hw_vendor license_num prepared_by sw_avail sw_base_ptrsize sw_compiler sw_file sw_os sw_state sw_other sw_peak_ptrsize tester test_sponsor
"""

def get_runcpu_opts():
	runcpu_opts = raw_runcpu.split()

	runcpus = []
	readers = []

	
	for opt in runcpu_opts:
		found = opt.find("New")
		if found != -1:
			print(opt," Found @",found,"/",len(opt))
			runcpus.append(opt[:-3])
		else:	
			runcpus.append(opt)

	readers_opts = readers_full.split()
	for opt in readers_opts:
		found = opt.find("New")
		if found != -1:
			print(opt," Found @",found,"/",len(opt))
			readers.append(opt[:-3])
		else:	
			readers.append(opt)

	return runcpus,readers


def getdmi():
	dmi_list = re.split('\n',raw_dmi)#dmi.split('')

	dmi_dict = {}

	for i in dmi_list:
		print(i)
		#print(i.split('   '))
		info = i.split('   ')

		dmi_dict[str(info[0])] = info[1]

		print(len(info))


	for k,v in dmi_dict.items():
		print(k,v)

def get_content(link):
	
	print("Using link:",link)

	resp = req.get(link)

	#http_respone 200 means OK status 
	if resp.status_code==200: 
		print("Successfully opened the web page") 
		print("The news are as follow :-\n") 

		# we need a parser,Python built-in HTML parser is enough . 
		soup=BS(resp.text,'html.parser')     

		# # l is the list which contains all the text i.e news  
		# l=soup.find("ul",{"class":"searchNews"}) 

		# #now we want to print only the text part of the anchor. 
		# #find all the elements of a, i.e anchor 
		# for i in l.findAll("a"): 
		# 	print(i.text)

		badges = soup.body.find('span')
		print(badges);exit()
		for span in badges.span.find('span', recursive=False):
		    print(span.attrs['title'])
     
	else: 
		print("Error")


def open_in_browser(link):
	#my_browser="/usr/bin/google-chrome-statble %s"
	#a_website = "https://www.spec.org/cpu2017/Docs/runcpu.html#runlist"

	# Open url in a new window of the default browser, if possible
	#webbrowser.get(my_browser).open_new(a_website)
	webbrowser.open_new(link)

	# Open url in a new page (“tab”) of the default browser, if possible
	#webbrowser.open_new_tab(a_website)

	#webbrowser.open(a_website, 1) # Equivalent to: webbrowser.open_new(a_website)
	#webbrowser.open(a_website, 2) # Equivalent to: webbrowser.open_new_tab(a_website)


def livegraph():

	plt.rcParams['animation.html'] = 'jshtml'
	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)

	fig.show()

	x,y = [],[]

	i = 0

	while True:
		x.append(i)
		y.append(psutil.cpu_percent())
		ax1.plot(x,y,color='blue',markevery=1)
		fig.canvas.draw()
		time.sleep(0.1)
		i += 1

		#ani = animation.FuncAnimation(fig, animate, interval=1000)
		#plt.show()

def main():
	#livegraph()
	#print(len(dmi.split()))
	#getdmi()
	#open_in_browser()

	#req_link=r"https://www.spec.org/cpu2017/Docs/runcpu.html#"

	#get_content(req_link+"runlist")
	#create_options()
	#generate_cfg()
	#
	# manual = input("Do you want to enter options manually...(y/n)?\n")
	# if manual == "y" :
	# 	using_lines=input("Insert at lines(y/n)?\n")
	# 	if using_lines == 'y':
	# 		use_lines()
	# 	else:
	# 		read_conf_from_user()
	# 		print_configuration()
	# 		ec.generate_cfg(manual)
	# else:
	gen_cfg=input("Which one you want to generate?\n1. SPECCPU2017\n2. SPECJBB2015\nEnter Value: ")
	if gen_cfg == "1":
		print("Generating Configuration for SPECCPU2017\n")
		#print_configuration()
		print("\nUpdating Configuration with Hardware Info...\n")
		set_default()
		#review_conf()
		confirm_copiesNthreads()

		time.sleep(3)
		ec.generate_cfg(manual)
	else:
		print("Generating Configuration for SPECJBB2015\n")
		print("\nUpdating Configuration with Hardware Info...\n")
		#set_default()
		set_multijvm_conf()
		ec.gen_multijvm_cfg()




main()