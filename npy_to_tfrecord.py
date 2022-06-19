import argparse
import os

import numpy as np
import tensorflow as tf
from google.cloud import storage

parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", type=str, default="gs://homebrewnlp-eu/the-token-pile/",
                    help="Where to put tfrecords (in a bucket)")


def create_tfrecords(args):
    slash_idx = args.output_dir.find('/')
    bucket_name, output_dir = args.output_dir[:slash_idx], args.output_dir[slash_idx + 1:]
    bucket = storage.Client().get_bucket(bucket_name)
    filename = "data.tfrecord"
    joined = np.load("cache.npy")
    with tf.io.TFRecordWriter(filename) as writer:
        feature = {"text": tf.train.Feature(int64_list=tf.train.Int64List(value=joined.reshape(-1)))}
        tf_example = tf.train.Example(features=tf.train.Features(feature=feature))
        writer.write(tf_example.SerializeToString())

    bucket.blob(f'{output_dir}{filename}').upload_from_filename(filename)

    os.remove(filename)


def main():
    args = parser.parse_args()

    if not args.output_dir.endswith("/"):
        args.output_dir = args.output_dir + "/"
    if not args.output_dir.startswith("gs://"):
        print("Output dir isn't a cloud bucket. Exiting.")
        return
    args.output_dir = args.output_dir[len('gs://'):]
    create_tfrecords(args)


if __name__ == "__main__":
    main()
