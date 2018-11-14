import os
import time
#import subprocess
PRNT = False	#True #
from cfg import *
#mymanual = configure.manual

def label_pp():
	lbl_pp=r"""#--------- Label --------------------------------------------------------------
# Arbitrary string to tag binaries (no spaces allowed)
#                  Two Suggestions: # (1) EDIT this label as you try new ideas.
%define label """+ configuration["label"] +"""                # (2)      Use a label meaningful to *you*.


#--------- Preprocessor -------------------------------------------------------
%ifndef %{bits}                # EDIT to control 32 or 64 bit compilation.  Or,
%   define  bits        64     #      you can set it on the command line using:
%endif                         #      'runcpu --define bits=nn'

%ifndef %{build_ncpus}         # EDIT to adjust number of simultaneous compiles.
%   define  build_ncpus 8      #      Or, you can set it on the command line:
%endif                         #      'runcpu --define build_ncpus=nn'

# Don't change this part.
%define    os           LINUX
%if %{bits} == 64
%   define model        -m64
%elif %{bits} == 32
%   define model        -m32
%else
%   error Please define number of bits - see instructions in config file
%endif
%if %{label} =~ m/ /
%   error Your label "%{label}" contains spaces.  Please try underscores instead.
%endif
%if %{label} !~ m/^[a-zA-Z0-9._-]+$/
%   error Illegal character in label "%{label}".  Please use only alphanumerics, underscore, hyphen, and period.
%endif
	"""

	if PRNT:
		print(lbl_pp)

	return lbl_pp

def pre_env():
	preenv="""

# EDIT if needed: the preENV line adds library directories to the runtime
#      path.  You can adjust it, or add lines for other environment variables.
#      See: https://www.spec.org/cpu2017/Docs/config.html#preenv
#      and: https://gcc.gnu.org/onlinedocs/gcc/Environment-Variables.htmli

%define gcc_dir /usr
preENV_LD_LIBRARY_PATH  = %{gcc_dir}/lib64/:%{gcc_dir}/lib/:/lib64
#preENV_LD_LIBRARY_PATH  = %{gcc_dir}/lib64/:%{gcc_dir}/lib/:/lib64:%{ENV_LD_LIBRARY_PATH}
SPECLANG                = %{gcc_dir}/bin/
CC                      = $(SPECLANG)gcc     -std=c99   %{model}
CXX                     = $(SPECLANG)g++     -std=c++03 %{model}
FC                      = $(SPECLANG)gfortran           %{model}
# How to say "Show me your version, please"
CC_VERSION_OPTION       = --version
CXX_VERSION_OPTION      = --version
FC_VERSION_OPTION       = --version
"""
	if PRNT:
		print(preenv)
	return preenv

def global_settings():
	gbl_settings= r"""
#--------- Global Settings ----------------------------------------------------
# For info, see:
#            https://www.spec.org/cpu2017/Docs/config.html#fieldname
#   Example: https://www.spec.org/cpu2017/Docs/config.html#tune

command_add_redirect = 1
flagsurl             = $[top]/config/flags/gcc.xml
ignore_errors        = 1
label                = %{label}-m%{bits}
line_width           = 1020
log_line_width       = 1020
makeflags            = --jobs=%{build_ncpus}
mean_anyway          = 1
output_format        = txt,html,cfg,pdf,csv
preenv               = 1
reportable           = """+ configuration["reportable"] +"""
iterations           = """+ configuration["iterations"] +"""
tune                 = """+ configuration["tune"] +"""
size				 = """+ configuration["size"]

# print("iterations	= ",iterations)
# print("reportable	= ",reportable)
# print("tune		= ",tune)

	if PRNT:
		print(gbl_settings)

	return gbl_settings


