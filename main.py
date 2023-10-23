from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Create a YouTube object
        yt = YouTube(request.form["url"])

        # Get the highest resolution stream
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
      
        temp_folder = 'temp'
        os.makedirs(temp_folder, exist_ok=True)  # Save in a directory with video title as folder name

        # Download the video
        video_stream.download(output_path=temp_folder)
        video_file = f"{temp_folder}/{yt.title}.mp4"
        return send_file(video_file, as_attachment=True)
      
    except Exception as e:
        return f'Error: {e}'
    

# Example usage
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
