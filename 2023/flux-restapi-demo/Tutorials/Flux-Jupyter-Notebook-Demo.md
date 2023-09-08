 Jupyter Notebook with Flux Client Demo
======================================
**Objective:**
Demonstrate a use case with Flux Python RestAPI in Jupyter Notebook environment

**General prerequisites:**

Carefully read the Installation of Flux guide! 

**Prerequisites on your local machine:**

*   **VSCode (for ease of editing and viewing Jupyter Notebook without hassles of manually setting up tunnels and stuff)**
    *   Download from [here](https://code.visualstudio.com/download) 

**Prerequisites on your Virtual Machine(Not needed for this tutorial as we have already provided a VM cluster for convenience.)**

*   **Python 3.9+ (preferably Python 3.11+)**
    *   Example: `dnf install python3.11`  
        optional: check for Python version using `python3 --version` inside your environment
*   **Separate Python environment for now**
    *   Refer to this guide for more details
*   **Flux RestAPI server is being hosted (preferably by "flux" user)**
*   **Setup a mounted shared directory and enable read-write-execute (**`chmod 777 /shared` **to enable read-write-execute permission for all users)  (refer to the Installation of Flux RestAPI guide to mount. Make sure to `mkdir /shared` in all VM nodes before restarting nfs-server and mounting the directory in worker VMs)**

**Setup Guide:**

1.  In VSCode, install **Remote** **SSH extension** for automatic tunneling (extension ID: **`ms-vscode-remote.remote-ssh`**)
    1.  Click on this icon on the left sidebar in VSCode to search on extension marketplace → and then search for the extension mentioned above
2.  Create another environment (run as root) using Python3.9+ and activate the environment in the Virtual Machine  
    1.  Example: **`python3.11 -m venv jn-env`** for an environment with Jupyter notebook
    2.  **`source jn-env/bin/activate`** to activate the environment
3. Go to directory that contains `flux-restful-api` to install requirements again from `requirement.txt `and `flux-restful-client` Python module.
```
pip install -r requirements.txt && pip install flux-restful-client
```
4.  Set up automatic tunnel to the VM through SSH extension
    1.  click on the "Remote Explorer" tab on the left sidebar.
    2.  click on "Configure" button
    3.  Select "/Users/<your-OUN>/.ssh/config" and add the following (for SSH tunnel forwarding) Make it look like this:

        Host HPC1 # change HPC1 to your management VM hostname
            HostName HPC1 # same here
            User root
            ProxyJump xenoni # change to your cluster name
        
        Host xenoni 
            HostName xenoni # change to your cluster name
            User root
            ProxyJump lgw2-pub 
        
    4.  in a VSCode terminal, ssh into root@xenoni and then ssh into HPC1
    5. Where HPC1 is the management VM, xenoni is the management node of the physical cluster (change it to your cluster name)  
        **NOTE: if you want to do this at home/outside of LLNL network, add oslic server (the password to SSH would be your RSA pin + token)    
    6.  click on this to refresh the content.
    7.  click on the icon with the plus sign _**NEXT TO THE VM THAT YOU HAVE FLUX ON (NOT YOUR PHYSICAL CLUSTER)**_ to start an SSH session in a new window
    8.  Enter the passwords in order: (optional) oslic, lgw2-pub, physical mgmt node, VM mgmt node
    9.  Now you can interactively read and write files by clicking on this → 
5.  In your management VM, if you haven't created a separate environment for Jupyter notebook, create it and install Jupyter metapackage: **`pip install jupyter`**
6.  Install Jupyter VSCode extensions with this ID: **`ms-toolsai.jupyter`**
7.  Launch Jupyter notebook by command **`jupyter notebook`**    
8.  You can create new Jupyter Notebook file (.ipynb) or upload existing ones straight from your local machine.
9. Inside a Jupyter Notebook file, run these codes:
```
from flux_restful_client.main import get_client

cli = get_client()

res = cli.submit(command='hostname', num_tasks=3, num_nodes=3)
if res and 'detail' not in res:
    jobid = res['id']
    sleep(2)
    print(json.dumps(cli.output(jobid), indent=4)) # this prints out the output of the command submitted to 3 different nodes
    print('\n\n CONGRATULATIONS! You have submitted your first job in Flux RestAPI in Python')

```

**Note: You can also run the demo code files in Demo Code directory using `python3 <demo-file>.py` on your management VM node in user**

**Run the API endpoint on your local machine in "flux" user (please refer to the Installation of Flux for this):** 
```
uvicorn app.main:app --host=0.0.0.0 --port=XXXXX

--port argument: Any port number you want to launch (preferably above 20000, but 5000 or 8080 is usually fine)
```
  

**Log into the VM cluster from your machine**

From lgw2: 
```
ssh root@xenoni
ssh e2
ssh HPC1 
su - your-user
```
  

To run flux on the VM, you have to be in the /home directory and run the python virtual environment.
```
cd /home/
source /path/to/fluxenv-vars # refer to install-with-VNC-guide.md
```

**Run your own API on your Machine:**  Originally from [here](https://lc.llnl.gov/confluence/pages/viewpage.action?pageId=753198163)

Create a terminal instance from your local machine and run this command:
```
ssh -ND 9999 <your-OUN>@lgw2-pub
```
  

Enter your Password for `lgw2`, it will  look like it is hanging but that is what we want.

  

Open up a Firefox Browser. Go to the settings and type "socks" in the search menu. Click on what pops up and have your connection settings like this:

**NOTE:** The port needs to be identical with the number you chose in the previous step.

In a new terminal window, log into the xenon cluster and run this command:
```
ssh -L 0.0.0.0:xxxxx:HPC1:yyyy root@xenoni
```
Replace the Xs and Ys with a port number of your own (check this guide to learn more). It can't be the same port as someone else since only one person can use a given port at a time in this scenario.

  

Log into your user on HPC1 and run the python environment like you did at the very beginning.

Once you are in the directory `flux-restful-api` run this command:
```
uvicorn app.main:app --host=0.0.0.0 --port=yyyy --workers=2
```

**NOTE:  you must use the same 4 digit number as you did in the previous command otherwise this won't work!**

At this point the server is setup, on the Firefox or any browser type in this url
`http://xenoni:xxxxx` (replace `xenoni` with your management cluster)

Again, this must use the same 5 digit port number as you did in the previous ssh command. You should see the API on your browser and you can submit jobs!

Make sure you submit tasks from the `/shared/` working directory (In the example above, Replace `/home/` with `/shared/`) . In your user on management VM node cd into`/shared`/ and look at the .py benchmark tests and submit them on the api similar to how it is shown in the picture. Change some of the options in the API and see what happens!
