# python3
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example using TF Lite to detect objects with the Raspberry Pi camera."""

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

import cv2

CAMERA_WIDTH = 1280 #640
CAMERA_HEIGHT = 720 #480


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


def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


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
    dy = (boxes[i][2] - boxes[i][0])
    dx = (boxes[i][3] - boxes[i][1])
    size = dy * dx
    # objects must be larger than a certain size
    if scores[i] >= threshold and size > 0.1:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results


def identify_objects(queue, results, labels):
  stop_list = ["person", "stop sign"]
  obstacle_list = ['tennis racket', "apple"]
  for obj in results:
      if labels[obj['class_id']] in obstacle_list:
        print("Detected ", labels[obj['class_id']], obj['score'])
        queue.put("obstacle")
      elif labels[obj['class_id']] in stop_list:
        print("Detected ", labels[obj['class_id']], obj['score'])
        queue.put("stop")


#def look_for_objects(obstacle_queue: Queue):

def look_for_objects(shutoff: bool, obstacle_queue: Queue):  
  labels = load_labels("Object-detection/Model/coco_labels.txt")
  interpreter = Interpreter("Object-detection/Model/detect.tflite")

  #labels = load_labels("./picam/Object-detection/Model/mobilenet2labels.txt")
  #interpreter = Interpreter("./picam/Object-detection/Model/mobilenet_v3.tflite")
  interpreter.allocate_tensors()

    # Get input and output tensors.
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()
    # Test the model on random input data.
  input_shape = input_details[0]['shape']
  threshold = 0.6

  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

  with picamera.PiCamera(
      resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=15) as camera:
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

        results = detect_objects(interpreter, image, threshold)

        elapsed_ms = (time.monotonic() - start_time) * 1000
        #print(elapsed_ms)
        identify_objects(obstacle_queue, results, labels)
        
        stream.seek(0)
        stream.truncate()
        if shutoff:
          break

    finally:
      camera.stop_preview()
