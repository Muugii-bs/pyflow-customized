# Author: Deepak Pathak (c) 2016

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals
import time, argparse, sys, os, re, subprocess

import numpy as np
from PIL import Image
import pyflow, cv2

video_name, fps, skip_seconds, step = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
frames_path = video_name.split('.')[0]

def getLength(filename):
  result = subprocess.Popen(["ffprobe", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  a = [x for x in result.stdout.readlines() if "Duration" in x][0].rstrip().lstrip()
  m = re.search(r"(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)", a, re.U).groups(1)
  return int(m[0]) * 60 * 60 + int(m[1]) * 60 + int(m[2])


def create_flows_path():
    duration = getLength(video_name)
    for i in range(0, int(duration / step)):
        os.system("mkdir -m 755 {0}".format(frames_path + '/flows' + str(i)))


def create_frames():
    try:
        os.system('rm -rf {0}'.format(frames_path))
    except Exception as e:
        print(e)
    try:
        os.system('./get-frames.sh {0} {1}'.format(video_name, fps))
    except Exception as e1:
        print(e1)


def create_flows(im1, im2, wrapp_file, flow_file):
    # Flow Options:
    alpha = 0.012
    ratio = 0.75
    minWidth = 20
    nOuterFPIterations = 7
    nInnerFPIterations = 1
    nSORIterations = 30
    colType = 0  # 0 or default:RGB, 1:GRAY (but pass gray image with shape (h,w,1))

    s = time.time()
    u, v, im2W = pyflow.coarse2fine_flow(
        im1, im2, alpha, ratio, minWidth, nOuterFPIterations, nInnerFPIterations,
        nSORIterations, colType)
    e = time.time()
    print('Time Taken: %.2f seconds for image of size (%d, %d, %d)' % (
        e - s, im1.shape[0], im1.shape[1], im1.shape[2]))
    flow = np.concatenate((u[..., None], v[..., None]), axis=2)
    #np.save('examples/outFlow.npy', flow)

    hsv = np.zeros(im1.shape, dtype=np.uint8)
    hsv[:, :, 0] = 255
    hsv[:, :, 1] = 255
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite(flow_file, rgb)
    cv2.imwrite(wrapp_file, im2W[:, :, ::-1] * 255)


if __name__ == '__main__':
    create_frames()
    print('frames path: {0}'.format(frames_path))
    create_flows_path()

    # Get the base & target images
    base_num = int(fps) * skip_seconds + 1

    for f in os.listdir(frames_path):
        if f.endswith('.jpg'):
            frame_num = int(f.split('.')[0]) - 1
            chunk_num = int(frame_num / (int(fps) * step))
            local_num = frame_num % (int(fps) * step)
            if local_num < base_num:
                continue
            if local_num == base_num:
                base_img = np.array(Image.open(frames_path + '/' + f))
                base_img = base_img.astype(float) / 255.
                continue
            target_img = np.array(Image.open(frames_path + '/' + f))
            target_img = target_img.astype(float) / 255.

            create_flows(base_img, target_img, 
                '{0}/wrappImage{1}.png'.format(frames_path + '/flows' + str(chunk_num), str(frame_num)), 
                '{0}/flowImage{1}.jpg'.format(frames_path + '/flows' + str(chunk_num), str(frame_num)))
    print('flows path: {0}'.format(frames_path))

