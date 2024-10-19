import os

import keras
from imutils import paths

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import imageio
import cv2
from IPython.display import Image
from sklearn.model_selection import train_test_split


IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 10

MAX_SEQ_LENGTH = 20 #frames: if video is shorter than 20 frames, use what's available
NUM_FEATURES = 2048


csv_file = 'video_metadata.csv'
df = pd.read_csv(csv_file)
print(df.head())

X = df['file_path']
y = df['label']


X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.2, random_state = 42)

print(f"Training video paths:\n{X_train.head()}")
print(f"Training labels:\n{y_train.head()}")
print(f"Validation video paths:\n{X_val.head()}")
print(f"Validation labels:\n{y_val.head()}")


train_df = pd.DataFrame({
    'file_path': X_train,
    'label': y_train
})

test_df = pd.DataFrame({
    'file_path': X_val,
    'label': y_val
})

def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y : start_y + min_dim, start_x : start_x + min_dim]


def load_video(path, max_frames=0, resize=(IMG_SIZE, IMG_SIZE)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)


def build_feature_extractor():
    feature_extractor = keras.applications.InceptionV3(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    preprocess_input = keras.applications.inception_v3.preprocess_input

    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    preprocessed = preprocess_input(inputs)

    outputs = feature_extractor(preprocessed)
    return keras.Model(inputs, outputs, name="feature_extractor")


feature_extractor = build_feature_extractor()


label_processor = keras.layers.StringLookup(
    num_oov_indices=0, vocabulary=np.unique(train_df["label"])
)
print(label_processor.get_vocabulary())

# Add this line to save the vocabulary
np.save('model_obj/saved_vocabulary.npy', label_processor.get_vocabulary())

def prepare_all_videos(df, root_dir):
    num_samples = len(df)
    video_paths = df["file_path"].values.tolist()
    labels = df["label"].values
    labels = keras.ops.convert_to_numpy(label_processor(labels[..., None]))

    frame_masks = np.zeros(shape=(num_samples, MAX_SEQ_LENGTH), dtype="bool")
    frame_features = np.zeros(
        shape=(num_samples, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32"
    )

    for idx, path in enumerate(video_paths):
        frames = load_video(os.path.join(root_dir, path))
        frames = frames[None, ...]  # Add batch dimension

        video_length = frames.shape[1]
        print(f"Processing video {idx+1}/{num_samples}: {path}, frames: {video_length}")

        length = min(MAX_SEQ_LENGTH, video_length)

        if length > 0:
            frame_features[idx, :length, :] = feature_extractor.predict(
                frames[0, :length], verbose=0
            )
            frame_masks[idx, :length] = 1  # Mark the valid frames

    return (frame_features, frame_masks), labels


train_data, train_labels = prepare_all_videos(train_df, "")
test_data, test_labels = prepare_all_videos(test_df, "")

print(f"Frame features in train set: {train_data[0].shape}")
print(f"Frame masks in train set: {train_data[1].shape}")


# Utility for our sequence model.
def get_sequence_model():
    class_vocab = label_processor.get_vocabulary()

    frame_features_input = keras.Input((MAX_SEQ_LENGTH, NUM_FEATURES))
    mask_input = keras.Input((MAX_SEQ_LENGTH,), dtype="bool")

    # Refer to the following tutorial to understand the significance of using `mask`:
    # https://keras.io/api/layers/recurrent_layers/gru/
    x = keras.layers.GRU(16, return_sequences=True)(
        frame_features_input, mask=mask_input
    )
    x = keras.layers.GRU(8)(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(8, activation="relu")(x)
    output = keras.layers.Dense(len(class_vocab), activation="softmax")(x)

    rnn_model = keras.Model([frame_features_input, mask_input], output)

    rnn_model.compile(
        loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )
    return rnn_model


# Utility for running experiments.
def run_experiment():
    filepath = "model_obj/.weights.h5"
    checkpoint = keras.callbacks.ModelCheckpoint(
        filepath, save_weights_only=True, save_best_only=True, verbose=1
    )

    seq_model = get_sequence_model()
    history = seq_model.fit(
        [train_data[0], train_data[1]],
        train_labels,
        validation_split=0.3,
        epochs=EPOCHS,
        callbacks=[checkpoint],
    )

    seq_model.load_weights(filepath)
    
    # Get predictions for the test set
    predictions = seq_model.predict([test_data[0], test_data[1]])
    predicted_labels = np.argmax(predictions, axis=1)
    
    # Convert numeric labels back to string labels
    class_vocab = label_processor.get_vocabulary()
    predicted_label_names = [class_vocab[idx] for idx in predicted_labels]
    
    # Convert test_labels to numeric format if they're not already
    if isinstance(test_labels[0], str):
        numeric_test_labels = label_processor(test_labels).numpy()
    else:
        numeric_test_labels = test_labels

    # Check if numeric_test_labels is 2D and flatten it if necessary
    if numeric_test_labels.ndim > 1:
        numeric_test_labels = numeric_test_labels.flatten()

    # Ensure the labels are integers
    numeric_test_labels = numeric_test_labels.astype(int)

    true_label_names = [class_vocab[idx] for idx in numeric_test_labels]

    # Print predictions vs actual labels
    print("\nPredictions vs Actual Labels:")
    print("--------------------------------")
    for pred, true, prob in zip(predicted_label_names, true_label_names, predictions):
        max_prob = np.max(prob)
        print(f"Predicted: {pred:<20} Actual: {true:<20} Confidence: {max_prob:.2f}")

    # Calculate and print accuracy
    accuracy = np.mean(predicted_labels == numeric_test_labels)
    print(f"\nTest accuracy: {accuracy:.2%}")

    # Add this line to save the entire model
    seq_model.save('model_obj/keras_model.h5')

    return history, seq_model


# Run the experiment
_, sequence_model = run_experiment()