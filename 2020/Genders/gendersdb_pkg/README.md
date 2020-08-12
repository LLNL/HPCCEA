# Centralized Genders Database

This tool is designed for LLNL system administrators to query node attribute values from a centralized database through a command line interface. 

Our database is based on the genders tool, which is an open source LLNL tool that stores information about node configurations.
The tool can be found [here](https://github.com/chaos/genders).

With the genders tool, information can only be queried locally with the *nodeattr* tool. We designed this database in order to allow engineers to access this information for multiple clusters from anywhere in the system. 

This was developed by Nisha Prabhakar and Meghan Utter during their summer 2020 HPC Cluster Enginnering Academy Internship. Mike Gilbert and Jason Shortino served as our mentors. 
