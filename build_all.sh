docker pull quay.io/pypa/manylinux_2_24_x86_64
docker build -f Dockerfile.debian . -t livarot
docker run -it --name livarot livarot
docker cp livarot:/livarot/wheelhouse .
 