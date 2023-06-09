# -*- coding: utf-8 -*-
"""Video_Utilities.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CsoUQv5lLhPkK2HIUBj-Mi2VLc8w2YQc
"""

import imageio
from tensorflow_docs.vis import embed
import cv2
import tensorflow as tf
import numpy as np
import random
import os


def format_frames(frame, h):
  output_size = (h,h)
  # standardizing pixel values

  frame = tf.image.convert_image_dtype(frame, tf.float32)     # changing  dtype


  # Resizes an img to target width and height by keeping the aspect_ratio same without distortion.
  # If the target dims don't match the image dims, 
  # the img resized and then padded with zeroes to match requested dims.
  frame = tf.image.resize_with_pad(frame, *output_size)
  return frame/225.0

############################################################################

# h  = input('height: \n')
# w  = input('width : \n')
# n_frames = input('Total Frames: \n')
# output_size = (h, w)

###########################################################################

def frames_from_video_file(video_path, h , net_frames, factor):

  # Read each video frame by frame
  result = []
  result.append(np.zeros((h,h,3)))
  src = cv2.VideoCapture(video_path)  

  video_length = src.get(cv2.CAP_PROP_FRAME_COUNT)    # no. of frames in the video file.

  start = (int)(video_length//20)

  src.set(cv2.CAP_PROP_POS_FRAMES, start)

  # ret : bool indicating whether read was successful
  # frame : the image itself

  ct = 0
  for _ in range(start,  start+ net_frames):
    ret, frame = src.read()     # reading next frame
    ct += 1
    if ct%factor !=0:
      continue
    
    if ret:
      frame = format_frames(frame, h)
      result.append(frame)
    else:
      result.append(np.zeros_like(result[0]))

  # result.append(np.array(li))   # converting li to np_array

  src.release()   # Closes video file or capturing device.

  result = np.array(result)[..., [2, 1, 0]]

  return result  # (n_frames, height, width, channels)

#############################################################################

def to_gif(images):
  converted_images = np.clip(images * 255, 0, 255).astype(np.uint8)  #  vals outside interval clipped to interval edges
  imageio.mimsave('./animation.gif', converted_images, fps=4)
  return embed.embed_file('./animation.gif')

############################################################################

class FrameGenerator:
  def __init__(self, video_ids, base_path ,h, n_frames, factor=4):
    
    self.video_ids = video_ids
    self.h = h
    self.factor = factor
    self.net_frames = factor*n_frames
    self.base_path = base_path
    
  def __call__(self):
    # video_paths, classes = self.get_files_and_class_names()
    for vid_id in self.video_ids:
      path = os.path.join(self.base_path, vid_id +'.mp4')
      video_frames = frames_from_video_file(path, self.h, self.net_frames, self.factor) 
      yield video_frames, vid_id