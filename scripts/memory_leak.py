import os
import sys
import gc
sys.path.append('..')
sys.path.append('../examples')

from tifffile import TiffFile
from peak_detection import detect_peaks

from memory_profiler import LineProfiler, show_results
import memory_profiler as mprof

prof = LineProfiler()

@prof
def test(sample_path):


    detection_params = {'w_s': 11,
                        'peak_radius': 4.,
                        'threshold': 40.,
                        'max_peaks': 4
                        }

    sample = TiffFile(sample_path)

    curr_dir = os.path.dirname(__file__)
    fname = os.path.join(
        curr_dir, os.path.join(sample.fpath, sample.fname))

    arr = sample.asarray()
    peaks = detect_peaks(arr,
                         shape_label=('t', 'z', 'x', 'y'),
                         verbose=True,
                         show_progress=False,
                         parallel=True,
                         **detection_params)

    # del sample
    # sample = None
    gc.get_referrers(arr)
    del arr
    gc.collect()
    # arr = None
    # gc.collect()

data_path = "/media/thor/data/ldtracker/"
data_path = "/home/hadim/Insync/Documents/phd/data/ldtracker"
fpath = os.path.join(data_path, "..", "test.tif")

test(fpath)

show_results(prof)
