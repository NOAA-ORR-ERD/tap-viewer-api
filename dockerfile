# TAP Viewer Docker configuration
#

FROM gitlab.orr.noaa.gov:5002/centos:latest
RUN yum update -y

COPY ./ /tap-viewer/
RUN cd tap-viewer/TAP-Viewer-API && conda install --file conda_requirements.txt
RUN cd tap-viewer/TAP-Viewer-API && python setup.py develop

RUN mkdir /config
RUN cp /tap-viewer/TAP-Viewer-API/config-example.ini /config/config.ini
RUN ln -s /config/config.ini /tap-viewer/config.ini

EXPOSE 9900
VOLUME /config
ENTRYPOINT ["/tap-viewer/docker_start.sh"] 