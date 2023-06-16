FROM ghcr.io/luxonis/robothub-app-v2:2023.137.1758-regular

RUN apt-get update && apt-get install -y ffmpeg git 
RUN pip3 uninstall -y depthai_sdk robothub_oak 
RUN pip3 install -U robothub_depthai 
RUN pip3 install -U git+https://github.com/luxonis/depthai.git@fix/race_cond#subdirectory=depthai_sdk
RUN pip3 install -U git+https://github.com/luxonis/robothub-oak.git@develop