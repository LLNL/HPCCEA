**Prerequisites:**

  

* Python 3.9+

* pip 21+

* Having finished the tutorial for Installation of Flux **(VERY IMPORTANT TO HAVE THIS DONE CORRECTLY)**

* SSH tunnel so you can have local port forwarded and displayed on your local machine's browser after deploying the uvicorn webserver

* Would recommend installing VSCode and its Remote server extension to launch the server there since it will save your time from manually setting up SSH tunnel

* Or do this on VNC

* Or if you want to be fancy, follow guide to set up on SOCKS5

  

**Steps:**

  

1. Create Python environment

		python3.11 -m venv env 
		source env/bin/activate

2. Start Flux so you can get the environment variable under the running instance

		start flux

3. Export Flux environment variables so Python can import flux environment variables. 
	Put the following commands in a file for convenience

		$ vi fluxenv-vars
		#Paste these variables
		export FLUX_CONNECTOR_PATH=/usr/local/lib/flux/connectors
		export FLUX_MODULE_PATH=/usr/local/lib/flux/modules
		export FLUX_EXEC_PATH=/usr/local/libexec/flux/cmd
		export FLUX_PMI_LIBRARY_PATH=/usr/local/lib/flux/libpmi.so
		export FLUX_URI=local:///run/flux/local
		export PYTHONPATH=/usr/local/lib/flux/python3.6
		export FLUX_NUMBER_NODES=3 #Put the number of nodes you have 
		export PATH=/home/env/bin:/home/your_user/.local/bin:/home/your_user/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
		#Change the parts in the line above where it says "your_user"
		
4. Type "exit" to exit Flux instance and activate the Flux environment variables

5. Clone the repository
		
		git clone git clone https://github.com/flux-framework/flux-restful-api

6. Install dependencies and flux-restful-client in "flux-restful-api" directory/repository

		cd flux-restful-api
		pip install -r requirements.txt

7. Run uvicorn web app for the API to work (inside flux-restful-api directory that you cloned in step 5)

		uvicorn app.main:app --host=0.0.0.0 --port=yyyy --workers=2
		

9. With the tunnel, open up a browser and type [http://0.0.0.0:yyyy](http://0.0.0.0/yyyy) (VSCode) [http://computer_hostname:yyyy](http://xenoni:yyyy) (SOCKS5 and VNC) Refer to proxy-portforward.md as its a guide to set up the visual webserver.
