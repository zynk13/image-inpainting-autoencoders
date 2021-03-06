import sys
# import matplotlib.pyplot as plt 
import numpy as np 
import math 
import tensorflow as tf 
import dataset

#WEIGHT AND BIASES 
n1 = 16 
n2 = 32 
n3 = 64
n4 = 128
n5 = 256 
n6 = 512 
ksize = 5 

def run_training(): 
    # Basic model parameters as external flags.
    # flags = tf.app.flags
    # FLAGS = flags.FLAGS
    # flags.DEFINE_string('input_dir', 'input', 'Input Directory.')

    #LOAD PACKAGES 
    # print 'Path in the argument:', str(sys.argv[1])
    mnist = dataset.read_data_sets(one_hot=True) 
    trainimgs   = mnist.train.images 
    trainlabels = mnist.train.labels 
    testimgs    = mnist.test.images 
    testlabels  = mnist.test.labels 
    ntrain      = trainimgs.shape[0] 
    ntest       = testimgs.shape[0] 
    dim         = trainimgs.shape[1] 
    nout        = trainlabels.shape[1] 
    print ("Packages loaded") 
      
    weights = { 
    'ce1': tf.Variable(tf.random_normal([ksize, ksize, 1, n1],stddev=0.1)), 
    'ce2': tf.Variable(tf.random_normal([ksize, ksize, n1, n2],stddev=0.1)), 
    'ce3': tf.Variable(tf.random_normal([ksize, ksize, n2, n3],stddev=0.1)), 
    'ce4': tf.Variable(tf.random_normal([ksize, ksize, n3, n4],stddev=0.1)), 
    'ce5': tf.Variable(tf.random_normal([ksize, ksize, n4, n5],stddev=0.1)), 
    'ce6': tf.Variable(tf.random_normal([ksize, ksize, n5, n6],stddev=0.1)), 
    'cd6': tf.Variable(tf.random_normal([ksize, ksize, n5, n6],stddev=0.1)), 
    'cd5': tf.Variable(tf.random_normal([ksize, ksize, n4, n5],stddev=0.1)), 
    'cd4': tf.Variable(tf.random_normal([ksize, ksize, n3, n4],stddev=0.1)), 
    'cd3': tf.Variable(tf.random_normal([ksize, ksize, n2, n3],stddev=0.1)), 
    'cd2': tf.Variable(tf.random_normal([ksize, ksize, n1, n2],stddev=0.1)), 
    'cd1': tf.Variable(tf.random_normal([ksize, ksize, 1, n1],stddev=0.1)) 
    } 
    biases = { 
    'be1': tf.Variable(tf.random_normal([n1], stddev=0.1)), 
    'be2': tf.Variable(tf.random_normal([n2], stddev=0.1)), 
    'be3': tf.Variable(tf.random_normal([n3], stddev=0.1)), 
    'be4': tf.Variable(tf.random_normal([n4], stddev=0.1)), 
    'be5': tf.Variable(tf.random_normal([n5], stddev=0.1)), 
    'be6': tf.Variable(tf.random_normal([n6], stddev=0.1)), 
    'bd6': tf.Variable(tf.random_normal([n5], stddev=0.1)), 
    'bd5': tf.Variable(tf.random_normal([n4], stddev=0.1)), 
    'bd4': tf.Variable(tf.random_normal([n3], stddev=0.1)), 
    'bd3': tf.Variable(tf.random_normal([n2], stddev=0.1)), 
    'bd2': tf.Variable(tf.random_normal([n1], stddev=0.1)), 
    'bd1': tf.Variable(tf.random_normal([1],  stddev=0.1)) 
    } 
     
    print ("Network ready") 
     
    x = tf.placeholder(tf.float32, [None, dim]) 
    y = tf.placeholder(tf.float32, [None, dim]) 
    keepprob = tf.placeholder(tf.float32) 
    pred = cae(x, weights, biases, keepprob)
    #['out'] 
    cost = tf.reduce_sum(tf.square(cae(x, weights, biases, keepprob)- tf.reshape(y, shape=[-1, 256, 256, 1]))) 
    learning_rate = 0.001 
    optm = tf.train.AdamOptimizer(learning_rate).minimize(cost)
    init = tf.global_variables_initializer()
    print ("Functions ready")
     
    sess = tf.Session() 
    sess.run(init) 
    # mean_img = np.mean(mnist.train.images, axis=0) 
    mean_img = np.zeros((65536)) 
    # Fit all training data 
    batch_size = 128 
    n_epochs   = 251
     
    print("Start training..") 
    for epoch_i in range(n_epochs): 
        for batch_i in range(mnist.train.num_examples // batch_size): 
            batch_xs, _ = mnist.train.next_batch(batch_size) 
            trainbatch = np.array([img - mean_img for img in batch_xs]) 
            trainbatch_noisy = trainbatch
            # trainbatch_noisy = trainbatch + 0.3*np.random.randn( 
            #     trainbatch.shape[0], 65536) 
            # f, a = plt.subplots(2, 2, figsize=(10, 5))
            # a[0][0].imshow(np.reshape(trainbatch[0], (256, 256))) 
            # a[0][1].imshow(np.reshape(trainbatch[1], (256, 256))) 

            # a[1][0].imshow(np.reshape(trainbatch_noisy[0], (256, 256))) 
            # a[1][1].imshow(np.reshape(trainbatch_noisy[1], (256, 256))) 
            # f.show()
            # plt.draw()
            # plt.show()
            sess.run(optm, feed_dict={x: trainbatch_noisy, y: trainbatch, keepprob: 0.7}) 
        print ("[%02d/%02d] cost: %.4f" % (epoch_i, n_epochs, sess.run(cost, feed_dict={x: trainbatch, y: trainbatch, keepprob: 1.}))) 
        # if (epoch_i % 50) == 0: 
        #     n_examples = 5 
        #     test_xs, _ = mnist.test.next_batch(n_examples) 
        #     test_xs_noisy = test_xs
        #     # test_xs_noisy = test_xs + 0.3*np.random.randn(test_xs.shape[0], 65536) 
        #     recon = sess.run(pred, feed_dict={x: test_xs_noisy, keepprob: 1.}) 
        #     fig, axs = plt.subplots(2, n_examples, figsize=(15, 4)) 
        #     for example_i in range(n_examples): 
        #         axs[0][example_i].matshow(np.reshape( 
        #             test_xs_noisy[example_i, :], (256, 256)) 
        #             , cmap=plt.get_cmap('gray')) 
        #         axs[1][example_i].matshow(np.reshape( 
        #             np.reshape(recon[example_i, ...], (65536,)) 
        #             + mean_img, (256, 256)), cmap=plt.get_cmap('gray')) 
        #     plt.show()

def cae(_X, _W, _b, _keepprob): 
    _input_r = tf.reshape(_X, shape=[-1, 256, 256, 1]) 
    # Encoder 
    _ce1 = tf.nn.sigmoid(tf.add(tf.nn.conv2d(_input_r, _W['ce1'],strides=[1, 2, 2, 1],padding='SAME'),_b['be1'])) 
    _ce1 = tf.nn.dropout(_ce1, _keepprob) 
 
    _ce2 = tf.nn.sigmoid(tf.add(tf.nn.conv2d(_ce1, _W['ce2'],strides=[1, 2, 2, 1],padding='SAME'),_b['be2']))  
    _ce2 = tf.nn.dropout(_ce2, _keepprob) 
 
    _ce3 = tf.nn.sigmoid(tf.add(tf.nn.conv2d(_ce2, _W['ce3'],strides=[1, 2, 2, 1],padding='SAME'),_b['be3']))  
    _ce3 = tf.nn.dropout(_ce3, _keepprob) 

    _ce4 = tf.nn.sigmoid(tf.add(tf.nn.conv2d(_ce3, _W['ce4'],strides=[1, 2, 2, 1],padding='SAME'),_b['be4']))  
    _ce4 = tf.nn.dropout(_ce4, _keepprob) 

    _ce5 = tf.nn.sigmoid(tf.add(tf.nn.conv2d(_ce4, _W['ce5'],strides=[1, 2, 2, 1],padding='SAME'),_b['be5']))  
    _ce5 = tf.nn.dropout(_ce5, _keepprob) 

    _ce6 = tf.nn.sigmoid(tf.add(tf.nn.conv2d(_ce5, _W['ce6'],strides=[1, 2, 2, 1],padding='SAME'),_b['be6']))  
    _ce6 = tf.nn.dropout(_ce6, _keepprob) 
 
    # Decoder 
    _cd6 = tf.nn.sigmoid(tf.add(tf.nn.conv2d_transpose(_ce6, _W['cd6'],tf.stack([tf.shape(_X)[0], 8, 8, n5]),strides=[1, 2, 2, 1],padding='SAME'),_b['bd6']))  
    _cd6 = tf.nn.dropout(_cd6, _keepprob) 
    
    _cd5 = tf.nn.sigmoid(tf.add(tf.nn.conv2d_transpose(_cd6, _W['cd5'],tf.stack([tf.shape(_X)[0], 16, 16, n4]),strides=[1, 2, 2, 1],padding='SAME'),_b['bd5']))  
    _cd5 = tf.nn.dropout(_cd5, _keepprob) 
    
    _cd4 = tf.nn.sigmoid(tf.add(tf.nn.conv2d_transpose(_cd5, _W['cd4'],tf.stack([tf.shape(_X)[0], 32, 32, n3]),strides=[1, 2, 2, 1],padding='SAME'),_b['bd4']))  
    _cd4 = tf.nn.dropout(_cd4, _keepprob) 

    _cd3 = tf.nn.sigmoid(tf.add(tf.nn.conv2d_transpose(_cd4, _W['cd3'],tf.stack([tf.shape(_X)[0], 64, 64, n2]),strides=[1, 2, 2, 1],padding='SAME'),_b['bd3']))  
    _cd3 = tf.nn.dropout(_cd3, _keepprob) 
 
    _cd2 = tf.nn.sigmoid(tf.add(tf.nn.conv2d_transpose(_cd3, _W['cd2'],tf.stack([tf.shape(_X)[0], 128, 128, n1]),strides=[1, 2, 2, 1],padding='SAME'),_b['bd2']))  
    _cd2 = tf.nn.dropout(_cd2, _keepprob) 
 
    _cd1 = tf.nn.sigmoid(tf.add(tf.nn.conv2d_transpose(_cd2, _W['cd1'] ,tf.stack([tf.shape(_X)[0], 256, 256, 1]),strides=[1, 2, 2, 1],padding='SAME'),_b['bd1']))  
    _cd1 = tf.nn.dropout(_cd1, _keepprob) 
    _out = _cd1 
    return _out 
    
def main(_):
    run_training()

if __name__ == '__main__':
    tf.app.run()