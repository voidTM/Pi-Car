import argparse
import io
import re
import time

import numpy as np
import picamera

from PIL import Image
# v2.5
from tflite_runtime.interpreter import Interpreter
from queue import Queue


CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

class PiCam(object):

    def __init__(self, model_path: str, label_path: str, threshold: float):
        self.labels = load_labels(label_path)
        self.interpreter = Interpreter(model_path)
        self.threshold = threshold

        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = interpreter.get_input_details()
        self.output_details = interpreter.get_output_details()
        _, self.input_height, self.input_width, _ = interpreter.get_input_details()[0]['shape']

        # initialize camera
        

    # loads a new model
    def load_model(self, model_path: str, label_path: str, threshold: float):
        self.labels = load_labels(label_path)
        self.interpreter = Interpreter(model_path)
        self.threshold = threshold

        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = interpreter.get_input_details()
        self.output_details = interpreter.get_output_details()
        _, self.input_height, self.input_width, _ = interpreter.get_input_details()[0]['shape']


    def stream_detection(self, detected: Queue):
        with picamera.PiCamera(
        resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:
        camera.start_preview()
        try:
            stream = io.BytesIO()
            for _ in camera.capture_continuous(
                stream, format='jpeg', use_video_port=True):
                stream.seek(0)
                image = Image.open(stream).convert('RGB').resize(
                    (input_width, input_height), Image.ANTIALIAS)
                start_time = time.monotonic()
                # detects th objects
                results = detect_objects(interpreter, image, args.threshold)
                elapsed_ms = (time.monotonic() - start_time) * 1000


                identify_objects(results, labels)
                
                stream.seek(0)
                stream.truncate()

        finally:
            camera.stop_preview()

    def detect_objects(interpreter, image, threshold):
      """Returns a list of detection results, each a dictionary of object info."""
      set_input_tensor(interpreter, image)
      interpreter.invoke() # hang here?

      # Get all output details
      boxes = get_output_tensor(interpreter, 0)
      classes = get_output_tensor(interpreter, 1)
      scores = get_output_tensor(interpreter, 2)
      count = int(get_output_tensor(interpreter, 3))

      results = []
      for i in range(count):
        if scores[i] >= threshold:
          result = {
              'bounding_box': boxes[i],
              'class_id': classes[i],
              'score': scores[i]
          }
          results.append(result)
      return results

    def set_input_tensor(self, image):
      """Sets the input tensor."""
      tensor_index = self.interpreter.get_input_details()[0]['index']
      input_tensor = self.interpreter.tensor(tensor_index)()[0]
      input_tensor[:, :] = image


    def get_output_tensor(self, interpreter, index):
      """Returns the output tensor at the given index."""
      output_details = interpreter.get_output_details()[index]
      tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
      return tensor



def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels
