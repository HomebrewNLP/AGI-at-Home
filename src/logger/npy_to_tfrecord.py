import numpy as np
import tensorflow as tf


def main():
    filename = "../../data.tfrecord"
    joined = np.load("../../cache.npy")
    with tf.io.TFRecordWriter(filename) as writer:
        feature = {"text": tf.train.Feature(int64_list=tf.train.Int64List(value=joined.reshape(-1)))}
        tf_example = tf.train.Example(features=tf.train.Features(feature=feature))
        writer.write(tf_example.SerializeToString())


if __name__ == "__main__":
    main()
