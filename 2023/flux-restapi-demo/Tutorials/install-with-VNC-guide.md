The flux documentation shows users how to run flux within a python environment. This method however runs a second instance of flux under the one we already have running on our VM cluster, which is only able to detect the node that it is being hosted on, which is why we have to run it right on the cluster.

**Installations:**
VNC Viewer on your physical machines.

On your management node as root user:

* xterm
* firefox
* xauth

On your VM cluster:

* Python3.9+ (preferably Python3.11 or whichever is the latest)

**Flux:**
You should already have flux installed on your VM. If not, follow *Installation of Flux* guide.

1. Clone the Flux Restful API [repo](https://github.com/flux-framework/flux-restful-api)

2. cd into flux-restful-api (`cd flux-restful-api`) repo on your machine

3. Create a python environment, start the environment and install the dependencies

```
python3 -m venv env ## This creates the python environment##
source env/bin/activate   ##Starts the environment##
pip install -r requirements.txt
```

4. cd back into root (`cd /`) and create a temporary file fluxenv-vars and make it look like the following:
```
export FLUX_CONNECTOR_PATH=/usr/local/lib/flux/connectors
export FLUX_MODULE_PATH=/usr/local/lib/flux/modules
export FLUX_EXEC_PATH=/usr/local/libexec/flux/cmd
export FLUX_PMI_LIBRARY_PATH=/usr/local/lib/flux/libpmi.so
export FLUX_URI=local:///run/flux/local
export PYTHONPATH=/usr/local/lib/flux/python3.6
export FLUX_NUMBER_NODES=5 #This is the total number of nodes you have. Including the management node.
```

5. Run the following commands:
```
cd flux-restful-api    ## Just make sure you are back in the directory
uvicorn app.main:app --host=0.0.0.0 --port=5000 --workers=2 ## This starts the api environment locally
```
If the last line says `Application startup complete`, you're good to go!

**Viewing and using the API:**

Notice if you try to go to http://0.0.0.0:5000 on Firefox (or any browser) on your physical machine, it won't connect. This happens becaus eyour physical machine is not on the LAN that your cluster and VMs are on. This is where VNC viewer is helpful.

Connecting to the API locally
1. Log into VNC viewer
2. Open up a terminal and type `xterm` in the command line, use the new window that popped up.
3. Sign into `lgw2-pub` (or provided `lgw` server for you)
4. Log into your cluster as a user (`ssh -X xenoni` for example)
5. Run the command `firefox --no-remote` (a Firefox window should pop up)
6. Type the URL `http://your-vm-name:port-launched-from-uvicorn` (example `http://HPC1:5000` because my VM name is HPC1 and I launch the API server through port 50000 from HPC1)

You should see the webpage.

Make sure it can see all the nodes by going to API -> /v1/nodes -> `Try it out` button -> `Execute` button

Under `Response Body` you should see all of the nodes you plan to run with `flux`
