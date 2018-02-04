# depth estimation
# how it works: if we place a object of any particular shape on the joints, it will estimate the distance from that object

# we have a marker of known width W, we place this marker at some distance D from the camera. We take the picture of the
# object and estimate the apparent width in pixels P. Focal lenght = P*D / W
# new D' = W*F/P
import cv2
import numpy as np
import time
import argparse

# focal length = 543.45

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
# KNOWN_DISTANCE = 24.0 # 60.96 cm
KNOWN_DISTANCE = 24 # 60.96 cm

# initialize the known object width, which in this case, the piece of
# paper is 11 inches wide
# KNOWN_WIDTH = 11.0 # 27.94 cm
KNOWN_WIDTH = 11 # 15.24 cm

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help ="path to the video file")
args = vars(ap.parse_args())

if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

firstFrame = None

def find_marker(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5, 5),0)
    # edged = cv2.Canny(gray, 35, 125)
    edged = cv2.Canny(gray, 35, 125)

    # assumption we are looking for the largest contour
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key = cv2.contourArea)
    return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
    # perwidth is the percieved width
	# compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

count = 0
while True:
    (grabbed, frame) = camera.read()
    if not grabbed:
        break
    image = frame.copy()
    marker = find_marker(frame)
    if count == 0:
        focalLength = 543
    else:
        focalLength = focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    box = np.int0(cv2.boxPoints(marker))
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.putText(image, "%.2fft" % (inches / 12), (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
    cv2.imshow("image", image)
    count += 1
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

# initialize the list of images that we'll be using
# IMAGE_PATHS = ["images/2ft.png", "images/3ft.png", "images/4ft.png"]

# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
# image = cv2.imread(IMAGE_PATHS[0])
# marker = find_marker(image)
# focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

# loop over the images
# for imagePath in IMAGE_PATHS:
	# load the image, find the marker in the image, then compute the
	# distance to the marker from the camera
	# image = cv2.imread(imagePath)
	# marker = find_marker(image)
	# inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

	# draw a bounding box around the image and display it
	# box = np.int0(cv2.cv.BoxPoints(marker))
	# cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	# cv2.putText(image, "%.2fft" % (inches / 12), (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
	# cv2.imshow("image", image)
	# cv2.waitKey(0)
