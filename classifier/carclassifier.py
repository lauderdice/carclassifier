import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds


[train_ds, test_ds], ds_info = tfds.load(
    "cars196",
    split=["train", "test"],
    as_supervised=True,
    with_info=True
)


height, width = 150, 150
size = (150, 150)

train_ds = train_ds.map(lambda x, y: (tf.image.resize(x, size), y))
test_ds = test_ds.map(lambda x, y: (tf.image.resize(x, size), y))
batch_size = 32


def augment_func(image,label):
    image = tf.image.resize_with_crop_or_pad(image,height+6,width+6)
    image = tf.image.random_crop(image, size=[height, width, 3])
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_hue(image, 0.2)
    image = tf.image.random_contrast(image, 0.5, 2)
    image = tf.image.random_saturation(image, 0, 2)
    return image, label

train_ds = train_ds.cache().map(augment_func).shuffle(100).batch(batch_size).prefetch(buffer_size=10)
test_ds = test_ds.cache().batch(batch_size).prefetch(buffer_size=10)
ImageNetModel = tf.keras.applications.Xception(
    weights="imagenet",
    input_shape=(height, width, 3),
    include_top=False,
)

ImageNetModel.trainable = True


inputs = tf.keras.Input(shape=(height, width, 3))

norm_layer = keras.layers.experimental.preprocessing.Normalization()
mean = np.array([127.5] * 3)
var = mean ** 2
# Scale inputs to [-1, +1]
x = norm_layer(inputs)
norm_layer.set_weights([mean, var])


x = ImageNetModel(x, training=False)
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(0.5)(x)
num_outputs = ds_info.features['label'].num_classes
outputs = keras.layers.Dense(num_outputs, activation="softmax")(x)
model = keras.Model(inputs, outputs)
model.summary()


learning_rate = 5.0e-5

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
    loss=keras.losses.SparseCategoricalCrossentropy(),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

epochs = 50
model.fit(train_ds, epochs=epochs, validation_data=test_ds)

model.save("cars196model50epochs.h5", save_format="h5")

