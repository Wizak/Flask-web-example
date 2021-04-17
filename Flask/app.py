from flask import Flask, render_template, url_for, request, redirect, Response
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure

import clustering
import detection
import efecting
import time
import random
import numpy as np 
import cv2
import io


app = Flask(__name__)
camera = cv2.VideoCapture(0)

selector_ni_video = 0
selector_ni_photo = 'gray'
clustering_points = []


def ni_clustering_gen_frame():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.grid()
    cl_x, cl_y, nc_x, nc_y, c = clustering.avaragek(clustering_points[0], clustering_points[1], clustering_points[2])
    [axis.scatter(cl_x[i], cl_y[i]) for i in range(len(c))]
    axis.scatter(nc_x, nc_y, s=120, marker='s', c='black')
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return output.getvalue()


def ni_video_gen_frames(): 
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ni_video_gen_frames_after():  
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            frame = efecting.efect_video(selector_ni_video, frame)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ni_photo_gen_frame(): 
    photo_ni = cv2.imread('static/other/ni_photo.jpg')
    _, buffer = cv2.imencode('.jpg', photo_ni)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ni_photo_gen_frame_after(): 
    efecting.efect_photo(selector_ni_photo)
    frame = cv2.imread('static/other/ni_photo_after.jpg')
    _, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ai_video_gen_frames(): 
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ai_video_gen_frames_after():  
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            frame = detection.detect_video(frame)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ai_photo_gen_frame(): 
    frame = cv2.imread('static/other/ai_photo.jpg')
    _, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ai_photo_gen_frame_after(): 
    frame = cv2.imread('static/other/ai_photo_after.jpg')
    _, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ai_audio_gen_frame():
    with open("static/other/audio.wav", "rb") as fwav:
        data = fwav.read(1024)
        while data:
            yield data
            data = fwav.read(1024)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/analisys')
def analisys():
    return render_template('analisys.html')


@app.route('/analisys/ai_video', methods=['POST', 'GET'])
def ai_video():
    if request.method == 'POST':
        return render_template('ai_video.html')
    else:
        return render_template('ai_video.html')


@app.route('/analisys/ai_photo', methods=['POST', 'GET'])
def ai_photo():
    text = ''
    if request.method == 'POST':
        image = request.files['photo']
        image.save('static/other/ai_photo.jpg')
        info = detection.detect_photo()
        for i in list(info.items()):
            i = list(map(str, i))
            text += ': '.join(i) + '\n'
        return render_template('ai_photo.html', text=text)
    else:
        return render_template('ai_photo.html', text=text)


@app.route('/analisys/ai_audio', methods=['POST', 'GET'])
def ai_audio():
    text = ''
    if request.method == 'POST':
        audio = request.files['audio']
        audio.save('static/other/audio.wav')
        text = detection.detect_voice()
        print('DETECT VOICE | '+text)
        return render_template('ai_audio.html', text=text)
    else:
        return render_template('ai_audio.html', text=text)


@app.route('/analisys/ni_video', methods=['POST', 'GET'])
def ni_video():
    global selector_ni_video
    if request.method == 'POST':
        selector_ni_video = int(request.form['efect'])
        return redirect('/analisys/ni_video')
    else:
        return render_template('ni_video.html')


@app.route('/analisys/ni_photo', methods=['POST', 'GET'])
def ni_photo():
    global selector_ni_photo
    if request.method == 'POST':
        selector_ni_photo = request.form['efect']
        image = request.files['photo']
        image.save('static/other/ni_photo.jpg')
        return redirect('/analisys/ni_photo')
    else:
        return render_template('ni_photo.html')


@app.route('/analisys/ni_clustering', methods=['POST', 'GET'])
def ni_clustering():
    global clustering_points
    if request.method == 'POST':
        try:
            points = int(request.form['points'])
            centers = int(request.form['centers'])
            edge = [int(request.form['a']), int(request.form['b'])]
            clustering_points = [centers, points, edge]
            return redirect('/analisys/ni_clustering')
        except:
            return redirect('/analisys/ni_clustering')
    else:
        return render_template('ni_clustering.html')


@app.route("/ni_clustering_feed")
def ni_clustering_feed():
    return Response(ni_clustering_gen_frame(), mimetype="image/png")

@app.route('/ni_video_feed')
def ni_video_feed():
    return Response(ni_video_gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/ni_video_feed_after')
def ni_video_feed_after():
    return Response(ni_video_gen_frames_after(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/ni_photo_feed')
def ni_photo_feed():
    return Response(ni_photo_gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/ni_photo_feed_after')
def ni_photo_feed_after():
    return Response(ni_photo_gen_frame_after(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/ai_video_feed')
def ai_video_feed():
    return Response(ai_video_gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/ai_video_feed_after')
def ai_video_feed_after():
    return Response(ai_video_gen_frames_after(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/ai_photo_feed')
def ai_photo_feed():
    return Response(ai_photo_gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/ai_photo_feed_after')
def ai_photo_feed_after():
    return Response(ai_photo_gen_frame_after(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/ai_audio_feed")
def ai_audio_feed():
    return Response(ai_audio_gen_frame(), mimetype="audio/x-wav")


if __name__ == "__main__":
    app.run(debug=True)