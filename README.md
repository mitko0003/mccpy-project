# An Adaptive Color-Based Particle Filter
The implementation is based on the idea from [this paper](http://www.cs.mcgill.ca/~fkaeli/publications/particle_filter.pdf). Additionally, our version allows quasi-random numbers to be used instead of pseudo-random ones.

## Prerequisites
You need the following libraries:
- numpy
- scipy
- opencv

### OpenCV installation instructions
The easiest way to install OpenCV is through anaconda. However this method only works if you want to track an object through the webcam. To get opencv through anaconda use:
```
conda install -c https://conda.binstar.org/menpo opencv3
conda install -c asmeurer pango
```

If you want to track an object from a pre-recorded video you will have to compile opencv yourself. Instructions to do so can be found [here](http://docs.opencv.org/trunk/dd/dd5/tutorial_py_setup_in_fedora.html).

## Possible problems
If a problem occurs when running the particle filter with quasi-random numbers try running `setup.sh` to recompile the quasi-random number generator libraries (only works on linux).

## How to run?
Just run `python particle_filter.py`

