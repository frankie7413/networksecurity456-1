#### Removed old committed since i messed -__________________- 
Availeble VMs
---------------------------------------------------------------------
Endian FW - Network Switch VM
Ubun2 12.04, Ubuntu 12.04 & Ubuntu Desktop 12.04 - Ubuntu VMs
Windows XP/7 - Windows VMs
Kali Linux - Attack VM
Metaploitable - Target VM


---------------------------------------------------------------------
*Caution*
When changing account password within the xrdp session, use both 
vncpasswd and passwd commands to sync the new password.  Otherwise, 
ssh into the node and use only passwd command.


NFS Share
---------------------------------------------------------------------
Node1 is dedicated as NFS server.  All other nodes are considered 
NFS clients.


Environment Setup
---------------------------------------------------------------------
-Endian VM provides DHCP service for the internal network and also a
 gateway to the outside network (i.e. Internet).  Alternatively, 
 virtualbox's builtin dhcp service can be used using the vboxmanage 
 command. [https://www.virtualbox.org/manual/ch06.html]

 e.g.
 vboxmanage natnetwork add --netname intnet "192.168.1.0/24 --enable --dhcp on
 vboxmanage natnetwork start --netname intnet

-Each Ubuntu VM has shared directory access to the node's 
 host desktop directory which includes the nfs_share directory.


Other features
---------------------------------------------------------------------
Rebuilding a VM: First remove the current VM and import the 
	corresponding VM application under /home/VMs

Cloning a VM: right click on a VM and select clone.  Note that the VM 
	must be turned off.


Change Log
---------------------------------------------------------------------
10/9/15  Implemented a single server to be a multi-user system on
         opal.ecs.fullerton.edu and opal1.ecs.fullerton.edu
	 The system has 12 core with 50 GB RAM.

10/9/15  Modified /etc/xrdp/startwm and added the following line
	 to suppress keys that get repeated when pressed.

		xset r off
	
10/9/15  Users should now be able to restart xrdp service using sudo.
            
               	sudo service xrdp restart
		or
		sudo /etc/init.d/xrdp restart
