import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, Concatenate, Conv2D, Flatten, Dense, MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.initializers import RandomNormal, Constant, GlorotNormal
from tensorflow import math
import matplotlib.pyplot as plt


def angle_loss_fn(y_true, y_pred):
    x_p = math.sin(y_pred[:, 0]) * math.cos(y_pred[:, 1])
    y_p = math.sin(y_pred[:, 0]) * math.sin(y_pred[:, 1])
    z_p = math.cos(y_pred[:, 0])

    x_t = math.sin(y_true[:, 0]) * math.cos(y_true[:, 1])
    y_t = math.sin(y_true[:, 0]) * math.sin(y_true[:, 1])
    z_t = math.cos(y_true[:, 0])

    norm_p = math.sqrt(x_p * x_p + y_p * y_p + z_p * z_p)
    norm_t = math.sqrt(x_t * x_t + y_t * y_t + z_t * z_t)

    dot_pt = x_p * x_t + y_p * y_t + z_p * z_t

    angle_value = dot_pt/(norm_p * norm_t)
    angle_value = tf.clip_by_value(angle_value, -0.99999, 0.99999)

    loss_val = (math.acos(angle_value))


    return tf.reduce_mean(loss_val, axis=-1)

# model_dir = ''
dataset_folder = "../datasets/"

x_img = np.load(dataset_folder + 'dataset_x_img.npy')
x_head_angles = np.load(dataset_folder + 'dataset_x_head_angles.npy')
y_gaze_angles = np.load(dataset_folder + 'dataset_y_gaze_angles.npy')

x_img_train, x_img_test, x_ha_train, x_ha_test, y_gaze_train, y_gaze_test = train_test_split(x_img, x_head_angles,
                                                                                             y_gaze_angles,
                                                                                             test_size=0.2,
                                                                                             random_state=42)


# Build the model
image_input = Input((36, 60, 1))
head_pose_input = Input((2,))

initialiser_normal = RandomNormal(mean=0., stddev=0.1)
initialiser_const = Constant(value=0)
initialiser_xavier = GlorotNormal(seed=None)

x = Conv2D(filters=20,
             kernel_size=(5, 5),
             strides=1,
             padding='valid',
             kernel_initializer=initialiser_normal,
             bias_initializer=initialiser_const,
             activation='relu'
           ) (image_input)

x = MaxPool2D(strides=2, pool_size = 2) (x)

x = Conv2D(filters=50,
             kernel_size=(5, 5),
             strides=1,
             padding='valid',
             kernel_initializer=initialiser_normal,
             bias_initializer=initialiser_const,
             activation='relu'
           ) (x)

x = MaxPool2D(strides=2, pool_size = 2) (x)

x = Flatten() (x)
# relu
x = Dense(500,
          activation='relu',
          kernel_initializer=initialiser_xavier,
          bias_initializer=initialiser_const,
          ) (x)

x = Concatenate()([head_pose_input, x])

output = Dense(2) (x)

model = Model(inputs = [image_input, head_pose_input], outputs = output)

model.compile(
    # optimizer="sgd",
    optimizer = tf.keras.optimizers.SGD(),
    loss=angle_loss_fn,
    metrics=[angle_loss_fn],
)

history = model.fit([x_img_train, x_ha_train], y_gaze_train, batch_size=128, epochs=50, shuffle=True, validation_split=0.1)

# model.save(model_dir + 'lenet_trained.h5')

score = model.evaluate([x_img_test, x_ha_test], y_gaze_test, verbose=0)

print(score)

#Plotting

# num_epochs = np.arange(0, 50)
#
# plt.figure(dpi=200)
# plt.style.use('ggplot')
# plt.plot(num_epochs, history.history['angle_loss_fn'], label='train_loss', c='red')
# plt.plot(num_epochs, history.history['val_angle_loss_fn'], label='val_loss', c='green')
# plt.title('Training Loss and Val loss')
# plt.xlabel('Epoch')
# plt.ylabel('Loss/Accuracy')
# plt.legend()
# plt.savefig('plotle2.png')
