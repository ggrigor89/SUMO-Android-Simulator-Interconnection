# SUMO Android Simulator interconnection
Repository with all elements to facilitate an interconnection between a SUMO simulation and an Android Application

Programming languages: Python, Kotlin

The repository includes all the elements for facilitating an interconnection among:
  1) A python script initiating and running a SUMO simulation (sumo_simulation) (CLIENT)
  2) A python simulator client (imported in sumo_simulation for facilitating the inteconnection beetween the pypthon server and the SUMO simulation)
  3) An Android application exchanging information with the SUMO simulation (CLIENT)
  4) A python server handling all commmunication traffic between the SUMO simulation and the Android application (SERVER)

The interconnection is facilitated using LogMeIn Hamachi. LogMeIn Hamachi is a hosted VPN service that lets you securely extend LAN-like networks
to distributed teams and mobile workers.
https://www.vpn.net/

All parties exchange information using .json packages. Packages are exchanged over TCP/IP Sockets.

The following image presents the interconnection among all elements in the example of a bicycle simulator, where SUMO is used for modelling surrounding traffic.

https://github.com/ggrigor89/SUMO_Android_Simulator_interconnection/blob/main/Interconnection_graph.png
