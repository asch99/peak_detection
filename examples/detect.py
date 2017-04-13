#!/usr/bin/env python
from __future__ import print_function

import sys
sys.path.append("..")

from peak_detection import detect_peaks
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

from peak_detection import show_peaks_plt, show_peaks
show_peaks_plt(arr, peaks, 3)
show_peaks(arr, peaks)
for id, p in peaks.groupby(level="stacks"):
    print(p.shape[0])
