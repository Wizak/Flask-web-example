import speech_recognition as sr
import face_recognition
import cv2 

from imageai.Detection import ObjectDetection


def detect_photo(model_path="static/other/yolo-tiny.h5", input_path="static/other/ai_photo.jpg", output_path="static/other/ai_photo_after.jpg"):
    detector = ObjectDetection()

    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()
    detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path, minimum_percentage_probability=40)
    
    names = [d['name'] for d in detection]
    counts = {n: names.count(n) for n in set(names)}

    return counts


def detect_video(frame):
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)  
        
    for top, right, bottom, left in face_locations:
        image = cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(image, 'Person ', (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    return frame


def detect_voice():
    audio = sr.AudioFile('static/other/audio.wav')
    r = sr.Recognizer()

    with audio as source:
        content = r.record(source)
        text = r.recognize_google(content, language='uk')
    
    return text
