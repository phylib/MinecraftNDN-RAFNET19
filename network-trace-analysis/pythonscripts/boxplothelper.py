import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def replaceLabel(default_label):
    if default_label == "Entity_Type.MOB":
        return "Mob"
    elif default_label == "Entity_Type.EXP_ORB":
        return "Experience Orb"
    elif default_label == "Entity_Type.EXP_ORB":
        return "Experience Orb"
    elif default_label == "Entity_Type.PLAYER":
        return "Player"
    return default_label

def draw_multiple_boxplots(data_map, title=None, filename="boxplot.pdf", add_mean_label=False, add_total_count=False, outliers=True, yLabel=None):

    # Remove unclassified entity type
    if "Entity_Type.UNDEFINED" in data_map:
        del data_map["Entity_Type.UNDEFINED"]
    if "Entity_Type.EXP_ORB" in data_map:
        del data_map["Entity_Type.EXP_ORB"]


    fig, axarr = plt.subplots(1, len(data_map), figsize=(15,7))

    for i in range(0, len(data_map)):
        axis = axarr[i]
        key = list(data_map.keys())[i]
        label = replaceLabel(key)



        if add_total_count:
            label += "\n(Cnt=" + str(len(data_map[key])) + ")"
        # axis.set_xticklabels(axis.get_xticklabels(), rotation=90)
        if yLabel is not None and i == 0:
            axis.set_ylabel(yLabel)

        median = np.median(data_map[key])
        axis.annotate("Median\n{:.0f}".format(median), xy=(1.05, median), xytext=(1.17, median), fontsize=9, arrowprops=dict(arrowstyle="->", facecolor="black"))
        mean = np.mean(data_map[key])
        axis.annotate("Mean\n{:.2f}".format(mean), xy=(0.95, mean), xytext=(0.55, mean), fontsize=9, arrowprops=dict(arrowstyle="->", facecolor="black"))

        bp = axis.boxplot(data_map[key], labels=[label], showmeans=True, showfliers=outliers)
        #add_values(bp, axis)

    if title != None:
        fig.suptitle(title)

    fig.tight_layout()
    fig.subplots_adjust(top=0.9)

    plt.savefig(filename)
