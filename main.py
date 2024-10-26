import sys
import os
from rtsp_dashcam import RTSPDashCam

if __name__ == '__main__':
    size_args = len(sys.argv)
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
    t = RTSPDashCam(sys.argv[1], sys.argv[2], int(sys.argv[3]), 15, 30, 1)
    t.start()
