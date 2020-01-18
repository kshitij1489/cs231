from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_data = X.shape[0]
    num_class = W.shape[1]
    
    for i in range(num_data):
        correct_class = y[i]
        score = X[i, :].dot(W) # 1xC
        score = np.exp(score - np.max(score)) # 1xC
        normalizer = np.sum(score)

        for j in range(num_class):
            sf_score = score[j]/ normalizer
            dW[:,j] += (X[i, :].T)*sf_score
        dW[:,correct_class] -= X[i, :].T

        loss += -np.log(score[correct_class]/ normalizer)
    
    # Normalize
    loss /= num_data
    dW /= num_data
    
    # Regularization
    loss += reg * np.sum(W * W)
    dW += (2*reg*W)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_data = X.shape[0]
    num_class = W.shape[1]
    
    score = X.dot(W) # NxC
    exp_scores = np.exp(score - np.reshape(np.amax(score, axis=1), (-1, 1))) # NxC
    
    sf_scores = exp_scores / np.reshape(np.sum(exp_scores, axis=1), (-1, 1))
    loss = np.sum(-np.log(sf_scores[np.arange(num_data), y]))
    
    dW = X.T.dot(sf_scores) # DxC
    data_class_table = np.zeros_like(sf_scores) # NxC
    data_class_table[np.arange(num_data), y] = 1
    dW -= X.T.dot(data_class_table)
    
    # Normalize
    loss /= num_data
    dW /= num_data
    
    # Regularization
    loss += reg * np.sum(W * W)
    dW += (2*reg*W)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
