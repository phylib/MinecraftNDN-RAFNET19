import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 24})
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


def draw_burstiness(burst_matrix, title=None, filename="burstiness.pdf",
                    yLabel=None,
                    xLabel="Tick Number",
                    autoincrease=True, colorbar=False,
                    cmap=mp.colors.ListedColormap(['black', 'grey', 'white', 'green', 'red']), cmap_bounds=[-1, 0, 1, 2,3, 4]):

    maxlen=0
    for vector in burst_matrix:
        if len(vector) > maxlen:
            maxlen = len(vector)

    matrix = np.zeros((len(burst_matrix), maxlen))
    for i in range(0, len(burst_matrix)):
        for z in range(0, len(burst_matrix[i])):
            matrix[i,z] = burst_matrix[i][z]
            if autoincrease and z > 0 and matrix[i,z-1] >= 1 and matrix[i,z] == 1:
                matrix[i, z] = 2

    for i in range(0, 1):
        matrix[len(burst_matrix) - 1, maxlen - 20 + i] = 3.0

    norm = mp.colors.BoundaryNorm(cmap_bounds, cmap.N)

    # for i in range(0, len(burst_matrix)):
    #     burst_matrix[i] = list(np.array(list(burst_matrix[i]) + list(np.zeros(maxlen - len(burst_matrix)))).astype(float))
    #
    # burst_matrix = np.array(burst_matrix, dtype=float)

    fig, axarr = plt.subplots(1, 1, figsize=(40, 15))
    img = axarr.imshow(matrix, interpolation="nearest", aspect='auto', cmap = cmap,norm=norm, vmin=np.min(matrix), vmax=np.max(matrix))

    if colorbar:
        fig.colorbar(img)

    if title is not None:
        axarr.set_title(title)

    axarr.get_yaxis().set_ticks([])

    if xLabel != None:
        plt.xlabel(xLabel)
    if yLabel != None:
        plt.ylabel(yLabel)

    fig.tight_layout()
    plt.savefig(filename)