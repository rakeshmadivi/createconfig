bios=`sudo dmidecode -t bios | head -n8 | tail -n 2 | cut -f2 -d ':'`

# echo $bios

ncpus=$(echo `lscpu | egrep "^CPU\(s\):" | cut -f2 -d ':'`)

#echo $ncpus

mhz=$(echo `lscpu | egrep "MHz:" | cut -f2 -d ':'`)

#echo $mhz

corespersock=$(echo `lscpu | egrep "^Core\(s\)" | cut -f2 -d ':'`)
#echo CORESperSOCK: $corespersock

thpercore=$(echo `lscpu | egrep "Thread" | cut -f2 -d ':'`)
#echo $thpercore

sockets=$(echo `lscpu | egrep "^Socket" | cut -f2 -d ':'`)
#echo SOCKETS: $sockets

arch=$(echo `lscpu | egrep "Arch" | cut -f2 -d ':'`)
# echo $arch

vendor=$(echo `sudo dmidecode -t system | egrep "Manufacturer:" | cut -f2 -d ':' `)
# echo $vendor

model=$(echo `sudo dmidecode -t system | egrep "Product Name:" | cut -f2 -d':'`)
# echo $model

l1cache=$(echo `lscpu | egrep "L1" | cut -f2 -d ':'`)
# echo $l1cache

l2cache=$(echo `lscpu | egrep "L2" | cut -f2 -d ':'`)
# echo $l2cache

l3cache=$(echo `lscpu | egrep "L3" | cut -f2 -d ':'`)
# echo $l3cache

order=$((ncpus - 1))
# echo ORDER: $order

nominal=$(echo `sudo dmidecode -t processor | egrep "Max Speed:|Current Speed:" | sort |uniq |head -n1 |cut -f2 -d':'`)
max=$(echo `sudo dmidecode -t processor | egrep "Max Speed:|Current Speed:" | sort |uniq |tail -n1 |cut -f2 -d':'`)

nodes=$(echo `lscpu|grep "NUMA node("| awk -n '{print $3}'`)

disk=$(echo `sudo lshw -short | grep disk| awk '{for(i=4;i<=NF;i++)printf "%s ",$i;print ""}'`)


memory=$(echo `sed -n '1p' /proc/meminfo |awk -n '{print $2}'`)
#printf "Memory: $memory\n"
mem_in_GB=$(echo `echo "scale=2;${memory}/1024/1024" | bc -l`)


mem_dimms=$(echo `sudo lshw -class memory| egrep "-memory:"| wc -l`)
#mem_dimms=2
network=$(echo `sudo lshw -short | grep network | awk '{for(i=4;i<=NF;i++)printf "%s ",$i; print ""}'`)

avail=`date +%b-%Y`

cpuname=$(echo `lscpu | sed -n '13p'| cut -f2 -d ':'`)


osn=`uname -o`
osnv=`uname -n`
osv=`uname -v`
osr=`uname -r`
osa=`uname -m`

tester=TESTER


