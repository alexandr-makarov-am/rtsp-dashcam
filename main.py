import cv2
import queue
import sys
import os
import time
from threading import Thread
from datetime import datetime
from utils import dimensions, resize, get_dir_size, get_oldest_file

q = queue.Queue()

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
    last_time = 0.0
    while True:
        if not q.empty():
            frame = q.get()
            dt = time.time()
            if counter == -1:
                filename = os.path.join(out_dir, descr + "_" + str(datetime.now().strftime("%Y%m%d_%H%M%S")) + ".mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(filename, fourcc, fps, dimensions(frame))
                counter = 0
            if dt - last_time >= 1 / fps:
                last_time = dt
                out.write(resize(frame))
                counter += 1
                print("frames done: " + str(counter) + "/" + str(fps * interval))
                print("queue size: " + str(q.qsize()))
            if counter >= fps * interval:
                out.release()
                counter = -1

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
    t3 = Thread(target=cleaner, args=(out_dir,))
    t3.start()

size_args = len(sys.argv)

if size_args == 4:
    if os.path.exists(sys.argv[3]):
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('directory not found')
else:
    print("wrong number of arguments.")
