import shutil

import cv2
import queue
import sys
import os
import time
import tempfile
import signal
from threading import Thread
from datetime import datetime
from utils import dimensions, resize, get_dir_size, get_oldest_file

q = queue.Queue()

def move(fr, to):
    shutil.move(fr, to)
    print('file saved to ' + to)

def rtsp_receiver(url):
    vc = cv2.VideoCapture(url)
    while vc.isOpened():
        done, frame = vc.read()
        if done:
            q.put(frame)
    vc.release()

def frame_processor(descr, out_dir, fps = 15, interval = 30):
    out = 0
    counter = -1
    last_time = time.time()
    start_time = 0.0
    filename = None
    tmp = None
    while True:
        if not q.empty():
            frame = q.get()
            dt = time.time()
            if counter == -1:
                filename = os.path.join(out_dir, descr + "_" + str(datetime.now().strftime("%Y%m%d_%H%M%S")) + ".mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                tmp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
                out = cv2.VideoWriter(tmp.name, fourcc, fps, dimensions(frame))
                counter = 0
                start_time = dt
            if dt - last_time > 1 / fps:
                last_time = dt
                out.write(frame)
                counter += 1
                print("frames done: " + str(counter) + "/" + str(fps * interval) + " " + str(dt - start_time) + "s")
                print("queue size: " + str(q.qsize()))
            if counter >= fps * interval:
                out.release()
                tmp.close()
                t3 = Thread(target=cleaner, args=(out_dir,))
                t3.start()
                t4 = Thread(target=move, args=(tmp.name, filename))
                t4.start()
                counter = -1
                start_time = 0
        if time.time() - last_time > 30:
            print("frame processor exiting...")
            os.kill(os.getpid(), signal.SIGINT)

def cleaner(out_dir, max_size = 24990):
    while True:
        if get_dir_size(out_dir) >= max_size:
            old = get_oldest_file(out_dir)
            os.remove(old)
        time.sleep(30)

def main(url, descr, out_dir):
    t1 = Thread(target=rtsp_receiver, args=(url,))
    t1.start()
    t2 = Thread(target=frame_processor, args=(descr, out_dir))
    t2.start()

size_args = len(sys.argv)

if size_args == 4:
    if os.path.exists(sys.argv[3]):
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('directory not found')
else:
    print("wrong number of arguments.")
