import tensorflow as tf

for example in tf.python_io.tf_record_iterator("data/digicode.record"):
    result = tf.train.Example.FromString(example)