import numpy as np


def adjacent_values(x):

    sorted_val = sorted(x)

    # noinspection PyTypeChecker
    q1, md, q3 = np.percentile(x, [25, 50, 75])

    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, sorted_val[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, sorted_val[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def violin(ax, data, color="white", edgecolor=None, alpha=1, grid=True):

    data = list(data)
    n = len(data)

    if isinstance(color, str):
        color = [color, ] * n

    elif isinstance(edgecolor, str) or edgecolor is None:
        edgecolor = [edgecolor, ] * n

    if grid is True:
        ax.yaxis.grid(True, ls=":")
        ax.set_axisbelow(True)

    quartile1, medians, quartile3, whiskers_min, whiskers_max = [], [], [], [], []

    for i in range(n):
        # noinspection PyTypeChecker
        q1, md, q3 = np.percentile(data[i], [25, 50, 75])

        quartile1.append(q1)
        medians.append(md)
        quartile3.append(q3)

        w_min, w_max = adjacent_values(data[i])
        whiskers_min.append(w_min)
        whiskers_max.append(w_max)

    ind = np.arange(1, len(medians) + 1)

    parts = ax.violinplot(
        dataset=data, positions=ind, showmeans=False, showmedians=False,
        showextrema=False)

    for pc, fc, ec in zip(parts['bodies'], color, edgecolor):
        pc.set_facecolor(fc)
        pc.set_edgecolor(ec)
        pc.set_alpha(alpha)

    ax.scatter(ind, medians, marker='o', color='white', s=10, zorder=3)
    ax.vlines(ind, quartile1, quartile3, color='k', linestyle='-', lw=5)
    ax.vlines(ind, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)
    ax.set_xticks(ind)
