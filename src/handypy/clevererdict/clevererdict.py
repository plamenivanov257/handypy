"""
A recursive mod for CleverDict
"""

import itertools
from cleverdict import CleverDict


class ClevererDict(CleverDict):
    """
    A recursive mod for CleverDict
    """

    def update(self, mapping=(), **kwargs):
        """
        Parameters
        ----------
        The same as dict.update(), i.e.
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]
        """

        if hasattr(mapping, "items"):
            mapping = getattr(mapping, "items")()

        for k, v in itertools.chain(mapping, getattr(kwargs, "items")()):

            # This if statement is the only change relative to the upstream CleverDict
            if isinstance(v, dict) and not isinstance(v, CleverDict):
                v = ClevererDict(v)

            self.__setitem__(k, v)

