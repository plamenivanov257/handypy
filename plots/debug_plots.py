"""
Creating and managing debug plots
"""
import matplotlib.pyplot as plt


class DebugFigHandler:
    _figs = []  # stores debug figs
    _closed = []

    def new_debug_fig(self):
        fig = plt.figure()
        fig_index = len(self._figs)

        def on_close(event):
            print(f'Closed debug figure {fig_index}')
            self._closed[fig_index] = True

        fig.canvas.mpl_connect('close_event', on_close)
        fig.show()

        self._figs.append(fig)
        self._closed.append(False)

        return fig_index


    def subplots(self, fig_index, *args):
        if self._closed[fig_index]:
            print(f"Debug figure {fig_index} is no longer open! Cannot add subplots!")
            return

        self._figs[fig_index].clf()
        self._figs[fig_index].subplots(*args)


    def update_fig(self, fig_index):
        if self._closed[fig_index]:
            print(f"Debug figure {fig_index} is no longer open! Cannot update it!")
        self._figs[fig_index].canvas.draw()
        input(f"Updated debug figure {fig_index}. Press enter to continue.")
