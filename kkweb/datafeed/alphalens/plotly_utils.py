import random
import matplotlib.cm as cm
import matplotlib.colors as mcolors
#what is this for?
def random_color():
    # 生成随机颜色代码
    return "#{:02x}{:02x}{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )

def get_rgb_color(index: int, total: int, cump: str = "coolwarm") -> str:
    norm = mcolors.Normalize(vmin=0, vmax=total - 1)
    cmap = cm.ScalarMappable(norm=norm, cmap=cump)
    color = cmap.to_rgba(index)[:3]
    color = "rgb(" + ",".join([str(int(255 * c)) for c in color]) + ")"

    return color