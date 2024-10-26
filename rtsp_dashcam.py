import cv2
import time
import queue
import os
import tempfile
from datetime import datetime
from threading import Thread
from utils import dimensions, move, cleaner

class RTSPDashCam:
    def __init__(self, url, out_dir, index, fps = 15, interval = 10, lifetime = 1, max_dir_size = 128):
        self.q = queue.Queue()
        self.lifespan = time.time()
        self.url = url
        self.out_dir = out_dir
        self.id = index
        self.fps = fps
        self.interval = interval
        self.lifetime = lifetime
        self.exited = False
        self.max_dir_size = max_dir_size
    def __stream(self):
        self.vc = cv2.VideoCapture(self.url)
        print("init __stream")
        while self.vc.isOpened():
            ret, frame = self.vc.read()
            if ret:
                self.q.put(frame)
            if time.time() - self.lifespan >= 60 * self.lifetime:
                self.exited = True
                print("exit __stream")
                break
    def __frame_processor(self):
        done_frames = 0
        stime = 0
        filename = None
        output = None
        tmp = None
        while True:
            if not self.q.empty():
                frame = self.q.get()
                act_fps = done_frames / (time.time() - stime)
                if done_frames == 0:
                    filename = os.path.join(self.out_dir, str(datetime.now().strftime("%Y%m%d_%H%M%S")) + ".mp4")
                    tmp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
                    output = cv2.VideoWriter(tmp.name, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, dimensions(frame))
                    stime = time.time()
                if act_fps < self.fps:
                    output.write(frame)
                    done_frames += 1
                    print("done_frames ", done_frames, ' fps: ', act_fps)
                if done_frames >= self.fps * self.interval or self.exited:
                    output.release()
                    tmp.close()
                    th1 = Thread(target=cleaner, args=(self.out_dir, self.max_dir_size))
                    th1.start()
                    th2 = Thread(target=move, args=(tmp.name, filename))
                    th2.start()
                    done_frames = 0
                    print("saved ", filename)
            if self.exited:
                print("exit __frame_processor")
                break
    def start(self):
        thread1 = Thread(target=self.__stream, args=())
        thread1.start()
        thread2 = Thread(target=self.__frame_processor, args=())
        thread2.start()