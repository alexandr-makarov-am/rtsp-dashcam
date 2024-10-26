import time
import sys
import os
from multiprocessing import Process
from rtsp_dashcam import RTSPDashCam

process_list = []

def process(url, out_dir, index):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    t = RTSPDashCam(url, out_dir, index, 15 ,30, 1)
    t.start()

if __name__ == '__main__':
    process_list = [None] * (len(sys.argv) - 2)
    out_dir = sys.argv[1]
    while True:
        for i, prc in enumerate(process_list):
            key = i + 2
            if prc is None:
                prc = Process(target=process, args=(sys.argv[key], os.path.join(out_dir, str(key)), i + 1))
                prc.start()
                process_list[i] = prc
        running = filter(lambda el: el.is_alive(), process_list)
        if len(list(running)) == 0:
            break
        time.sleep(1)