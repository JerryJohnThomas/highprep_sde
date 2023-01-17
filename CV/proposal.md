# Volume Estimation

## Setup

Two cameras are set up in a specific configuration to capture different perspectives of an object or scene.

- The first camera is positioned to capture a top view, with an angle of 0 degrees. This camera will provide a bird's eye view of the subject, showing the top surface and the surrounding area.

- The second camera is positioned with an angle of 90 degrees to the first camera, capturing the vertical length of the subject.

This camera will provide a side view of the subject, showing its height and any features along its vertical length. This configuration of two cameras with different angles allows for a more comprehensive and detailed understanding of the subject being captured.

## Calibration

In the context of our current discussion, there exist two distinct categories of parameters that warrant attention. These parameters are known as extrinsic and intrinsic parameters.

Extrinsic parameters pertain to the rotation and translation of the cameras in a particular setup. It is crucial to take these parameters into consideration when defining the configuration of the cameras as they have a direct impact on the overall performance of the system.

On the other hand, intrinsic parameters are internal camera parameters that are dependent on the specific cameras chosen for the system. These parameters are closely related to the optics of the camera and have a significant influence on the image quality and resolution. It is thus imperative to give due consideration to the intrinsic parameters while selecting cameras for the system.

## Process

We use a technique called "pixels per cm" calculation to estimate the dimensions of an object. This method involves using a reference object of known dimensions and measuring the number of pixels it occupies in an image captured by the camera. This value can then be used to determine the dimensions of other objects in the image by comparing their pixel counts.

We then use classification techniques to identify the object that is in focus. This could involve training a machine learning model on a dataset of labeled images, or using pre-existing algorithms for object recognition.

Once the object has been identified, we apply edge detection techniques to calculate the dimensions of the object in pixels. Edge detection is a technique used to find the boundaries of an object in an image. By identifying the edges of the object, we can determine its shape and calculate its dimensions.

Finally, we use the previously calculated "pixels per cm" value to convert the dimensions from pixels to centimeters. With the dimensions in centimeters, we can then calculate the volume of the object using formulas specific to the shape of the object.

For example, if the object is a cuboid, we can calculate its volume by multiplying its length, width and height. If the object is a cylinder we can calculate its volume by πr²h.

## Future Work

- We can add a weighing scale which will also calculate the deadweight.

- The accuracy of this technique will not be 100% since we are estimating only from RGB images. But using LiDAR or any other sensor, this can be hugely improved.
