from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

# Specify a fixed download directory
DOWNLOAD_DIR = 'C:\Downloads'  # Replace with your desired directory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.form['url']
    try:
        yt = YouTube(url)
        selected_quality = request.form['quality']
        if selected_quality == "1024p":
            selected_quality = "720p"  # Replace 1024p with 720p to match Pytube's options
        video_stream = yt.streams.filter(res=selected_quality).first()
        video_size = video_stream.filesize
        video_info = f"Video Size: {video_size / (1024 * 1024):.2f} MB, Quality: {selected_quality}"
    except Exception as e:
        video_info = str(e)
    return render_template('index.html', video_info=video_info)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        yt = YouTube(url)
        selected_quality = request.form['quality']
        if selected_quality == "1024p":
            selected_quality = "720p"  # Replace 1024p with 720p to match Pytube's options
        video_stream = yt.streams.filter(res=selected_quality).first()

        # Use the fixed download directory
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        filename = yt.title + ".mp4"
        output_path = os.path.join(DOWNLOAD_DIR, filename)
        video_stream.download(DOWNLOAD_DIR)

        # Return the downloaded file as an attachment
        return send_file(output_path, as_attachment=True, download_name=filename)
    except Exception as e:
        status = str(e)
        return render_template('index.html', status=status)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
