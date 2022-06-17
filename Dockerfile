FROM ubuntu:bionic

WORKDIR "/flag_submitter"
COPY . .

RUN apt update \
 && apt -y install python3 python3-pip libev-dev libevdev2 \
 && python3 -m pip install -U pip \
 && pip3 install -r requirements.txt

#CMD ["python3","main.py"]
