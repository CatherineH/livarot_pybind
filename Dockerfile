FROM ubuntu:latest
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y wget gpg g++ python3 python3-dev pkg-config libboost1.71-dev libgsl-dev \
    libdouble-conversion-dev libglib2.0-dev libgtkmm-3.0-dev libgtest-dev python3-pytest  python3-venv python3-pip
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null && \
 echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ focal main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null && \
 apt-get update && apt-get install -y cmake=3.21.3-0kitware1ubuntu20.04.1
# TODO: step to checkout and build lib2geom
RUN apt install -y 
RUN mkdir /livarot
COPY . /livarot
WORKDIR "/livarot"
RUN cd lib2geom && cmake -DCMAKE_POSITION_INDEPENDENT_CODE=ON -S . -B docker-build
RUN cd lib2geom && cmake --build docker-build
RUN cd lib2geom && cmake --install docker-build
RUN cmake -S . -B docker-build
RUN cmake --build docker-build
RUN cp docker-build/*.so pylivarot
RUN pip3 install build
RUN python3 -m build
RUN pip3 install dist/*.whl
RUN pytest-3 test