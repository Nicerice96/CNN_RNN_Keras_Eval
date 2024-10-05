import os
import numpy as np
import cv2
import keras
from keras.models import load_model

# Constants
IMG_SIZE = 224
MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048

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

def prepare_single_video(path):
    frames = load_video(path)
    frames = frames[None, ...]

    frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH,), dtype="bool")
    frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

    for i, batch in enumerate(frames):
        video_length = batch.shape[0]
        length = min(MAX_SEQ_LENGTH, video_length)
        for j in range(length):
            frame_features[i, j, :] = feature_extractor.predict(
                batch[None, j, :], verbose=0
            )
        frame_mask[i, :length] = 1  # 1 = not masked, 0 = masked

    return frame_features, frame_mask

def main(video_path):
    global feature_extractor, sequence_model, label_processor

    # Load the feature extractor
    feature_extractor = build_feature_extractor()

    # Load the sequence model
    sequence_model = load_model('model_obj/keras_model.h5')

    # Load the label processor
    label_processor = keras.layers.StringLookup(
        num_oov_indices=0, vocabulary=np.load('model_obj/saved_vocabulary.npy')
    )

    # Prepare the video
    frame_features, frame_mask = prepare_single_video(video_path)

    # Predict
    probabilities = sequence_model.predict([frame_features, frame_mask])[0]

    # Get the predicted class
    predicted_label_index = np.argmax(probabilities)
    predicted_label = label_processor.get_vocabulary()[predicted_label_index]

    print(f"The video is classified as: {predicted_label}")
    print(f"Probability: {probabilities[predicted_label_index]:.2f}")

if __name__ == "__main__":
    video_path = input("Enter the path to the video file: ")
    main(video_path)