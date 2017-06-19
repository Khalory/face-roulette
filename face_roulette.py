import cv2
import sys
import numpy as np
import time
import random

# Get user supplied values
imagePath = sys.argv[1]
cascPath = "haarcascade_frontalface_default.xml"

# Constants!
enableZoom = True
slowZoom = True
allRects = True
fullscreen = True # If not in fullscreen mode, zoom will simply erase extra parts of the image

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.05,
    minNeighbors=3,
    minSize=(2, 2)
)

print("Found {0} faces!".format(len(faces)))

images = np.zeros((len(faces), image.shape[0], image.shape[1], image.shape[2]), dtype='uint8')
ordering = np.zeros((len(faces), 5), dtype='int')
i = 0
# Draw a rectangle around the faces
for i in np.arange(len(images)):
	j = 0
	images[i] = np.array(image)
	for (x, y, w, h) in faces:
		if j == i:
			cv2.rectangle(images[i], (x, y), (x+w, y+h), (0, 255, 0), 2)
		elif allRects:	
			cv2.rectangle(images[i], (x, y), (x+w, y+h), (255, 255, 255), 2)
		ordering[j] = [x, y, w, h, j]
		j += 1

winner = random.randint(0, len(faces)-1)
starter = random.randint(0, len(faces)-1)
# Do sorting so that the roulette moves in a reasonable order
ordering = sorted(ordering, key=lambda rect: rect[1]*image.shape[0] + rect[0])

x, y = ordering[winner][0:2]
w, h = ordering[winner][2:4]
cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Setup the window to use fullscreen
if fullscreen:
	cv2.namedWindow('Pick', cv2.WND_PROP_FULLSCREEN)          
	cv2.setWindowProperty('Pick', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

numKeys = winner + 3*len(faces)
for i in np.arange(starter, numKeys):
	index = ordering[i%len(faces)][4]
	cv2.imshow('Pick', images[index])
	# Function that starts fast but slows down the closer it is to the end
	cv2.waitKey(int(max(1, (i+1-starter)**2.8 / (len(faces)**2))))

cv2.imshow('Pick', image)
cv2.waitKey(1000)

if not enableZoom:
	cv.waitKey(0)
	exit(0)

# Blow up image for prize giving
scales = [3]
if slowZoom:
	scales = np.arange(10, 3, -.025)
for scale in scales:
	minX = max(1, x+w - scale*w)
	minY = max(1, y+h - scale*h)
	maxX = min(image.shape[1], x + scale*w)
	maxY = min(image.shape[0], y + scale*h)
	zoom = image[minY:maxY, minX:maxX, :]
	cv2.imshow('Pick', zoom)
	cv2.waitKey(10)
cv2.waitKey(0)
