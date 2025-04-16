# specify the node base image with your desired version node:<version>
FROM python:3.11.12-bookworm

WORKDIR /usr/src/app

COPY . .

RUN ./PyQt6-6.9.0-cp39-abi3-manylinux_2_39_aarch64.whl

RUN pip install -r requirements.txt



CMD [ "python", "./BencH2O.py" ]