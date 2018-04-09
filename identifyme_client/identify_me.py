import sys
import time
import cv2
import os
import numpy
import requests

def main():

    # Define variables.
    # The variable 'webcam' can only be set once. See next comment.
    # OpenCV will attempt to re-assign the webcam whilst it is in use and fail.
    current_location = ""
    face_library = 'face_library'
    face_cascade = cv2.CascadeClassifier('opencv_library/haarcascade_frontalface_default.xml')
    webcam = cv2.VideoCapture(0)

    current_location_id = set_location()

    # Call the usermenu, for user to decide operation.
    usermenu(face_library, face_cascade, webcam, current_location_id)


def usermenu(face_library, face_cascade, webcam, current_location_id):

    # Self plug.
    print("\nIdentifyMe - olirowan")
    print("https://github.com/olirowan")
    print("\nOptions:\n")
    print("- (t) train")
    print("- (i) identify")
    print("- (q) quit")

    # Loop through option choices for user to decide. Validation included.
    # First two options will call functions to perform associated operation.
    # Short hand option supported.
    user_option = raw_input("\nOption choice: ")

    if user_option == "train" or user_option == "t":
        learn_identity(face_library, face_cascade, webcam)

    elif user_option == "identify" or user_option == "i":
        identify_me(face_library, face_cascade, webcam, current_location_id)

    elif user_option == "quit" or user_option == "q":
        sys.exit("\nClosing.\n")

    else:
        print("\nOption not supported.\n")
        usermenu(face_library, face_cascade, webcam)


def set_location():

    server = '192.168.0.39:5000'
    current_location = raw_input("\nPlease set current camera location: ")
    response = requests.get('http://' + server + '/request/locations/' + current_location).json()

    json_result = (response['result'])
    for returns in json_result:
        for item in returns:
            current_location_id = (item['location_id'])

    print(current_location_id)

    return current_location_id

# This function will create a folder of faces, associated with a name.
def learn_identity(face_library, face_cascade, webcam):

    # Request name of subject who will be captured by camera.
    subject_identity = raw_input("Enter subjects name: ")
    subject_path = os.path.join(face_library, subject_identity)

    # Create the folder for the face_library if it does not already exist.
    # This is where named folders of individuals faces will be stored.
    if not os.path.isdir(face_library):
        os.mkdir(face_library)

    # If the subject does not already have a folder associated to their face, it will now be made.
    if not os.path.isdir(subject_path):
        os.mkdir(subject_path)

    # Bit of info for the user.
    print("Starting training. . .")

    # The capture_count variable dictates how many images will be taken of the subject.
    capture_count = 100
    count = 0
    size = 4
    (frame_width, frame_height) = (112, 92)

    # Loop until enough images have been captured.
    while count < capture_count:

        # Read stream from webcam.
        (rval, im) = webcam.read()

        im = cv2.flip(im, 1, 0)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        mini = cv2.resize(gray, (gray.shape[1] / size, gray.shape[0] / size))

        faces = face_cascade.detectMultiScale(mini)
        faces = sorted(faces, key=lambda x: x[3])

        if faces:

            face_i = faces[0]
            (x, y, w, h) = [v * size for v in face_i]
            face = gray[y:y + h, x:x + w]

            face_resize = cv2.resize(face, (frame_width, frame_height))
            pin = sorted([int(n[:n.find('.')]) for n in os.listdir(subject_path)
                          if n[0] != '.'] + [0])[-1] + 1

            cv2.imwrite('%s/%s.png' % (subject_path, pin), face_resize)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(im, subject_identity, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        time.sleep(0.38)

        # Update count, inform user of progress.
        count += 1
        remaining = (100 - count)
        print(str(remaining) + " remaining captures.")

        cv2.imshow('OpenCV', im)
        key = cv2.waitKey(10)
        if key == 27:
            break

    # At the end of the loop - inform user the process completed.
    # Return to usermenu.
    cv2.destroyAllWindows()
    print(str(count) + " images captured. Library saved to folder: " + subject_identity)
    usermenu(face_library, face_cascade, webcam)


# This function enables the camera and attmepts to identify individuals in the viewport.
def identify_me(face_library, face_cascade, webcam, current_location_id):


    print(current_location_id)

    # Create blank arrays and dictionaries in preparation.
    (images, lables, names, id) = ([], [], {}, 0)

    # Obtain a list of subdirectories.
    for (subdirs, dirs, files) in os.walk(face_library):

        # Assign the name of the directory to the ID to be used in the training model.
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(face_library, subdir)

            # The ID will be used as the lable.
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                lable = id
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))

            id += 1

    (width, height) = (130, 100)

    # The images and lables are assigned to a numpy array, to be fed into OpenCV.
    (images, lables) = [numpy.array(lis) for lis in [images, lables]]

    # Train the face recogniser model using the images and the associated labels.
    # The chosen computer vision recognition algorithm is LBPH.
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, lables)

    # Start an indefinite loop of continuously attempting to recognise an individual in each frame.
    while True:


        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if prediction[1] < 85:
                cv2.putText(im, '%s - %.0f' % (names[prediction[0]], prediction[1]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            else:
                cv2.putText(im, 'Unknown', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

        # Open a window to display the camera view.
        # Display frames for 10ms.
        cv2.imshow('IdentifyMe', im)
        key = cv2.waitKey(10)

        # Key 27 is ESC, allowing the user to return to the usermenu.
        if key == 27:
            cv2.destroyAllWindows()
            usermenu(face_library, face_cascade, webcam)

# Call main, start program.
main()