def set_cpus():
	cpu_settings = r"""
#--------- How Many CPUs? -----------------------------------------------------
# Both SPECrate and SPECspeed can test multiple chips / cores / hw threads
#    - For SPECrate,  you set the number of copies.
#    - For SPECspeed, you set the number of threads.
intrate,fprate:
   copies           = """+ configuration["copies"] +"""   
intspeed,fpspeed:
   threads          = """+ configuration["threads"] +"""
	"""

	if PRNT:
		print(cpu_settings)

	return cpu_settings


def portability():
	port = r"""
#--------- Portability --------------------------------------------------------
default:               # data model applies to all benchmarks
%if %{bits} == 32
    # Strongly recommended because at run-time, operations using modern file
    # systems may fail spectacularly and frequently (or, worse, quietly and
    # randomly) if a program does not accommodate 64-bit metadata.
    EXTRA_PORTABILITY = -D_FILE_OFFSET_BITS=64
%else
    EXTRA_PORTABILITY = -DSPEC_LP64
%endif

# Benchmark-specific portability (ordered by last 2 digits of bmark number)

500.perlbench_r,600.perlbench_s:  #lang='C'
%if %{bits} == 32
%   define suffix IA32
%else
%   define suffix X64
%endif
   PORTABILITY    = -DSPEC_%{os}_%{suffix}

521.wrf_r,621.wrf_s:  #lang='F,C'
   CPORTABILITY  = -DSPEC_CASE_FLAG
   FPORTABILITY  = -fconvert=big-endian

523.xalancbmk_r,623.xalancbmk_s:  #lang='CXX'
   PORTABILITY   = -DSPEC_%{os}

526.blender_r:  #lang='CXX,C'
   PORTABILITY   = -funsigned-char -DSPEC_LINUX

527.cam4_r,627.cam4_s:  #lang='F,C'
   PORTABILITY   = -DSPEC_CASE_FLAG

628.pop2_s:  #lang='F,C'
   CPORTABILITY    = -DSPEC_CASE_FLAG
   FPORTABILITY    = -fconvert=big-endian

	"""

	if PRNT:
		print(port)

	return port

def optimization():
	
	opt=r"""
intspeed:
   OPTIMIZE       = -DSPEC_SUPPRESS_OPENMP
657.xz_s=peak:
   OPTIMIZE       = -fopenmp  -DSPEC_OPENMP 
fpspeed:
   OPTIMIZE       = -fopenmp 
   EXTRA_OPTIMIZE = -DSPEC_OPENMP
"""

	if PRNT:
		print(opt)

	return opt

