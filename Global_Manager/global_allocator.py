##############################################################
# VM_list[*][0] = VM_name
# VM_list[*][1] = VM_LLC_MPKI
# PM_list[*][0] = Server_name
# PM_list[*][1] = Server_IP
# PM_list[*][2] = Server_Dynamic_Computing_Capability_file
# PM_list[*][3] = Server_Dynamic_Computing_Capability
##############################################################
import os
import time

#Make VM List
VM = open("VM_list","r")
lines = VM.readlines()
VM_list_size = 0
VM_list = [[0]*2] * len(lines)

for line in lines:
	VM_list[VM_list_size] = line.split(' ')
	os.system("sh VM_start.sh "+str(VM_list[VM_list_size][0]))
	VM_list[VM_list_size][1] = float(VM_list[VM_list_size][1])
	VM_list_size = VM_list_size+1
VM.close()

#Make PM List
PM=open("PM_list","r")
lines = PM.readlines()
PM_list_size = 0
PM_list = [[0]*4] * len(lines)

for line in lines:
	PM_list[PM_list_size] = line.split(' ')
	PM_list[PM_list_size][2] = "cat " + PM_list[PM_list_size][2][0:-1]
	PM_list_size = PM_list_size+1
PM.close()

#VM List Sorting in an ascending order of LLC MPKI
VM_list.sort(key=lambda x:x[1])

#Update ambient-aware dynamic computing capability of PMs
for j in range(PM_list_size):
                PM_list[j].append(float(os.popen('sshpass -psmrlsmrl ssh '+str(PM_list[j][0])+'@'+str(PM_list[j][1])+' '+ str(PM_list[j][2])).read()))

#Mapping VMs to PMs
for i in range(VM_list_size):
	time.sleep(1)
	for j in range(PM_list_size):
		PM_list[j][3] = (float(os.popen('sshpass -psmrlsmrl ssh '+str(PM_list[j][0])+'@'+str(PM_list[j][1])+' '+ str(PM_list[j][2])).read()))
	PM_list.sort(key=lambda x:-x[3])

	#for Computation-intensive VM
	if VM_list[0][1] < 1.0:
		os.system("virsh migrate --verbose "+str(VM_list[0][0])+" qemu+ssh://"+str(PM_list[0][0])+"@"+str(PM_list[0][1])+"/system --live --migrateuri tcp://"+str(PM_list[0][1])+":49152")
		print(VM_list[0][0]+" is allocated to "+PM_list[0][0])
		VM_list = VM_list[1:VM_list_size]
	#for Memory-intensive VM
	else:
		for j in range(VM_list_size-i):
			os.system("virsh migrate --verbose "+str(VM_list[j][0])+" qemu+ssh://"+str(PM_list[j][0])+"@"+str(PM_list[j][1])+"/system --live --migrateuri tcp://"+str(PM_list[j][1])+":49152")
			print(VM_list[j][0]+" is allocated to "+PM_list[j][0])

