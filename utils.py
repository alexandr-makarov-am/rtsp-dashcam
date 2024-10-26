import os
import cv2
import shutil

# return directory size in MB
def get_dir_size(dir = '.'):
    total_size = 0
    for path, _, filenames in os.walk(dir):
        for f in filenames:
            fp = os.path.join(path, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size / 1024 / 1024

# return oldest file in the directory
def get_oldest_file(dir = '.'):
    list_of_files = [os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.mp4')]
    return sorted(list_of_files, key=os.path.getctime)[0]

def dimensions(frame, width = 1440):
    # height = int(frame.shape[0] * (width/frame.shape[1]))
    return frame.shape[1], frame.shape[0]

def resize(frame_input):
    dim = dimensions(frame_input)
    return cv2.resize(frame_input, dim, interpolation=cv2.INTER_AREA)

def move(fr, to):
    shutil.move(fr, to)

def cleaner(out_dir, max_size = 24990):
    if get_dir_size(out_dir) >= max_size:
        old = get_oldest_file(out_dir)
        os.remove(old)