def sut_tester_info():
	
	info = r"""
#------------------------------------------------------------------------------
# Tester and System Descriptions - EDIT all sections below this point
#------------------------------------------------------------------------------
#   For info about any field, see
#             https://www.spec.org/cpu2017/Docs/config.html#fieldname
#   Example:  https://www.spec.org/cpu2017/Docs/config.html#hw_memory
#-------------------------------------------------------------------------------

#--------- EDIT to match your version -----------------------------------------
default:
   sw_compiler001   = C/C++/Fortran: """+str(os.popen("gcc --version | head -n 1").read())+"""
   sw_compiler002   = GNU Compiler Collection

#--------- EDIT info about you ------------------------------------------------
# To understand the difference between hw_vendor/sponsor/tester, see:
#     https://www.spec.org/cpu2017/Docs/config.html#test_sponsor
intrate,intspeed,fprate,fpspeed: # Important: keep this line
   hw_vendor          = """+configuration["hw_vendor"]+"""
   tester             = """+configuration["tester"]+"""
   test_sponsor       = """+configuration["test_sponsor"]+"""
   license_num        = """+configuration["license_num"]+"""				#nnn (Your SPEC license number)
#  prepared_by        = 				# Whatever you like: is never output


# #--------- EDIT system availability dates -------------------------------------
# intrate,intspeed,fprate,fpspeed: # Important: keep this line
#                         # Example                             # Brief info about field
   hw_avail           = """+configuration["hw_avail"]+"""				# Date of LAST hardware component to ship
   sw_avail           = """+configuration["sw_avail"]+"""				# Date of LAST software component to ship

#--------- EDIT system information --------------------------------------------
intrate,intspeed,fprate,fpspeed: # Important: keep this line
                        # Example                             # Brief info about field
#  hw_cpu_name        = 				# chip name
   hw_cpu_nominal_mhz = """+configuration["hw_cpu_nominal_mhz"]+"""				# Nominal chip frequency, in MHz
   hw_cpu_max_mhz     = """+configuration["hw_cpu_max_mhz"]+"""				# Max chip frequency, in MHz
#  hw_disk            = 				# Size, type, other perf-relevant info
   hw_model           = """+configuration["hw_model"]+"""				# system model name
#  hw_nchips          = 				# number chips enabled
   hw_ncores          = """+configuration["hw_ncores"]+"""				# number cores enabled
   hw_ncpuorder       = """+configuration["hw_ncpuorder"]+"""				# Ordering options
   hw_nthreadspercore = """+configuration["hw_nthreadspercore"]+"""				# number threads enabled per core
   hw_other           = 				# Other perf-relevant hw, or "None"

#  hw_memory001       = 				# The 'PCn-etc' is from the JEDEC
#  hw_memory002       = 				# label on the DIMM.

   hw_pcache          = """+configuration["hw_pcache"]+"""			   # Primary cache size, type, location
   hw_scache          = """+configuration["hw_scache"]+"""		       # Second cache or "None"
   hw_tcache          = """+configuration["hw_tcache"]+"""	           # Third  cache or "None"
   #hw_ocache          = # 9 GB I+D off chip per system board  # Other cache or "None"

   fw_bios            = """+configuration["fw_bios"]+"""	# American Megatrends 39030100 02/29/2016 # Firmware information
#  sw_file            = # ext99                               # File system
#  sw_os001           = # Linux Sailboat                      # Operating system
#  sw_os002           = # Distribution 7.2 SP1                # and version
#   sw_other           = # TurboHeap Library V8.1              # Other perf-relevant sw, or "None"
#  sw_state           = # Run level 99                        # Software state.
	"""

	if PRNT:
		print(info)
	return info

def input_opts_in_file(runcpus,readers):

	file1 = "runcpus.cfg"
	file2 = "readers.cfg"
	f1 = open(file1,"w")
	f2 = open(file2,"w")

	for i in runcpus:
		f1.write(i+"	= \n")

	for i in readers:
		f2.write(i+"	= \n")

	print("Please enter your values in:\n",file1,file2)

def read_values_from_files():
	print("= STILL TO BE DONE =")	

def create_options():
	runcpus,readers = get_runcpu_opts()
	print("RUNCPUS:\n",runcpus,"\nREADERS:\n",readers)
	input_opts_in_file(runcpus,readers)


def generate_cfg(in_manual):

	global manual

	manual = in_manual

	lbl = label_pp()
	preEnv = pre_env()

	gbl = global_settings()
	cpus = set_cpus()
	porting = portability()
	info = sut_tester_info()

	fname = configuration['label']+'x'+configuration['copies']+'c_'+configuration['threads']+'th_'+configuration['iterations']+'i_'+configuration['size']+'s.cfg'	#input("Please enter config filename to generate...\n")
	print("GENERATING Config file:\n",fname,"\nwith following configuration:\n")
	for k,v in configuration.items():
		print(k,v)

	f = open(fname,'w')
	print("Writing: LABEL...\n");time.sleep(2)
	f.write(lbl)

	print("Writing: preENV...\n");time.sleep(2)
	f.write(preEnv)

	opt_confirm = input("Want to enable parallelism(y/n)? ")
	if opt_confirm == 'y':
		opt = optimization()
		print("Writing: OPTIMIZATION...\n");time.sleep(2)
		f.write(opt)
	else:
		print("Parallelism Disabled.")

	print("Writing: GLOBAL SETTINGS...\n");time.sleep(2)
	f.write(gbl)

	print("Writing: CPU INFO...\n");time.sleep(2)
	f.write(cpus)

	print("Writing: PORTABILITY SETTINGS...\n");time.sleep(2)
	f.write(porting)

	print("Writing: TESTER INFO...\n");time.sleep(2)
	f.write(info)

	f.close()
	print("Config file:\n"+fname+"\ngenerated.")

