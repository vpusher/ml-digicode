# Digicode ML

## Create TF Record

docker-compose up -d
docker exec -it digicode-ml_tensorflow_1 bash
python convert.py
docker-compose down

## Training 

https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_locally.md

>  From the /tensorflow-models/research/ directory:

```
python object_detection/train.py \
    --logtostderr \
    --pipeline_config_path=/workspace/models/model/ssd_inception_v2_coco.config \
    --train_dir=/workspace/models/model/train
```

```
python object_detection/train.py \
    --logtostderr \
    --pipeline_config_path=/workspace/models/model/ssd_mobilenet_v1_coco.config \
    --train_dir=/workspace/models/model/train
```

# Evaluation

Evaluation is run as a separate job.
The eval job will periodically poll the train directory for new checkpoints and evaluate them on a test dataset.
The job can be run using the following command:

> From the tensorflow/models/research/ directory:

```
python object_detection/eval.py \
    --logtostderr \
    --pipeline_config_path=/workspace/models/model/ssd_inception_v2_coco.config \
    --checkpoint_dir=/workspace/models/model/train \
    --eval_dir=/workspace/models/model/eval
```

```
python object_detection/eval.py \
    --logtostderr \
    --pipeline_config_path=/workspace/models/model/ssd_mobilenet_v1_coco.config \
    --checkpoint_dir=/workspace/models/model/train \
    --eval_dir=/workspace/models/model/eval
```

# Tensorboard

```
tensorboard --logdir=/workspace/models/model/train
```

# Debug

> Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA

export TF_CPP_MIN_LOG_LEVEL=2

> Log stderr

export GLOG_logtostderr=1