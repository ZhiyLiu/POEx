import numpy as np
import tensorflow as tf

def dense_nn(x, dims, dim_out, norm=True, name='dense_nn'):
    with tf.variable_scope(name, reuse=tf.AUTO_REUSE):
        for i, size in enumerate(dims):
            x = tf.layers.dense(x, size, name=f'd{i}')
            if norm:
                x = tf.contrib.layers.instance_norm(x)
            x = tf.nn.leaky_relu(x)
        x = tf.layers.dense(x, dim_out, name='d_out')

        return x

def convnet(x, dims, dim_out, name='convnet'):
    with tf.variable_scope(name, reuse=tf.AUTO_REUSE):
        for i, d in enumerate(dims):
            x = tf.layers.conv2d(x, d, 3, padding='same', name=f'c{i}_1')
            x = tf.contrib.layers.instance_norm(x)
            x = tf.nn.leaky_relu(x)
            x = tf.layers.conv2d(x, d, 3, padding='same', name=f'c{i}_2')
            x = tf.contrib.layers.instance_norm(x)
            x = tf.nn.leaky_relu(x)
            x = tf.layers.max_pooling2d(x, 2, 2)
        x = tf.layers.flatten(x)
        x = tf.layers.dense(x, dim_out, name='d1')
        x = tf.contrib.layers.instance_norm(x)
        x = tf.nn.leaky_relu(x)
        x = tf.layers.dense(x, dim_out, name='d2')

    return x

def peq_convnet(x, dims, dim_out, attention, name='peq_convnet'):
    B,N,H,W,C = tf.shape(x)[0], tf.shape(x)[1], *x.get_shape().as_list()[2:]
    with tf.variable_scope(name, reuse=tf.AUTO_REUSE):
        # downsample
        x = tf.reshape(x, [-1,H,W,C])
        for d in dims[:2]:
            x = tf.layers.conv2d(x, d, 3, strides=(1,1), padding='same')
            x = tf.contrib.layers.instance_norm(x)
            x = tf.nn.leaky_relu(x)
            x = tf.layers.conv2d(x, d, 3, strides=(2,2), padding='same')
            x = tf.contrib.layers.instance_norm(x)
            x = tf.nn.leaky_relu(x)
            H, W, C = H//2, W//2, d
        x = tf.reshape(x, [B,N,H,W,C])
        # attention across set dimension
        x = tf.reshape(tf.transpose(x, [0,2,3,1,4]), [B*H*W,N,C])
        rep = attention(x, x, x)
        x += rep
        x = tf.transpose(tf.reshape(x, [B,H,W,N,C]), [0,3,1,2,4])
        # downsample
        x = tf.reshape(x, [-1,H,W,C])
        for d in dims[2:]:
            x = tf.layers.conv2d(x, d, 3, strides=(1,1), padding='same')
            x = tf.contrib.layers.instance_norm(x)
            x = tf.nn.leaky_relu(x)
            x = tf.layers.conv2d(x, d, 3, strides=(2,2), padding='same')
            x = tf.contrib.layers.instance_norm(x)
            x = tf.nn.leaky_relu(x)
            H, W, C = H//2, W//2, d
        x = tf.layers.flatten(x)
        x = tf.layers.dense(x, dim_out)
        x = tf.contrib.layers.instance_norm(x)
        x = tf.nn.leaky_relu(x)
        x = tf.layers.dense(x, dim_out)
        x = tf.reshape(x, [B,N,dim_out])

    return x

def peq_resblock(x, dim, attention, name='peq_resnet'):
    B,N,H,W,C = tf.shape(x)[0], tf.shape(x)[1], *x.get_shape().as_list()[2:]
    with tf.variable_scope(name, reuse=tf.AUTO_REUSE):
        res = tf.reshape(tf.transpose(x, [0,2,3,1,4]), [B*H*W,N,C])
        res = attention(res, res, res)
        res = tf.transpose(tf.reshape(res, [B,H,W,N,C]), [0,3,1,2,4])
        res = tf.reshape(res, [B*N,H,W,C])
        res = tf.layers.conv2d(res, dim, 3, strides=(1,1), padding='same')
        res = tf.contrib.layers.instance_norm(res)
        res = tf.nn.leaky_relu(res)
        res = tf.layers.conv2d(res, dim, 3, strides=(1,1), padding='same')
        res = tf.contrib.layers.instance_norm(res)
        res = tf.reshape(res, [B,N,H,W,C])
        x += res
        x = tf.nn.leaky_relu(x)

    return x

