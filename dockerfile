# TAP Viewer Docker configuration
#

<<<<<<< HEAD
FROM registry.orr.noaa.gov/erd/environments/ubuntu/ubuntuforge-python3.11
=======
FROM registry.orr.noaa.gov/erd/environments/ubuntu/ubuntuforge-python3.13
>>>>>>> develop

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install git -y

COPY ./ /tap-viewer/
<<<<<<< HEAD
RUN cd tap-viewer/TAP-Viewer-API && conda install --file conda_requirements.txt -q
RUN cd tap-viewer/TAP-Viewer-API && pip install -e ./
=======
RUN cd tap-viewer/ && conda install --file conda_requirements.txt -q
RUN cd tap-viewer/ && pip install ./
>>>>>>> develop

RUN mkdir /config
RUN cp /tap-viewer/config-deploy.ini /config/config.ini
RUN ln -s /config/config.ini /tap-viewer/config.ini
RUN echo "working dir:" & pwd
RUN ls
RUN ls tap-viewer


EXPOSE 9900
VOLUME /config
ENTRYPOINT ["/tap-viewer/docker_start.sh"] 
