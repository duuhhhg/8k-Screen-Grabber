import cv2
import os
import glob
import numpy
import heapq
import collections
#take input for processing
new_video = input('Enter filename of video to process: ')

if os.path.exists(new_video):
    print('Processing ' + new_video + '...')
else:
    print('File does not exist.')

new_capture = cv2.VideoCapture(new_video)
#create folder to store images
try:
    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')

except OSError:
    print('Could not create new directory.')

new_frame = 0
#while loop to create an image from each frame
while True:
    #if video is still playing keep processing
    ret, frame = new_capture.read()

    if ret:
        #create images
        name = './captured_images/frame' + str(new_frame) + '.jpg'
        print('Saving ... ' + name)

        #writing the extracted images
        cv2.imwrite(name, frame)

        #increasing frame counter
        new_frame += 1
    else:
        break

#release capture and windows when done
new_capture.release()
cv2.destroyAllWindows()

print(f"Captured {new_frame} images.")
minimum_contours = int(input("Enter the minimum number of contours allowed: "))
#total_desired_images = int(input('How many images would you like to keep? '))

captured_images = os.listdir('./captured_images/')
#initializing dictionary for total contour comparison
#files_contours = {}
#value to store number of total saved images
chosen_ones = 0
#initializing a dict to store the chosen images
#top_contour_counter = {}
#iterate through images - find most contours and save best selections
for img in glob.glob('./captured_images/[frame]*.jpg'):
    image = cv2.imread(img)
    resized_image = cv2.resize(image, (1080, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    #blurry_image = cv2.GaussianBlur(image,(5, 5), cv2.BORDER_DEFAULT)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    canny_image = cv2.Canny(gray_image, 220, 120)
    kernel = numpy.ones((2,2))
    dilated_image = cv2.dilate(canny_image, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilated_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    total_contours = len(contours)
    #preview = cv2.resize(canny_image, (1080, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    #files_contours.update(img=total_contours)
    #need to create function to choose the top selections by total contours
#top_contour_counter = dict(collections.Counter(files_contours).most_common(5))
#print(top_contour_counter)
# for key in files_contours:
#     if key not in top_contour_counter:
#         os.remove(f"./captured_images/{files_contours[key]}")
#     else:
#         chosen_ones += 1
#### heap?
    #contour_heap = heapq.heapify(files_contours)

    #heapq.nlargest(total_desired_images, contour_heap)
#####
    if total_contours < minimum_contours:
        os.remove(img)
    else:
        cv2.imshow('Contours found in ' + img, cv2.drawContours(resized_image, contours, -1, (0, 0, 255), 2))
        cv2.waitKey(1)
        chosen_ones += 1
        print('Total contours in ' + img + ' ' + str(total_contours))#make this an f string???

print(f'Saved {chosen_ones} images!')
