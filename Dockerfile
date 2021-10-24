FROM ubuntu:latest
RUN cd /opt && wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-linux-x86_64.sh && yes cmake-3.21.1-linux-x86_64.sh && ln -s /opt/cmake-3.31.1/bin/* /usr/local/bin
# TODO: step to checkout and build lib2geom
RUN cmake -S . -B build
RUN cmake --build build
RUN cp build/*.so pylivarot
RUN python3 setup.py install
RUN pytest tests