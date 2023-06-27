FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y software-properties-common gcc 
RUN apt-get update 
RUN apt-get install -y python3.10 
RUN apt-get install -y python3-distutils 
RUN apt-get install -y python3-pip 
RUN apt-get install -y python3-apt
RUN apt-get install -y libgl1-mesa-glx
RUN ldconfig

COPY ./* /app/
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]