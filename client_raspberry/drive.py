from picamera.array import PiRGBArray
from picamera import PiCamera
from Resolution import Resolution
import cv2
import time

# ----- Global parameters -----
res = Resolution(640, 480);						# Frame resolution
 
camera = PiCamera()							# Initializing picamera
camera.resolution = (res.width, res.height)				# Sets the camera resolution
camera.framerate = 32							# 32 frames per second
streamCapture = PiRGBArray(camera, size=(res.width, res.height))	# Obtain 3-dimensional numpy array from an unencoded RGB capture
 
# Wait camera initializing (adjust luminosity or focus)
time.sleep(0.1)
 
# Capture images continuously from the camera as an infinite iterator
for frame in camera.capture_continuous(streamCapture, format="bgr", use_video_port=True):
	
	# Gets the array representing the image to process
	image = frame.array
 
	# Apply filter in image
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)		# Gray-scale filter
	FrameGray = cv2.GaussianBlur(image, (21, 21), 0)	# GaussianBlur filter
	cv2.imshow("Frame", FrameGray)				# Shows resulting image
	
	# Input the filtered image to ANN_MLP (pre-trained)
	# ANN_MLP manages the DC motors controller according to the input image
	# -----------------------------
	#             TO DO
	# -----------------------------
	
	# clear the stream in preparation for the next frame
	streamCapture.truncate(0)
	
	# Wait for a pressed key => delay 1 milisecond
	key = cv2.waitKey(1) & 0xFF
	
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break