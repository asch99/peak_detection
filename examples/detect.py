import sys
sys.path.append("..")

from peak_detection import detect_peaks
from peak_detection import show_peaks

from tifffile import TiffFile

fname = 'sample.tif'

detection_parameters = {'w_s': 10,
                        'peak_radius': 4.,
                        'threshold': 60.,
                        'max_peaks': 10
                        }

sample = TiffFile(fname)
arr = sample.asarray()
peaks = detect_peaks(arr,
                     shape_label=('t', 'z', 'x', 'y'),
                     parallel=True,
                     verbose=True,
                     show_progress=False,
                     **detection_parameters)

for id, p in peaks.groupby(level="stacks"):
    print(p.shape[0])

show_peaks(arr, peaks, 3)
