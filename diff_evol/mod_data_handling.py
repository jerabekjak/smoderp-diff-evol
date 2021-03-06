import numpy as np


class RecModData(object):
    """ RecObsData contains data of one observed record """

    def __init__(self, n):

        self.time = np.zeros(n, float)
        self.val = np.zeros(n, float)
        self._n = n

    def set_vals(self, time, val):

        self.time = time
        self.val = val


def read_mod_file(path, col, t_col='time[s]', multip = 1):

    with open(path, 'r') as md:

        lines = md.readlines()
        nlines = len(lines)
        nlineheader = 3
        header = lines[2].replace('#', '').replace(
            ' ', '').replace('\n', '').split(';')
        ncols = len(header)

        data = dict((el, [None]*(nlines-nlineheader)) for el in header)

        for i in range(nlineheader, nlines):
            line = lines[i].replace('\n', '').split(';')
            for j in range(ncols):
                data[header[j]][i-nlineheader] = float(line[j])

        cdata = RecModData(nlines-nlineheader)
        
        for i in range(nlines-nlineheader):
            data[col][i] = data[col][i]*multip
            
        cdata.set_vals(data[t_col], data[col])

        return cdata


def interpolate(mod, obs):

    cdata = RecModData(len(obs.time))

    y_interp = np.interp(obs.time, mod.time, mod.val)

    cdata.set_vals(obs.time, y_interp)

    return cdata
