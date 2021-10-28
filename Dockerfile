FROM ubuntu:latest
RUN apt update && apt install -y wget gpg
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null && \
 echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ focal main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null && \
 apt-get update && apt-get install -y cmake=3.21.3-0kitware1ubuntu20.04.1
# TODO: step to checkout and build lib2geom
RUN DEBIAN_FRONTEND=noninteractive apt install -y g++ python3 python3-dev pkg-config libboost1.71-dev
RUN apt install -y libgsl-dev
RUN apt install -y libdouble-conversion-dev
RUN apt install -y libglib2.0-dev
RUN apt install -y libgtkmm-3.0-dev
RUN apt install -y libgtest-dev
RUN mkdir /livarot
COPY . /livarot
WORKDIR "/livarot"
RUN cd lib2geom && cmake -S . -B docker-build
RUN cd lib2geom && cmake --build docker-build
RUN cmake -S . -B docker-build
RUN cmake --build docker-build
RUN cp docker-build/*.so pylivarot
RUN python3 setup.py install
RUN pytest tests