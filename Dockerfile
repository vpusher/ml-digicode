FROM gcr.io/tensorflow/tensorflow:latest

ENV TF_MODELS_DIR=/tensorflow-models
ENV TF_MODELS_RESEARCH_DIR=${TF_MODELS_DIR}/research

RUN apt-get update \
      && apt-get install -y protobuf-compiler git python-tk
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