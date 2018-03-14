## Python Dense Optical Flow

**Python** wrapper for Ce Liu's [C++ implementation](https://people.csail.mit.edu/celiu/OpticalFlow/) of Coarse2Fine Optical Flow. This is **super fast and accurate** optical flow method based on Coarse2Fine warping method from Thomas Brox. This python wrapper has minimal dependencies, and it also eliminates the need for C++ OpenCV library. For real time performance, one can additionally resize the images to a smaller size.

Run the following steps to download, install and demo the library:
  ```Shell
  git clone https://github.com/Muugii-bs/pyflow-customized.git
  cd pyflow/
  python setup.py build_ext -i
  python prepare-video.py <input file> <fps> <skip>

  """
  prepare-video.py:
    input: 
      <input file>: the path/name of the target video
      <fps>: defines the "frames per second"
      <skip>: defines how many seconds skipped to choose the base image
    output:
      flow images saved in <input file> (without the '.jpg' extension) + '/flows'
  """
  ```


This wrapper code was developed as part of our [CVPR 2017 paper on Unsupervised Learning using unlabeled videos](http://cs.berkeley.edu/~pathak/unsupervised_video/). Github repository for our CVPR 17 paper is [here](https://github.com/pathak22/unsupervised-video).
