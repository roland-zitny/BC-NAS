import os
import os.path
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pylab as plt
from tensorflow.keras.models import load_model


def plot_confusion_matrix(cm, classes, normalize=False,title="Confusion Matrix", cmap=plt.cm.Blues):
    plt.imshow(cm,interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix without normalization")

    print(cm)

    thresh = cm.max() / 2.

    for i,j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j], horizontalalignment='center', color='white' if cm[i,j] > thresh else 'black')

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


if __name__ == '__main__':
    # https://www.youtube.com/watch?v=qFJeN9V1ZsI&t=1321s

    # Creating data
    train_labels = [0,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0]
    train_samples = [10,100,100,150,180,190,10,8,7,9,1,9,165,7,6,5,4,3,250,1,1,5,8,7,100,125,140,7,1,2]

    test_labels = [0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0]
    test_samples = [1,2,3,4,5,480,250,1,4,3,8,7,5,4,164,8,1,4,6,185,8,100,1,3,4]

    # Change it to numpy array
    train_labels = np.array(train_labels)
    train_samples = np.array(train_samples)

    test_labels = np.array(test_labels)
    test_samples = np.array(test_samples)

    # Shuffle data
    train_labels, train_samples = shuffle(train_labels, train_samples)

    test_labels, test_samples = shuffle(train_labels, train_samples)

    # Normalize or standardize data in range 0 to 1, to CNN be more efficient or quicker.
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_train_samples = scaler.fit_transform(train_samples.reshape(-1,1))
    scaled_test_samples = scaler.fit_transform(test_samples.reshape(-1,1))

    # MODEL
    # input_shape je 1. layer
    # vsetky dense su hidden layers
    # Activation je tiez layer nasledujuci po dense
    # DENSE je fully connected layer

    model = models.Sequential([
        layers.Dense(units=16, input_shape=(1,), activation='relu'),
        layers.Dense(units=32, activation='relu'),
        layers.Dense(units=2, activation='softmax') # 2 lebo 2 posible output classes 0 or 1
        # Softmax gives also probability for each output class
    ])

    model.summary()

    model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # batch size how many samples are in one batch, processed data in one time
    # epochs how many times will model train on given data
    # shuffle je defaultne TRUE , a sluzi na vymazanie flastnosti poradia ALE JA TO MOZNO VYMAZEM U EEG
    # verbose to see just output messages

    # VALIDATION overfitting problem riesime a uvidime ci je dobry model aj pre netrenovacie data.
    # TOTO je metoda kedy model vzytvori validation data pre nas samotne a nemusi vytvarat dalsi dataset na to
    # validation_split  how mutch we want to split out into validation dataset 0.1  je 10% a tychto 10 percent vstupnych
    # dat sa nebude pouzivat na trenovanie ale ponechaju sa sa validation test
    # tzchto 10 percent je vzdy poslednych 10 pecent dat cize iba poslednych 10 percent vzoriek to bere DOLEZITE!!!!!!!
    #
    model.fit(x=scaled_train_samples,
              y=train_labels,
              validation_split=0.1,
              batch_size=5,
              epochs=30,
              shuffle=True,
              verbose=2)

    # PREDICTION
    prediction = model.predict(x=scaled_test_samples, batch_size=5, verbose=0)
    # DATA su [x,y], kde x udava pravdepodobnost ze je jedna class CLASS 0!!! a y udava pravdepodobnost ze
    # je druha class CLASS 1!!!! je to podla indexu

    # VYBERE MAX A VYPSE JEHO INDEX takze 0 a 1 mame CLASSES
    rounded_prediction = np.argmax(prediction, axis=-1)
    print(rounded_prediction)

    ######################################################################################
    # VYUZIJEME CONFUSION MATRIX aby sme urcili ako si nas model poradil
    cm = confusion_matrix(y_true=test_labels, y_pred=rounded_prediction)

    cm_plot_labels = ['non_self_face', 'self_face']
    plot_confusion_matrix(cm=cm, classes=cm_plot_labels, title='Confusion Matrix')
    # DOKOPY SETKy cisla a modre su dobre prediktnute a biele su zle prediktnute.



    #######################################################################################
    # SAVING AND LOADING KERAS SEQUANTIAL MODEL
    if os.path.isfile('saved_model.h5') is False:
        model.save('saved_model.h5')
    # Ulozi aj natrenovany model.

    loaded_model = load_model('saved_model.h5')

    #######################################################################################
    # Saving just weights of the model.
    if os.path.isfile('model_weights.h5') is False:
        model.save_weights('model_weights.h5')

    # nacitanie a nastavenie váh
    model.load_weights('model_weights.h5')



    #########################################################################################
    ###############                     CNN                                         #########
    #########################################################################################
    
    # OKA

    ###################################################
    # DEEP LEARNING COURSE
    ####################################################
    # BC napisat deep learning a machine learning, supervised and unsepervised atd...
    # https: // www.youtube.com / watch?v = gZmobeGL0Yg