##------------------------ Multi JVM  Configuration --------------
def execute(cmd):
	return  str(os.popen(cmd).read())

def gen_multijvm_cfg():
	hw_output=os.popen("./get_hw_info.sh jbb").read()
	multi_jvm_cfg2=r"""
#
# SAMPLE SPECJBB2015-MultiJVM SUBMISSION TEMPLATE
#

# ----------------------------------------- Benchmark and test descriptions -------------------------------------------
#
jbb2015.test.specLicense=LIC-XXXX-XXXX-XXX
jbb2015.test.date="""+jbb_conf["date"]+"""
jbb2015.test.internalReference=www.myreference.com
jbb2015.test.location=Bengaluru
jbb2015.test.testSponsor="""+jbb_conf["testSponsor"]+"""
jbb2015.test.testedBy="""+jbb_conf["testSponsor"]+"""
jbb2015.test.testedByName="""+jbb_conf["testSponsor"]+"""
jbb2015.test.hwVendor="""+jbb_conf["hwVendor"]+"""
jbb2015.test.hwSystem="""+jbb_conf["hwVendor"]+"""
# Enter latest availability dates for hw and sw when using multiple components
jbb2015.test.hwAvailability="""+jbb_conf["date"]+"""
jbb2015.test.swAvailability="""+jbb_conf["date"]

	multi_jvm_cfg=r""""""+hw_output+"""
# ---------------------------------------------- Config descriptions for unique jvm instances -------------------------
#
# Describe unique JVM instances using following format:
# jbb2015.config.jvmInstances.<JVM Instance label>.<param> = <value>
# Different jvm_product, agent running, cmdline, tuning, or notes requires unique JVM instance label
# Sample configuration for "jvm_Ctr_1" JVM instance
# What component is running on this JVM
jbb2015.config.jvmInstances.jvm_Ctr_1.agents = Controller
# can be Controller, TxInjector, Backend for multiJVM and Distributed category 
# can be Composite for Composite category
jbb2015.config.jvmInstances.jvm_Ctr_1.jvm_product=jvm_1
# This MUST be one of the jvm product
jbb2015.config.jvmInstances.jvm_Ctr_1.cmdline= -ms256m -mx1024m
jbb2015.config.jvmInstances.jvm_Ctr_1.tuning=affinity note 1 <ul><li>note 2</li></ul>
jbb2015.config.jvmInstances.jvm_Ctr_1.notes="Notes here"
# Sample configuration for "jvm_Backend_1" JVM instance
jbb2015.config.jvmInstances.jvm_Backend_1.agents = Backend
jbb2015.config.jvmInstances.jvm_Backend_1.jvm_product=jvm_1
jbb2015.config.jvmInstances.jvm_Backend_1.cmdline= -Xms24g -Xmx24g -Xmn20g
jbb2015.config.jvmInstances.jvm_Backend_1.tuning=affinity note 1 <ul><li>note 2</li></ul>
jbb2015.config.jvmInstances.jvm_Backend_1.notes="Notes here"
# Sample configuration for "jvm_TxInjector_1" JVM instance
jbb2015.config.jvmInstances.jvm_TxInjector_1.agents = TxInjector
jbb2015.config.jvmInstances.jvm_TxInjector_1.jvm_product=jvm_1
jbb2015.config.jvmInstances.jvm_TxInjector_1.cmdline= -Xms2g -Xmx2g
jbb2015.config.jvmInstances.jvm_TxInjector_1.tuning=affinity note 1 <ul><li>note 2</li></ul>
jbb2015.config.jvmInstances.jvm_TxInjector_1.notes="Notes here"
# ----------------------------------- Config descriptions for unique OS Images ---------------------------------------
#
# Describe unique OS image participated in the run in this section using following format.
# jbb2015.config.osImages.<OS Image label>.<param> = <value>
# Any OS image which is different for os_product, tuning, notes or running jvm instances need to have 
# unique os image label
# Sample configuration for "os_Image_1" OS image
# Provide the comma-separated list of <JVM Instances label>(num of Instances of that type)
# which were running on this OS image.
# JVM labels should match those from previous section "JVM Instances descriptions"
jbb2015.config.osImages.os_Image_1.jvmInstances = jvm_Ctr_1(1), jvm_Backend_1(4), jvm_TxInjector_1(4) 
# This OS image has jvm instances 1 for Ctr, 4 for TxI and 4 for Backends
jbb2015.config.osImages.os_Image_1.os_product= os_1
jbb2015.config.osImages.os_Image_1.tuning=<ul><li>bufcache=1024</li><li>threads=65536</li></ul>
jbb2015.config.osImages.os_Image_1.notes=None
# ----------------------------- Config descriptions for OS images deployed on a SUT hw -----------------------------
#
# Describe how OS Images are deployed across systems
# The common syntax is:
# jbb2015.config.SUT.system.<config label>.<param> = <value>
# Sample configuration for "config_1" host
# Each config has one or more OS images running.
# Provide the comma-separated list of OS image labels which were running on this host.
# OS image labels should match those from previous section "OS image descriptions"
# format <os Image label (num of OS Image Instances deployed per system)>
jbb2015.config.SUT.system.config_1.osImages = os_Image_1(1)
jbb2015.config.SUT.system.config_1.hw_product = hw_1
jbb2015.config.SUT.system.config_1.nSystems = 1
jbb2015.config.SUT.system.config_1.tuning = tuning
jbb2015.config.SUT.system.config_1.notes = notes
jbb2015.config.SUT.system.config_1.swEnvironment = non-virtual

#
# ---------------------------------------- DO NOT EDIT BELOW THIS LINE -----------------------------------------------
#

#
# Only SPEC office is allowed to edit lines below
#

# This field either be empty or encoded value placed by reporter. Any other text will result in error
jbb2015.result.data=

# Can only be set to [ PASSED / NA / NC / CD ]  where
# PASSED: accepted; NA: non-available; NC: non-compliant; CD: code defect;
jbb2015.result.compliant=

# Text explaining reason for Acceptance of a warning
jbb2015.result.compliant.warning.waived.reason=

# Text explaining reason for NC/NA/CD marking or Acceptance of an error
jbb2015.result.compliant.reason=

# Link to replacement result if available
jbb2015.result.compliant.remedy=

jbb2015.result.category=<set by reporter>
jbb2015.result.group.count=<set by reporter>
jbb2015.result.metric.max-jOPS=<set by reporter>
jbb2015.result.metric.critical-jOPS=<set by reporter>
jbb2015.result.SLA-10000-jOPS=<set by reporter>
jbb2015.result.SLA-25000-jOPS=<set by reporter>
jbb2015.result.SLA-50000-jOPS=<set by reporter>
jbb2015.result.SLA-75000-jOPS=<set by reporter>
jbb2015.result.SLA-100000-jOPS=<set by reporter>

jbb2015.spec.publication.date=MMM DD, YYYY
jbb2015.spec.updated.date=<date the result was last updated by SPEC>

# Link to full disclosure report
jbb2015.spec.disclosure.url=OnSUBMISSION

jbb2015.benchmark.version = 1.01
jbb2015.benchmark.version.date = """+jbb_conf["date"]

	#print("\n\nFINAL CONFIGURATION:\n"+multi_jvm_cfg)
	jbb_f='jbb_multijvm.conf'
	fp=open(jbb_f,'w')
	fp.write(multi_jvm_cfg)
	fp.close()
	print("JBB Configuration written to: "+multi_jvm_cfg)
