import sys
sys.path.append('/home/ubuntu/anaconda2/lib/python2.7/site-packages/')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import h5py
import scipy
from PIL import Image
from scipy import ndimage
import re
import time
def load_dataset():
    train_dataset = h5py.File('datasets/train_catvnoncat.h5', "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:]) # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:]) # your train set labels
    test_dataset = h5py.File('datasets/test_catvnoncat.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:]) # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your test set labels
    classes = np.array(test_dataset["list_classes"][:]) # the list of classes
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes
train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = load_dataset()
train_set_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T  
test_set_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T  
train_set_x = train_set_x_flatten/255.
test_set_x = test_set_x_flatten/255.
var_lr = float(sys.argv[1])
var_num_iteration = int(sys.argv[2])
print_every = int(sys.argv[3])
variable_learning_rate = sys.argv[4]
cat_identification_number = sys.argv[5]
cat_file_name = sys.argv[6]
def sigmoid(z):
    s = 1/(1+np.exp(-z))
    return s
def initialize_with_zeros(dim):
    w = np.zeros((dim,1))
    b = 0
    return w, b
def propagate(w, b, X, Y):
    m = X.shape[1]
    A = sigmoid(np.dot(w.T,X)+ b )                                
    cost = -(1/m)*np.sum((Y*np.log(A)+(1-Y)*np.log(1-A)))    
    dw = 1/m*(np.dot(X,(A-Y).T))
    db = 1/m*np.sum((A-Y))
    cost = np.squeeze(cost)    
    grads = {"dw": dw,
             "db": db}
    return grads, cost
def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost = False, print_every = 100):
    costs = []
    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)
        dw = grads["dw"]
        db = grads["db"]
        w = w-learning_rate*dw
        b = b-learning_rate*db
        if i % print_every == 0:
            costs.append(cost)        
        if print_cost and ((i % print_every) == 0):
            print ("Cost after iteration %i: %f" %(i, cost))
    params = {"w": w,
              "b": b}
    grads = {"dw": dw,
             "db": db}
    return params, grads, costs

def predict(w, b, X):
    m = X.shape[1]
    Y_prediction = np.zeros((1,m))
    w = w.reshape(X.shape[0], 1)
    A = sigmoid(np.dot(w.T,X)+ b )
    for i in range(A.shape[1]):
        if (A[0,i] >= 0.5):
            Y_prediction[0,i]= 1
        else:
            Y_prediction[0,i] = 0
        pass
    return Y_prediction
def model(X_train, Y_train, X_test, Y_test, num_iterations = 2000, learning_rate = 0.5, print_cost = False, print_every  = 100):
    w, b = initialize_with_zeros(X_train.shape[0])
    parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iterations, learning_rate, print_cost, print_every)
    w = parameters["w"]
    b = parameters["b"]
    Y_prediction_test = predict(w, b, X_test)
    Y_prediction_train = predict(w, b, X_train) 
    d = {"costs": costs,
         "Y_prediction_test": Y_prediction_test, 
         "Y_prediction_train" : Y_prediction_train, 
         "w" : w, 
         "b" : b,
         "learning_rate" : learning_rate,
         "num_iterations": num_iterations}
    return d
d = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations = var_num_iteration, learning_rate = var_lr, print_cost = True, print_every = print_every)
costs = np.squeeze(d['costs'])
plt.plot(costs)
plt.ylabel('cost')
plt.xlabel('iterations (per hundreds)')
plt.title("Learning rate =" + str(d["learning_rate"]))
plt.savefig('public/'+ cat_identification_number+'.png')
# plt.show()
if(variable_learning_rate == "true"):
    learning_rates = [0.01, 0.001, 0.0001]
    models = {}
    for i in learning_rates:
        print ("learning rate is: " + str(i))
        models[str(i)] = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations = 1500, learning_rate = i, print_cost = False)
        print ('\n' + "-------------------------------------------------------" + '\n')
    for i in learning_rates:
        plt.plot(np.squeeze(models[str(i)]["costs"]), label= str(models[str(i)]["learning_rate"]))
    plt.ylabel('cost')
    plt.xlabel('iterations')
    legend = plt.legend(loc='upper center', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    plt.show()
my_image = cat_file_name 
fname = "public/" + my_image
image = np.array(ndimage.imread(fname, flatten=False))
num_px = train_set_x_orig.shape[1]
my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
my_predicted_image = predict(d["w"], d["b"], my_image)
f = open(cat_identification_number+ ".txt","w+")
f.write(classes[int(np.squeeze(my_predicted_image)),].decode("utf-8"))
f.close()
# plt.imshow(image)
print("y = " + str(np.squeeze(my_predicted_image)) + ", your algorithm predicts a \"" + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8") +  "\" picture.")

