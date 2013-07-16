from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from functools import reduce

def show_peaks(arr, peaks, stack_id=0):
    """
    Show peaks detected in corresponding array
    """

    import matplotlib
    matplotlib.use('Qt4Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    xy = list(arr.shape[-2:])
    nstacks = reduce(lambda x, y: x*y, arr.shape[:-2])
    arr = arr.reshape([nstacks] + xy)
    arr_flat = arr[stack_id]

    ratio = reduce(lambda x, y: x/float(y), arr_flat.shape)
    fig = plt.figure(figsize=(1 * 10., ratio * 10.))
    ax = plt.subplot(111)

    ax.imshow(arr_flat, cmap='gray', interpolation='none')
    for id, peak in peaks.loc[stack_id].iterrows():
        outline = Circle((peak['y'], peak['x']), peak['w'], alpha=0.3, color='red')
        ax.add_patch(outline)
        ax.scatter(peak['y'], peak['x'], marker='x')

    ax.set_xlim(0, arr_flat.shape[1])
    ax.set_ylim(0, arr_flat.shape[0])


    plt.show()

