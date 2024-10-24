# RTSP DashCam

Python script for looping video recording from rtsp. The script divides rtsp stream into 60 second chunks and save them as .mp4.
Maximum write cycle - 24.9GB

### Installation

```
pip install opencv-python-headless
```

### Running the app

```
python main.py [rtsp_url] [descr] [output_dir]
```

- rtsp_url - stream url
- descr - prefix name for output video files
- output_dir - directory to save output video files
