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

We calculate the pixels per cm using some reference and this value can be used to estimate the dimensions of the object.
