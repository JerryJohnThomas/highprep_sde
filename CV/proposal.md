# Volume Estimation

## Setup

We take two cameras and setup them as:

- One covering top view with angle 0&deg;
- One with angle 90&deg; to cover the vertical length.

## Calibration

There are two parameters we care about,

- Extrinnsic parameters - Rotation and translation, which we took care when defined a particular setup for the cameras.
- Intrinsic parameters - The internal camera parameters, which depends on the choice of our cameras.

## Process

- We calculate the pixels per cm using some reference and this value can be used to estimate the dimensions of the object.

- We classify the object being placed in the focus using some classification technique(can be decided based on needs).

- Then we use edge detection techniques to calculate dimensions(in pixels) related to the respective shape of the packaging and then use the `pixels per cm` value to convert the dimensions.

- Using the dimensions, calculate the volume for the respective shape.

## Future Work

The accuracy of this technique will not be 100% since we are estimating only from RGB images. But using LiDAR or any other sensor, this can be hugely improved.
