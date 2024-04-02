from comtypes.tools.typedesc import SAFEARRAYType
from django.conf import settings
import os


class FatigueDetections:
    def start_process(self):
        import cv2
        import os
        from keras.models import load_model
        import numpy as np
        from pygame import mixer
        import time

        mixer.init()
        sound = mixer.Sound(os.path.join(settings.MEDIA_ROOT, 'alarm.wav'))

        face = cv2.CascadeClassifier(
            os.path.join(settings.MEDIA_ROOT, 'haar cascade files', 'haarcascade_frontalface_alt.xml'))
        leye = cv2.CascadeClassifier(
            os.path.join(settings.MEDIA_ROOT, 'haar cascade files', 'haarcascade_lefteye_2splits.xml'))
        reye = cv2.CascadeClassifier(
            os.path.join(settings.MEDIA_ROOT, 'haar cascade files\haarcascade_righteye_2splits.xml'))

        lbl = ['Close', 'Open']

        model = load_model(os.path.join(settings.MEDIA_ROOT, 'models', 'cnncat2.h5'))
        path = os.getcwd()
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        count = 0
        score = 0
        thicc = 2
        rpred = [99]
        lpred = [99]
        flag = False

        while (True):
            ret, frame = cap.read()
            height, width = frame.shape[:2]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
            left_eye = leye.detectMultiScale(gray)
            right_eye = reye.detectMultiScale(gray)

            cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)

            for (x, y, w, h) in right_eye:
                r_eye = frame[y:y + h, x:x + w]
                count = count + 1
                r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
                r_eye = cv2.resize(r_eye, (24, 24))
                r_eye = r_eye / 255
                r_eye = r_eye.reshape(24, 24, -1)
                r_eye = np.expand_dims(r_eye, axis=0)
                predict_x = model.predict(r_eye)
                rpred = np.argmax(predict_x,axis=1)
                # rpred = model.predict_classes(r_eye)
                if (rpred[0] == 1):
                    lbl = 'Open'
                if (rpred[0] == 0):
                    lbl = 'Closed'
                break

            for (x, y, w, h) in left_eye:
                l_eye = frame[y:y + h, x:x + w]
                count = count + 1
                l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
                l_eye = cv2.resize(l_eye, (24, 24))
                l_eye = l_eye / 255
                l_eye = l_eye.reshape(24, 24, -1)
                l_eye = np.expand_dims(l_eye, axis=0)
                predict_x = model.predict(l_eye)
                lpred = np.argmax(predict_x,axis=1)
                # lpred = model.predict_classes(l_eye)
                if (lpred[0] == 1):
                    lbl = 'Open'
                if (lpred[0] == 0):
                    lbl = 'Closed'
                break

            if (rpred[0] == 0 and lpred[0] == 0):
                score = score + 1
                cv2.putText(frame, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            # if(rpred[0]==1 or lpred[0]==1):
            else:
                score = score - 1
                cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            if (score < 0):
                score = 0
            cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            if (score > 15):
                # person is feeling sleepy so we beep the alarm
                cv2.imwrite(os.path.join(path,'assets','static','image.jpg'), frame)
                try:
                    sound.play()
                    flag = True

                except:  # isplaying = False
                    pass
                if (thicc < 16):
                    thicc = thicc + 2
                else:
                    thicc = thicc - 2
                    if (thicc < 2):
                        thicc = 2
                cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)
            cv2.imshow('frame press Q to Exit', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        return flag
    
    def yawn_detection(self):
        import cv2
        import numpy as np
        from keras.models import load_model

        # Set the size of the input images
        img_size = (224, 224)

        # Load the trained model
        try:
            model = load_model(r'D:\DriverDrowsiness (4)\DriverDrowsiness\yawn_detection_model.h5',compile=False)
        except Exception as e:
            print("Error loading the model:", e)
            exit()

        # Open the camera stream
        cap = cv2.VideoCapture(0)

        # Check if the camera is opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
            exit()

        print("Camera opened successfully.")

        # Loop through the frames from the camera
        while True:
            # Read a frame from the camera
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame from camera.")
                break
            
            # Preprocess the frame
            img = cv2.resize(frame, img_size)
            img = np.expand_dims(img, axis=0)
            img = img / 255.0
            
            # Predict whether the frame contains a yawn or not
            try:
                prediction = model.predict(img)
                if prediction[0] > 0.8:
                    label = 'yawn'
                else:
                    label = 'not yawn'
            except Exception as e:
                print("Error predicting:", e)
                break
            
            # Draw the label on the frame
            cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show the frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close all windows
        cap.release()
        cv2.destroyAllWindows()
