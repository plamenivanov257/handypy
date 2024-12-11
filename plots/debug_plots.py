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


    def subplots(self, fig_index=0, nrows=1, ncols=1, **kwargs):
        if len(self._figs) == 0 and fig_index == 0:
            print("Have no debug figs... Creating one now!")
            self.new_debug_fig()

        if self._closed[fig_index]:
            print(f"Debug figure {fig_index} is no longer open! Cannot add subplots!")
            return None

        self._figs[fig_index].clf()
        return self._figs[fig_index].subplots(nrows=nrows, ncols=ncols, **kwargs)


    def update_fig(self, fig_index=0):
        if self._closed[fig_index]:
            print(f"Debug figure {fig_index} is no longer open! Cannot update it!")
        self._figs[fig_index].canvas.draw()
        input(f"Updated debug figure {fig_index}. Press enter to continue.")


    def close_figs(self):
        for fig in self._figs:
            plt.close(fig)


    def __init__(self, n=0):
        """
        Creates a handler and initialises n debug figs.
        """
        for i in range(n):
            self.new_debug_fig()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_figs()
