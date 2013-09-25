from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from functools import reduce
import operator


# def show_peaks(arr, peaks, stack_id=0):
#     """
#     Show peaks detected in corresponding array
#     """

#     import matplotlib
#     matplotlib.use('Qt4Agg')
#     import matplotlib.pyplot as plt
#     from matplotlib.patches import Circle

#     xy = list(arr.shape[-2:])
#     nstacks = reduce(lambda x, y: x*y, arr.shape[:-2])
#     arr = arr.reshape([nstacks] + xy)
#     arr_flat = arr[stack_id]

#     ratio = reduce(lambda x, y: x/float(y), arr_flat.shape)
#     fig = plt.figure(figsize=(1 * 10., ratio * 10.))
#     ax = plt.subplot(111)

#     ax.imshow(arr_flat, cmap='gray', interpolation='none')
#     for id, peak in peaks.loc[stack_id].iterrows():
#         outline = Circle((peak['y'], peak['x']), peak['w'],
#                          alpha=0.3, color='red')
#         ax.add_patch(outline)
#         ax.scatter(peak['y'], peak['x'], marker='x')

#     ax.set_xlim(0, arr_flat.shape[1])
#     ax.set_ylim(0, arr_flat.shape[0])

#     fig.show()


def show_peaks(img, peaks):
    iv = InteractiveView(img, peaks)
    iv.show()


class InteractiveView:

    def __init__(self, img, peaks):

        import matplotlib.pyplot as plt
        from matplotlib.widgets import Button, Slider

        self.fig = plt.figure(figsize=(15, 10))
        self.ax = self.fig.add_subplot(111)
        plt.subplots_adjust(bottom=0.15)
        self.i = 1
        self.peaks = peaks
        self.img = img

        if self.img.ndim > 2:
            flatted_dim = [reduce(operator.mul, self.img.shape[:-2])]
            self.img.shape = flatted_dim + list(self.img.shape[-2:])

        self.text = plt.figtext(0.06, 0.05, '', transform=self.fig.transFigure)

        w = 0.1
        h = 0.050
        y_pos = 0.04

        self.axprev = plt.axes([0.7, y_pos, w, h])
        self.bprev = Button(self.axprev, 'Previous')
        self.bprev.on_clicked(self.prev)

        self.axnext = plt.axes([0.8, y_pos, w, h])
        self.bnext = Button(self.axnext, 'Next')
        self.bnext.on_clicked(self.next)

        self.axslide = plt.axes([0.4, 0.04, 0.25, 0.03])
        self.slider = Slider(self.axslide, 'Frames', 1, int(len(self.img)),
                             valinit=1)
        self.slider.on_changed(self.slide)

        self.artists = []
        self.im = None
        self.draw(0)

    def draw(self, i):

        from matplotlib.patches import Circle
        import matplotlib.pyplot as plt

        self.i = i

        if i > len(self.img) or i <= 0:
            self.i = 1
            i = 1

        if self.im:
            self.im.remove()

        for art in self.artists:
            art.remove()
        self.artists = []

        try:
            current_peaks = self.peaks.ix[i-1]
            for j, data in current_peaks.iterrows():
                x = data['x']
                y = data['y']
                w = data['w']
                outline = Circle((y, x), w, alpha=0.4, color='red')
                pt = self.ax.add_patch(outline)
                self.artists.append(pt)

                pt = self.ax.scatter(y, x, marker='+')
                self.artists.append(pt)

            n_peaks = current_peaks.shape[0]
        except:
            n_peaks = 0

        self.text.set_text("Frame %i/%i | Peaks number %i" % (i,
                                                              len(self.img),
                                                              n_peaks))

        self.im = self.ax.imshow(self.img[i-1], interpolation='none', cmap='gray', shape=(2, 2))

        plt.draw()

    def next(self, event=None):
        self.slider.set_val(self.i + 1)

    def prev(self, event=None):
        self.slider.set_val(self.i - 1)

    def slide(self, event):
        self.draw(int(event))

    def show(self):
        self.fig.show()
