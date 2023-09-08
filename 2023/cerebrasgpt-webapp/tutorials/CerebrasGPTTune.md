# How to Tune CerebrasGPT

## Log into GPU and make sure you are at the latest kernel version and install packages (some may already have been installed), disable the default GPU driver, then reboot
```
dnf update -y
  
dnf install -y kernel-devel kernel-headers wget
  
dnf install -y epel-release
  
dnf install -y tar bzip2 make automake gcc gcc-c++ pciutils elfutils-libelf-devel libglvnd-devel kernel kernel-core kernel-modules dkms xorg-x11-server-Xorg ocl-icd opencl-filesystem egl-wayland vulkan-loader pango-devel cairo-devel fontconfig-devel gtk3-devel libva-vdpau-driver gdk-pixbuf2-devel gtk2-devel
  
grub2-editenv - set "$(grub2-editenv - list | grep kernelopts) nouveau.modeset=0"
 
reboot
```
## Download and install driver
```
wget https://us.download.nvidia.com/tesla/535.54.03/NVIDIA-Linux-x86_64-535.54.03.run
 
sh NVIDIA-Linux-x86_64-535.54.03.run
 
# answers provided
# Register with DKMS - yes
# 32 bit compatability - yes  
```
## Verify driver sees GPU hardware
```
nvidia-smi
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.54.03              Driver Version: 535.54.03    CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA A100 80GB PCIe          Off | 00000000:65:00.0 Off |                    0 |
| N/A   42C    P0              67W / 300W |      4MiB / 81920MiB |      0%      Default |
|                                         |                      |             Disabled |
+-----------------------------------------+----------------------+----------------------+
|   1  NVIDIA A100 80GB PCIe          Off | 00000000:CA:00.0 Off |                    0 |
| N/A   40C    P0              66W / 300W |      4MiB / 81920MiB |     24%      Default |
|                                         |                      |             Disabled |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+

```
## Install CUDA and setup environment and gcc Nvidia off load compiler
```
dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo
 
dnf install -y cuda-driver-devel-11-2 cuda-toolkit-11-2  cuda-toolkit-10-2
 
dnf -y install gcc-offload-nvptx
 
cat > /etc/profile.d/cuda.sh << EOF
export PATH=$PATH:/usr/local/cuda-11.2/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-11.2/lib64
EOF
```
## Create a user
```
useradd <user>
passwd <user>
```
## As your USER
```
cp -r /usr/local/cuda/samples/ .
 
cd samples/0_Simple/matrixMul
 
make
 
./matrixMul
 
OUTPUT:
[Matrix Multiply Using CUDA] - Starting...
GPU Device 0: "Kepler" with compute capability 3.5
 
MatrixA(320,320), MatrixB(640,320)
Computing result using CUDA Kernel...
done
Performance= 289.21 GFlop/s, Time= 0.453 msec, Size= 131072000 Ops, WorkgroupSize= 1024 threads/block
Checking computed result for correctness: Result = PASS
 
NOTE: The CUDA Samples are not meant for performancemeasurements. Results may vary when GPU Boost is enabled.
```
## **As USER in your venv *** If having problems with pip, xturing, or pika, go to Debugging
```
cd
 
wget https://d33tr4pxdm6e2j.cloudfront.net/public_content/tutorials/datasets/alpaca_data.zip
 
unzip alpaca_data.zip
 
python3 -m venv cerebrasgpt-venv
 
source cerebrasgpt-venv/bin/activate
 
pip install --upgrade pip
 
pip install xturing accelerate
 
pip install pika
```
## Create a python file tuneCerebrasGPT.py to tune and save the CerebrasGPT model
```
# we used this website to help train the model: https://www.listendata.com/2023/03/open-source-chatgpt-models-step-by-step.html
from xturing.datasets.instruction_dataset import InstructionDataset
from xturing.models.base import BaseModel

instruction_dataset = InstructionDataset("./alpaca_data")
# Initializes the model
model = BaseModel.create("cerebras_lora_int8")

model.finetune(dataset=instruction_dataset)

output = model.generate(texts=["What's the most interesting thing Thomas Jefferson did?"])
print("Generated output by the model: {}".format(output))

# Save Model
model.save("./cerebras-1.3B-alpaca-tuned")
```

## Tune model
```
python3 tuneCerebrasGPT.py
```
* It was 3 epochs ~ 25 minutes on NVIDIA A100 GPU
## When you want to use it after being trained, create a useCerebrasGPT.py to load the model and ask it questions

```
from xturing.datasets.instruction_dataset import InstructionDataset
from xturing.models.base import BaseModel

# Load a fine-tuned model
finetuned_model = BaseModel.load("./cerebras-1.3B-alpaca-tuned")

output = finetuned_model.generate(texts=["What's for dinner?"])
print("Generated output by the model: {}".format(output))
```

## Use model

```
python3 useCerebrasGPT.py
```

## Cited Works

CerebrasGPT: https://www.listendata.com/2023/03/open-source-chatgpt-models-step-by-step.html#cerebrasgpt

