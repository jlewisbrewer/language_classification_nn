from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

import seaborn as sn
import pandas as pd

print(tf.__version__)

def loadData(path):
    """
        Load data from a text file and split into real training, 
        spam training and test data sets
    """

    fp = open(path)
    data = np.loadtxt(fp, delimiter=", ", converters = {18: lambda s: convertLanguages(s)})
    fp.close()
    return data

def convertLanguages(string):
    languages = {"english": 0.0, "spanish": 1.0, "mandarin": 2.0, "japanese": 3.0, "arabic": 4.0, "turkish": 5.0}
    return languages[string.decode("utf-8")]

def getSets():
    data = loadData("inputs_3.csv")
    np.random.shuffle(data)
    data = np.array_split(data, 3)
    trainData = np.concatenate((data[0][:,:-1], data[1][:,:-1]))
    trainLabels = np.concatenate((data[0][:,-1], data[1][:,-1]))
    testData = data[2][:,:-1]
    testLabels = data[2][:,-1]
    return (trainData, trainLabels), (testData, testLabels)

def plotCM(cm):
    """
        Plots a confusion matrix and writes out to 'cm.png'
    """
    plt.figure(figsize = (10,10))
    sn.set(font_scale=1.4)
    sn.heatmap(cm, annot=True, annot_kws={"size":10})
    plt.suptitle("Confusion Matrix", fontsize=16)
    plt.savefig("cm.png")
    plt.close()


if __name__ == "__main__":
    (trainData, trainLabels), (testData, testLabels) = getSets()
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=trainData[0].shape),
        keras.layers.Dense(50, activation=tf.nn.softmax),
        keras.layers.Dense(6, activation=tf.nn.softmax)
    ])

    model.compile(optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"])

    model.fit(trainData, trainLabels, epochs=50)
    loss, acc = model.evaluate(testData, testLabels)
    pred = model.predict(testData)
    classes = ["english", "spanish", "mandarin", "japanese", "arabic", "turkish"]
    cm = confusion_matrix(testLabels, pred.argmax(axis=1))
    df = pd.DataFrame(data=cm, index=classes, columns=classes)
    plotCM(df)
