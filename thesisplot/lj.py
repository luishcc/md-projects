import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 15,
    'figure.figsize': (.9*side, .6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


def lj(x, sigma=1, epsilon=1):
    term2 = (sigma/x)**6
    term1 = term2**2
    return 4*epsilon*(term1-term2)

x = np.linspace(0.3, 2, 1000)

fig, ax = plt.subplots()
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.plot(1, 0, " ", markersize=1, transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, " ", markersize=1, transform=ax.get_xaxis_transform(), clip_on=False)

# ax.spines["left"].set_bounds(0, 10)     # Limit the left spine to y=0 to y=9.8
# ax.spines["bottom"].set_bounds(0, 2)

ax.annotate("", xy=(2.1, 0), xytext=(1.98, 0), clip_on=False,
            arrowprops=dict(arrowstyle="->", linewidth=1.9, color="black"))
ax.annotate("", xy=(0, 10), xytext=(0, 9), clip_on=False,
            arrowprops=dict(arrowstyle="->", linewidth=1.9, color="black"))

ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

ax.spines["left"].set_linewidth(1.6)   
ax.spines["bottom"].set_linewidth(1.6) 

ax.text(0.15, 10, r'$U(r_{ij})$', va="center", ha="center", rotation=0)
ax.text(2.1, -1, r'$r_{ij}$', va="center", ha="center", rotation=0)

ax.set_ylim(-10,10)
ax.plot(x, lj(x, 0.5, 8), 'k-', linewidth=2)

sigma = 0.5  # Assuming sigma is known from the LJ function
ax.annotate(r"$\sigma_{ij}$", xy=(sigma, 0), xytext=(sigma + 0.15, 2.5),
            arrowprops=dict(arrowstyle="->", color="black"))

# Add measuring arrows for epsilon
epsilon_depth = -8  # Assuming epsilon is known from the LJ function
ax.annotate("", xy=(0.3, epsilon_depth), xytext=(0.3, 0),
            arrowprops=dict(arrowstyle="<->", color="black"))
ax.text(0.34, epsilon_depth / 2, r"$\epsilon_{ij}$", va="center", ha="left", color="black")

fig.savefig('app-lj.pdf', dpi=dpi, bbox_inches='tight')

# plt.show()


