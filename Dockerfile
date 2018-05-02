FROM gcr.io/tensorflow/tensorflow:latest

ENV TF_MODELS_DIR=/tensorflow-models
ENV TF_MODELS_RESEARCH_DIR=${TF_MODELS_DIR}/research

# Make sure you grab the latest version
RUN curl -OL https://github.com/google/protobuf/releases/download/v3.2.0/protoc-3.2.0-linux-x86_64.zip

# Unzip
RUN unzip protoc-3.2.0-linux-x86_64.zip -d protoc3

# Move protoc to /usr/local/bin/
RUN mv protoc3/bin/* /usr/local/bin/

# Move protoc3/include to /usr/local/include/
RUN mv protoc3/include/* /usr/local/include/

RUN apt-get update \
      && apt-get install -y git python-tk
RUN pip install lxml
RUN git clone https://github.com/tensorflow/models ${TF_MODELS_DIR}

# Packaging the object detection codes.
RUN cd ${TF_MODELS_RESEARCH_DIR} \
    && protoc object_detection/protos/*.proto --python_out=. \
    && python setup.py sdist \
    && (cd slim && python setup.py sdist)

# Exporting the object detection binaries.
ENV PYTHONPATH=$PYTHONPATH:${TF_MODELS_RESEARCH_DIR}:${TF_MODELS_RESEARCH_DIR}/slim

# Cleaning build deps.
RUN apt-get remove -y protobuf-compiler git \
      && apt-get autoremove -y

WORKDIR /workspace