if [ $# -eq 0 ];then
	#: '
	echo hw_cpu_max_mhz=$max	#`echo $mhz| cut -f2 -d' ' ` #set_mhz
	echo hw_nthreadspercore=$thpercore #set_hw
	echo hw_pcache=$l1cache #set_hw
	echo hw_tcache=$l3cache #set_hw
	echo hw_cpu_nominal_mhz=$nominal
	echo hw_vendor=$vendor #set_hw
	echo hw_ncpuorder=`echo 0 - $order`
	echo hw_avail=`date +%b-%Y` #set_availability
	echo sw_avail=`date +%b-%Y` #set_availability
	echo hw_ncores=$((sockets * corespersock)) #set_hw
	echo hw_model=$model #set_hw
	echo hw_scache=$l2cache #set_hw
	echo fw_bios=$bios
	#'
elif [ "$1" = "jbb" ]; then
	#printf "GENERATING SPECJBB2015 configuration...\n"
	#
	# SAMPLE SPECJBB2015-MultiJVM SUBMISSION TEMPLATE
	#

	# ----------------------------------------- Benchmark and test descriptions -------------------------------------------
	#
	echo "jbb2015.test.specLicense=LIC-XXXX-XXXX-XXXX"
	echo "jbb2015.test.date=`date`"
	echo "jbb2015.test.internalReference=http://$vendor/"
	echo "jbb2015.test.location=BENGALURU"
	echo "jbb2015.test.testSponsor=$vendor"
	echo "jbb2015.test.testedBy=$tester"
	echo "jbb2015.test.testedByName=$tester"
	echo "jbb2015.test.hwVendor=$vendor"
	echo "jbb2015.test.hwSystem=$vendor"
	# Enter latest availability dates for hw and sw when using multiple components
	echo "jbb2015.test.hwAvailability=$avail"
	echo "jbb2015.test.swAvailability=$avail"
	# ----------------------------------------- Overall SUT (System Under Test) descriptions --------------------------
	#
	# ----------------------------------------- Overall SUT (System Under Test) descriptions --------------------------
	#
	echo 	"jbb2015.test.aggregate.SUT.vendor=$vendor"
	echo 	"jbb2015.test.aggregate.SUT.vendor.url=http://www.$vendor.com"
	echo 	"jbb2015.test.aggregate.SUT.systemSource=Single Supplier"
	echo 	"jbb2015.test.aggregate.SUT.systemDesignation=Server Rack"
	echo 	"jbb2015.test.aggregate.SUT.totalSystems=1"
	echo 	"jbb2015.test.aggregate.SUT.allSUTSystemsIdentical= YES"
	echo 	"jbb2015.test.aggregate.SUT.totalNodes=$nodes"
	echo 	"jbb2015.test.aggregate.SUT.allNodesIndentical= YES"
	echo 	"jbb2015.test.aggregate.SUT.nodesPerSystem=$nodes"
	echo 	"jbb2015.test.aggregate.SUT.totalChips=$sockets"
	echo 	"jbb2015.test.aggregate.SUT.totalCores=$((corespersock * $sockets))"
	echo 	"jbb2015.test.aggregate.SUT.totalThreads=$ncpus"
	echo 	"jbb2015.test.aggregate.SUT.totalMemoryInGB=$mem_in_GB"
	echo 	"jbb2015.test.aggregate.SUT.totalOSImages=1"
	echo 	"jbb2015.test.aggregate.SUT.swEnvironment= Non-virtual"
	# ---------------------------------------------- SUT Product descriptions echo 	"-----------------------------------------------------
	#
	# Describe each JVM product using following format:
	#jbb2015.product.SUT.sw.jvm.<JVM label>.<param> = <value>
	# Sample configuration for "jvm_1" JVM
	echo 	"jbb2015.product.SUT.sw.jvm.jvm_1.name=$(echo `java -version`)"
	echo 	"jbb2015.product.SUT.sw.jvm.jvm_1.version=$(echo `java -version`)"
	echo 	"jbb2015.product.SUT.sw.jvm.jvm_1.vendor=$(echo `java -version`)"
	echo 	"jbb2015.product.SUT.sw.jvm.jvm_1.vendor.url=http://www.java.com"
	echo 	"jbb2015.product.SUT.sw.jvm.jvm_1.available=$(echo `java -version`)"
	echo 	"jbb2015.product.SUT.sw.jvm.jvm_1.bitness=$(echo `java -version`)"
	echo 	"jbb2015.product.SUT.sw.jvm.jvm_1.notes=note"
	# Describe each OS product using following format:
	#jbb2015.product.SUT.sw.os.<OS label>.<param> = <value>
	#Sample configuration for "os_1" OS
	echo 	"jbb2015.product.SUT.sw.os.os_1.name=$osn"
	echo 	"jbb2015.product.SUT.sw.os.os_1.version=$osv"
	echo 	"jbb2015.product.SUT.sw.os.os_1.bitness=$osa"
	echo 	"jbb2015.product.SUT.sw.os.os_1.available=$avail"
	echo 	"jbb2015.product.SUT.sw.os.os_1.vendor=$osvn"
	echo 	"jbb2015.product.SUT.sw.os.os_1.vendor.url=http://${osnv}.com/"
	echo 	"jbb2015.product.SUT.sw.os.os_1.notes=None"
	#jbb2015.product.SUT.sw.other.<OTHER label>.<param> = <value>
	# Sample configuration for "other_1" other
	echo 	"jbb2015.product.SUT.sw.other.other_1.name=$osn"
	echo 	"jbb2015.product.SUT.sw.other.other_1.vendor=$osn"
	echo 	"jbb2015.product.SUT.sw.other.other_1.vendor.url=http://$osn.com/"
	echo 	"jbb2015.product.SUT.sw.other.other_1.version=$osv"
	echo 	"jbb2015.product.SUT.sw.other.other_1.available=$avail"
	echo 	"jbb2015.product.SUT.sw.other.other_1.bitness=$osa"
	echo 	"jbb2015.product.SUT.sw.other.other_1.notes=None"

	# Describe each HW product using following format:
	#jbb2015.product.SUT.hw.system.<SYSTEM label>.<param> = <value>
	# Sample configuration for "hw_1"

	echo 	"jbb2015.product.SUT.hw.system.hw_1.name=$vendor"
	echo 	"jbb2015.product.SUT.hw.system.hw_1.model=$model"
	echo 	"jbb2015.product.SUT.hw.system.hw_1.formFactor=HW_FORM_FACTOR"
	echo 	"jbb2015.product.SUT.hw.system.hw_1.cpuName=$cpuname"
	echo 	"jbb2015.product.SUT.hw.system.hw_1.cpuCharacteristics=CPU_CHARACTERISTICS "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.nSystems=1 "
	echo 	"# all details below are per system basis "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.nodesPerSystem=$nodes"
	echo 	"jbb2015.product.SUT.hw.system.hw_1.chipsPerSystem=$sockets"
	echo 	"jbb2015.product.SUT.hw.system.hw_1.coresPerSystem=$((corespersock*sockets))"
	echo 	"jbb2015.product.SUT.hw.system.hw_1.coresPerChip=$corespersock "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.threadsPerSystem=$ncpus "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.threadsPerCore=$thpercore "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.version=$model "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.available=$avail "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.cpuFrequency=$mhz "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.primaryCache=$l1cache "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.secondaryCache=$l2cache "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.tertiaryCache=$l3cache "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.otherCache=None "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.disk=$disk "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.file_system=HW_FILE_SYSTEM "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.memoryInGB=$mem_in_GB "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.memoryDIMMS=$(if [ "$mem_dimms" != "0" ];then echo $mem_dimms;else echo "";fi) "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.memoryDetails=HW_MEM_DETAILS  "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.networkInterface=$network "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.psuInstalled=HW_PSU_DETAILS "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.other=HW_OTHER_DETAILS "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.sharedEnclosure=None "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.sharedDescription=None "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.sharedComment=None "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.vendor=$vendor "
	echo 	"jbb2015.product.SUT.hw.system.hw_1.vendor.url=http://${vendor}.com/"
	echo 	"jbb2015.product.SUT.hw.system.hw_1.notes=None"
	echo 	"#jbb2015.product.SUT.hw.other.<OTHER label>.<param> = <value> "
	echo 	"# Sample configuration for \"network_1\" other "
	echo 	"jbb2015.product.SUT.hw.other.network_1.name=NW_DETAILS "
	echo 	"jbb2015.product.SUT.hw.other.network_1.vendor=NW_DETAILS"
	echo 	"jbb2015.product.SUT.hw.other.network_1.vendor.url=http://NW_DETAILS.com/ "
	echo 	"jbb2015.product.SUT.hw.other.network_1.version=NW_VERSION "
	echo 	"jbb2015.product.SUT.hw.other.network_1.available=$avail "
	echo 	"jbb2015.product.SUT.hw.other.network_1.bitness=n/a "
	echo 	"jbb2015.product.SUT.hw.other.network_1.notes=None"
fi


