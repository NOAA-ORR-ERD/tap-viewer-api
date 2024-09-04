# TAP Viewer Docker configuration
#

FROM registry.orr.noaa.gov/erd/centos-conda/ubuntu/ubuntuforge-python3.12
#FROM registry.orr.noaa.gov/erd/centos-conda/centos7-python3

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install git -y

COPY ./ /tap-viewer/
RUN cd tap-viewer/TAP-Viewer-API && conda install --file conda_requirements.txt
RUN cd tap-viewer/TAP-Viewer-API && pip install -e ./

RUN mkdir /config
RUN cp /tap-viewer/TAP-Viewer-API/config-deploy.ini /config/config.ini
RUN ln -s /config/config.ini /tap-viewer/TAP-Viewer-API/config.ini

EXPOSE 9900
VOLUME /config
ENTRYPOINT ["/tap-viewer/docker_start.sh"] 