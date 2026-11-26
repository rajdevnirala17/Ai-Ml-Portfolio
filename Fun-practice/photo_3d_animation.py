import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

# 1. Load photograph
import tkinter as tk
from tkinter import filedialog

# Select image from computer
root = tk.Tk()
root.withdraw()

image_path = filedialog.askopenfilename(
    title="Select Your Photo",
    filetypes=[
        ("Image Files", "*.jpg *.jpeg *.png")
    ]
)

if not image_path:
    print("No image selected!")
    exit()

img = Image.open(image_path).convert("RGB")

print("Image loaded successfully!")

# Resize for better performance
img.thumbnail((700, 700), Image.Resampling.LANCZOS)

pixels = np.array(img)
height, width, _ = pixels.shape

# 2. Convert photograph into particles
np.random.seed(42)

yy, xx = np.mgrid[0:height, 0:width]

colors = pixels.reshape(-1, 3) / 255.0
brightness = colors.mean(axis=1)

# Select visible particles
mask = brightness > 0.08

x = xx.flatten()[mask]
y = yy.flatten()[mask]
rgb = colors[mask]
light = brightness[mask]

# 3. Convert into 3D coordinates
x = (x - width / 2) / (width / 2) * 2.5
z = (height / 2 - y) / (height / 2) * 2.5

# Give every particle a depth
depth = (light - 0.3) * 0.5
depth += np.random.normal(0, 0.035, len(depth))

# 4. Create glowing colours
glow_colors = np.column_stack((
    rgb,
    np.full(len(rgb), 0.18)
))

core_colors = np.column_stack((
    np.clip(rgb * 1.5, 0, 1),
    np.full(len(rgb), 0.95)
))

# 5. Create 3D canvas
fig = plt.figure(figsize=(12, 10),dpi=120, facecolor="black")

ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor("black")

ax.set_axis_off()

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)

ax.view_init(elev=0, azim=-90)

# 6. Glowing particle layers
halo = ax.scatter(
    x, depth, z,
    c=glow_colors,
    s=5,
    depthshade=False
)

particles = ax.scatter(
    x, depth, z,
    c=core_colors,
    s=2,
    depthshade=False
)

# 7. 3D rotation animation
def animate(frame):

    angle = np.radians(frame)

    # Rotate around vertical axis
    xr = x * np.cos(angle) - depth * np.sin(angle)
    yr = x * np.sin(angle) + depth * np.cos(angle)

    # Update glowing particles
    halo._offsets3d = (xr, yr, z)
    particles._offsets3d = (xr, yr, z)

    # Change camera angle
    ax.view_init(elev=0, azim=-90)

    return halo, particles

# 8. Start animation
ani = FuncAnimation(
    fig,
    animate,
    frames=360,
    interval=35,
    blit=False
)

plt.show()