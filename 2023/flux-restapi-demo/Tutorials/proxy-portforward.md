1.   In a new terminal from your local machine, run this:
	
     ssh -ND 9999 <your-OUN>@lgw2-pub  
     
     Enable SOCKS5 Proxy in Firefox ( I go by FIrefox right now but it should be the same across all popular browsers) by going to Settings -> in "Generals" tab, scroll all the way down to find Network Settings -> click on "Settings" in that section -> choose "Manual Proxy configurations" -> choose SOCKS v5 and type "localhost" in SOCKS Host field and 9999 ( or another port number prefereably higher like above 20000) in Port field. Make sure to check "Proxy DNS when using SOCKS v5" so the server can forward all DNS resolving to the hyperion client (lgw2-pub).


Refer to proxy.png in the Tutorials directory for a visual.


**NOTE** put \*.llnl.gov so that anything related to LLNL can be forwarded back to your local machine's route traffic since you cannot access anything Lab-related on the hyperion.


2.   Inside your cluster, run this : 
     ssh -L 0.0.0.0:20000:<VM-hostname>:5000 root@<your-mgmt-node>




3.  On your browser, type http://<your-cluster-name>:20000


**EXPLANATION** 

1.  The first step implies that you are using the hyperion as a proxy, which is the middleman, such that all internet traffic on your Firefox browser ( or any other browser if you don't like using Firefox) goes through the hyperion ( google what is my ip and you'll see the current IP address is that of the hyperion)

2.  Second step is route 0.0.0.0 (instead of localhost aka 127.0.0.1) to the port 20000, which means any package going through port 20000 in your cluster goes to port 5000 on the <VM-hostname>.

    This is example catering to setting up Flux RestAPI server and seeing it on the local machine. "5000" is the port you set in the argument when you launch the uvicorn app. Of course you can change it to any available/open ports 
