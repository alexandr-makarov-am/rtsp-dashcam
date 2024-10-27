# RTSP DashCam

Python script for looping video recording from rtsp. The script divides rtsp stream into 60 second chunks and save them as .mp4.
Maximum write cycle - 24.9GB

### Installation

```shell
pip install opencv-python-headless
```

### Running the app

```shell
python main.py [rtsp_url] [index] [output_dir] # single process
```

```shell
python multi.py [output_dir] ...[rtsp_url] # multi process
```

- rtsp_url - stream url
- index - id for output video files. Exp: 1,2,3, ...
- output_dir - directory to save output video files
