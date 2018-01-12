import tensorflow as tf
import os

from object_detection.utils import dataset_util
from PIL import Image
from lxml import etree

flags = tf.app.flags
flags.DEFINE_string('output_path', './data/digicode.record', 'Path to output TFRecord')
flags.DEFINE_string('images_path', './images', 'Images directory')
flags.DEFINE_string('annotations_path', './annotations', 'Images annotations directory')
FLAGS = flags.FLAGS

def create_tf_example(filepath):
  img = Image.open(filepath)
  basepath, filename = os.path.split(filepath)

  height = img.height # Image height
  width = img.width # Image width
  encoded_image_data = img.tobytes() # Encoded image bytes
  image_format = b'jpg' if filename.lower().endswith(('.jpeg', '.jpg')) else b'png' # b'jpeg' or b'png'

  label, xmin, xmax, ymin, ymax = read_example_coordinates(filename)

  xmins = [xmin] # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = [xmax] # List of normalized right x coordinates in bounding box
             # (1 per box)
  ymins = [ymin] # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = [ymax] # List of normalized bottom y coordinates in bounding box
             # (1 per box)
  classes_text = [label] # List of string class name of bounding box (1 per box)
  classes = [1] # List of integer class id of bounding box (1 per box)

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))

  print filename
  print height
  print width
  print image_format
  print classes_text
  print classes

  img.close()

  return tf_example

def read_example_coordinates(filename):
    file, extension = os.path.splitext(filename)
    tree = etree.parse(os.path.join(FLAGS.annotations_path, file + '.xml'))

    label = tree.xpath('/annotation/object/name')[0].text
    xmin = tree.xpath('/annotation/object/bndbox/xmin')[0].text
    xmax = tree.xpath('/annotation/object/bndbox/xmax')[0].text
    ymin = tree.xpath('/annotation/object/bndbox/ymin')[0].text
    ymax = tree.xpath('/annotation/object/bndbox/ymax')[0].text

    print '\t' + label + ': ' + xmin + '-' + xmax + 'x' + ymin + '-' + ymax

    return label, int(xmin), int(xmax), int(ymin), int(ymax)

def main(_):
  writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

  for dirname, dirnames, filenames in os.walk(FLAGS.images_path):

    # print path to all filenames.
    for filename in filenames:
      if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filepath = os.path.join(dirname, filename)
        print filepath
        tf_example = create_tf_example(filepath)
        writer.write(tf_example.SerializeToString())

  writer.close()


if __name__ == '__main__':
  tf.app.run()