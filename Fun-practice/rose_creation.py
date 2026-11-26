import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def petal_mesh(angle, length, width, base_z, rise, curl, inner_radius=0.04,
               twist=0.0):
    """Create a cupped petal surface in the flower's local coordinate system."""
    u = np.linspace(0.015, 1.0, 48)
    v = np.linspace(-1.0, 1.0, 27)
    U, V = np.meshgrid(u, v)

    outline = np.sin(np.pi * U) ** 0.68 * (0.38 + 1.0 * U)
    half_width = width * outline
    radius = inner_radius + length * U + 0.08 * U**2
    side = half_width * V
    direction = angle + twist * U**1.7

    X = radius * np.cos(direction) - side * np.sin(direction)
    Y = radius * np.sin(direction) + side * np.cos(direction)
    Z = (
        base_z
        + rise * U
        + 0.10 * np.sin(np.pi * U) * (1.0 - 0.35 * V**2)
        + curl * V**2 * np.sin(np.pi * U) * (0.35 + 0.65 * U)
        + 0.45 * curl * U**3 * np.abs(V) ** 3
        + 0.018 * np.sin(3 * np.pi * U + angle) * np.abs(V) ** 4
    )
    return U, V, X, Y, Z


def add_petal(ax, angle, length, width, base_z, rise, curl, color,
              inner_radius=0.04, twist=0.0, center=(0.0, 0.0),
              scale=1.0, z_offset=0.0):
    U, V, X, Y, Z = petal_mesh(
        angle, length, width, base_z, rise, curl, inner_radius, twist
    )
    X = center[0] + scale * X
    Y = center[1] + scale * Y
    Z = z_offset + scale * Z

    light = 0.58 + 0.28 * U + 0.12 * (1.0 - np.abs(V))
    facecolors = np.empty((*U.shape, 4))
    facecolors[..., :3] = np.clip(
        np.asarray(color) * light[..., np.newaxis], 0.0, 1.0
    )
    facecolors[..., 3] = 1.0

    ax.plot_surface(
        X, Y, Z,
        facecolors=facecolors,
        rstride=1,
        cstride=1,
        linewidth=0,
        edgecolor="none",
        antialiased=True,
        shade=False,
    )
    return X, Y, Z


def add_stem(ax, center, scale, z_offset):
    z = np.linspace(-2.25, 1.12, 100)
    theta = np.linspace(0, 2 * np.pi, 16)
    Z, T = np.meshgrid(z, theta)
    center_x = 0.055 * np.sin(z * 1.1)
    center_y = 0.035 * np.cos(z * 0.9)
    X = center_x[np.newaxis, :] + 0.045 * np.cos(T)
    Y = center_y[np.newaxis, :] + 0.045 * np.sin(T)
    ax.plot_surface(
        center[0] + scale * X,
        center[1] + scale * Y,
        z_offset + scale * Z,
        color="#176b35",
        linewidth=0,
        antialiased=True,
        shade=True,
    )


def add_leaf(ax, angle, base_z, length, center, scale, z_offset):
    X, Y, Z = add_petal(
        ax,
        angle=angle,
        length=length,
        width=0.27,
        base_z=base_z,
        rise=0.11,
        curl=0.035,
        color=(0.055, 0.34, 0.12),
        inner_radius=0.015,
        center=center,
        scale=scale,
        z_offset=z_offset,
    )
    middle = X.shape[0] // 2
    ax.plot(
        X[middle],
        Y[middle],
        Z[middle],
        color="#73a64d",
        linewidth=0.8,
        alpha=0.9,
    )


def add_grass(ax, center, ground_z, scale, orientation):
    t = np.linspace(0.0, 1.0, 18)
    for i in range(4):
        angle = orientation + 2 * np.pi * i / 4
        length = scale * (0.32 + 0.08 * (i % 2))
        radius = length * t
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        z = ground_z + scale * 0.24 * np.sin(np.pi * t / 2)
        ax.plot(
            x,
            y,
            z,
            color="#2b6638",
            linewidth=1.0,
            alpha=0.75,
        )


def add_ground(ax, rng, ground_z):
    angle = rng.uniform(0.0, 2 * np.pi, 1800)
    radius = np.sqrt(rng.uniform(0.0, 1.0, len(angle)))
    ax.scatter(
        3.05 * radius * np.cos(angle),
        2.72 * radius * np.sin(angle),
        np.full_like(radius, ground_z - 0.025),
        c="#315638",
        s=rng.uniform(2.0, 9.0, len(angle)),
        alpha=0.28,
        depthshade=False,
        edgecolors="none",
    )


def add_ground_grass(ax, rng, ground_z):
    t = np.linspace(0.0, 1.0, 9)
    for color, count in (("#285b32", 100), ("#367340", 75), ("#1e482a", 80)):
        angle = rng.uniform(0.0, 2 * np.pi, count)
        radius = np.sqrt(rng.uniform(0.0, 1.0, count))
        x0 = 2.95 * radius * np.cos(angle)
        y0 = 2.62 * radius * np.sin(angle)
        height = rng.uniform(0.12, 0.38, count)
        lean = rng.uniform(-0.16, 0.16, count)
        lean_y = rng.uniform(-0.14, 0.14, count)
        X = x0[:, None] + lean[:, None] * t
        Y = y0[:, None] + lean_y[:, None] * t
        Z = ground_z + height[:, None] * t
        separator = np.full((count, 1), np.nan)
        ax.plot(
            np.concatenate((X, separator), axis=1).ravel(),
            np.concatenate((Y, separator), axis=1).ravel(),
            np.concatenate((Z, separator), axis=1).ravel(),
            color=color,
            linewidth=0.8,
            alpha=0.78,
        )


def add_ellipsoid(ax, center, radii, color, rotation=0.0):
    u = np.linspace(0.0, 2 * np.pi, 28)
    v = np.linspace(-np.pi / 2, np.pi / 2, 20)
    U, V = np.meshgrid(u, v)
    X = radii[0] * np.cos(V) * np.cos(U)
    Y = radii[1] * np.cos(V) * np.sin(U)
    Z = radii[2] * np.sin(V)

    X_rotated = X * np.cos(rotation) + Z * np.sin(rotation)
    Z_rotated = -X * np.sin(rotation) + Z * np.cos(rotation)
    ax.plot_surface(
        center[0] + X_rotated,
        center[1] + Y,
        center[2] + Z_rotated,
        color=color,
        linewidth=0,
        antialiased=True,
        shade=True,
    )


def add_horse(ax, center, ground_z):
    x, y = center
    coat = "#86502f"
    dark_coat = "#57301f"
    body_z = ground_z + 0.88

    add_ellipsoid(ax, (x, y, body_z), (0.83, 0.30, 0.34), coat)
    add_ellipsoid(ax, (x + 0.47, y, ground_z + 0.91),
                  (0.38, 0.28, 0.33), "#754326")
    add_ellipsoid(ax, (x + 0.62, y, ground_z + 1.20),
                  (0.55, 0.20, 0.24), dark_coat, rotation=-0.72)
    add_ellipsoid(ax, (x + 1.02, y, ground_z + 1.52),
                  (0.22, 0.16, 0.29), coat, rotation=-0.22)
    add_ellipsoid(ax, (x + 1.19, y, ground_z + 1.34),
                  (0.18, 0.14, 0.13), "#a66b49", rotation=-0.18)

    for side in (-1, 1):
        ax.plot(
            [x + 0.94, x + 0.98, x + 1.00],
            [y + side * 0.13, y + side * 0.15, y + side * 0.12],
            [ground_z + 1.74, ground_z + 1.95, ground_z + 1.74],
            color=dark_coat,
            linewidth=2.6,
        )
        ax.scatter(
            [x + 1.08],
            [y + side * 0.145],
            [ground_z + 1.59],
            color="#170f0b",
            s=8,
            depthshade=False,
        )

    mane_t = np.linspace(0.0, 1.0, 18)
    mane_x = x + 0.34 + 0.52 * mane_t
    mane_z = ground_z + 1.49 + 0.33 * mane_t + 0.035 * np.sin(8 * np.pi * mane_t)
    ax.plot(
        mane_x,
        np.full_like(mane_x, y),
        mane_z,
        color="#241711",
        linewidth=4.0,
    )
    tail_t = np.linspace(0.0, 1.0, 16)
    ax.plot(
        x - 0.74 - 0.24 * tail_t,
        y + 0.04 * np.sin(2 * np.pi * tail_t),
        body_z - 0.06 - 0.45 * tail_t,
        color="#241711",
        linewidth=3.2,
    )

    legs = (
        (x - 0.53, y - 0.18, -0.07, True),
        (x - 0.47, y + 0.18, 0.03, True),
        (x + 0.48, y - 0.18, 0.05, False),
        (x + 0.52, y + 0.18, -0.04, False),
    )
    for leg_x, leg_y, bend, hind_leg in legs:
        knee_x = leg_x + bend
        if hind_leg:
            path_x = [leg_x, leg_x - 0.12, knee_x + 0.02, knee_x]
            path_z = [
                ground_z + 0.66,
                ground_z + 0.43,
                ground_z + 0.23,
                ground_z + 0.055,
            ]
        else:
            path_x = [leg_x, leg_x + 0.02, knee_x + 0.10, knee_x + 0.10]
            path_z = [
                ground_z + 0.66,
                ground_z + 0.40,
                ground_z + 0.17,
                ground_z + 0.055,
            ]
        ax.plot(
            path_x,
            [leg_y] * len(path_x),
            path_z,
            color=dark_coat,
            linewidth=4.2,
            solid_capstyle="round",
        )
        add_ellipsoid(
            ax,
            (path_x[-1] + 0.045, leg_y, ground_z + 0.035),
            (0.13, 0.10, 0.055),
            "#211711",
        )


def add_rose(ax, center, scale, orientation, z_offset, tint):
    add_stem(ax, center, scale, z_offset)
    add_leaf(
        ax, orientation + 0.10, -0.48, 0.93, center, scale, z_offset
    )
    add_leaf(
        ax, orientation + np.pi + 0.35, -1.05, 0.82,
        center, scale, z_offset
    )
    add_leaf(
        ax, orientation + 2.15, -0.78, 0.70, center, scale, z_offset
    )

    for i in range(5):
        add_petal(
            ax,
            angle=orientation + 2 * np.pi * i / 5 + 0.25,
            length=0.52,
            width=0.16,
            base_z=0.92,
            rise=-0.20,
            curl=0.025,
            color=(0.045, 0.31, 0.10),
            inner_radius=0.02,
            center=center,
            scale=scale,
            z_offset=z_offset,
        )

    petal_layers = (
        (9, 1.16, 0.49, 1.03, -0.06, 0.55, (0.44, 0.012, 0.050), 0.04, 0.10),
        (8, 0.91, 0.43, 1.04, 0.16, 0.47, (0.62, 0.020, 0.072), 0.30, 0.22),
        (7, 0.69, 0.35, 1.05, 0.39, 0.39, (0.76, 0.030, 0.095), 0.08, 0.38),
        (5, 0.49, 0.26, 1.06, 0.57, 0.34, (0.68, 0.018, 0.075), 0.42, 0.72),
    )
    for (count, length, width, base_z, rise, curl, color, offset,
         twist) in petal_layers:
        color = np.clip(np.asarray(color) * tint, 0.0, 1.0)
        for i in range(count):
            variation = np.sin(i * 12.7 + count)
            angle = (
                orientation + 2 * np.pi * i / count
                + offset + 0.035 * variation
            )
            add_petal(
                ax,
                angle,
                length * (1.0 + 0.06 * variation),
                width * (1.0 - 0.05 * variation),
                base_z + 0.025 * variation,
                rise,
                curl,
                color,
                twist=twist * (1.0 + 0.12 * variation),
                center=center,
                scale=scale,
                z_offset=z_offset,
            )


def create_rose_animation():
    fig = plt.figure(figsize=(10, 8), facecolor="#08050a")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#08050a")
    ax.set_axis_off()
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-3.0, 2.8)
    ax.set_zlim(-2.35, 2.25)
    ax.set_box_aspect((1.2, 1.05, 1.0))
    ax.view_init(elev=25, azim=-55)

    rng = np.random.default_rng(15)
    ground_z = -2.12
    rose_layout = (
        (0.00, 0.10, 1.00, 0.00, (1.00, 1.00, 1.00)),
        (-1.65, 0.65, 0.78, 0.28, (0.88, 0.90, 1.20)),
        (1.62, 0.72, 0.80, -0.24, (1.00, 3.00, 1.80)),
        (-1.12, -1.30, 0.72, -0.38, (1.00, 2.20, 0.82)),
        (2.00, -1.32, 0.74, 0.46, (0.92, 1.80, 1.55)),
    )
    add_ground(ax, rng, ground_z)
    add_ground_grass(ax, rng, ground_z)

    roses = []
    aura_points = []
    dust_points = []
    for x, y, scale, orientation, tint in rose_layout:
        center = (x, y)
        z_offset = ground_z + 2.25 * scale
        head_z = z_offset + 1.48 * scale
        roses.append((center, scale, orientation, z_offset, tint))
        aura_points.append(
            rng.normal(
                (x, y, head_z),
                (0.53 * scale, 0.53 * scale, 0.32 * scale),
                (220, 3),
            )
        )
        dust_points.append(
            rng.uniform(
                [x - 1.45 * scale, y - 1.45 * scale, head_z - 0.65 * scale],
                [x + 1.45 * scale, y + 1.45 * scale, head_z + 0.65 * scale],
                (28, 3),
            )
        )
    aura = np.vstack(aura_points)
    glow = ax.scatter(
        aura[:, 0],
        aura[:, 1],
        aura[:, 2],
        c="#ff174d",
        s=42,
        alpha=0.025,
        depthshade=False,
        edgecolors="none",
    )

    for center, scale, orientation, z_offset, tint in roses:
        add_rose(ax, center, scale, orientation, z_offset, tint)
        add_grass(ax, center, ground_z, scale, orientation)
    add_horse(ax, center=(-0.25, -2.12), ground_z=ground_z)

    # Small warm glints give the dark scene a soft, glowing atmosphere.
    dust = np.vstack(dust_points)
    sparkles = ax.scatter(
        dust[:, 0],
        dust[:, 1],
        dust[:, 2],
        c="#ff8b9b",
        s=5,
        alpha=0.42,
        depthshade=False,
        edgecolors="none",
    )

    def animate(frame):
        rotation = frame * 1.5
        phase = np.radians(rotation)
        ax.view_init(
            elev=25 + 2.5 * np.sin(phase),
            azim=-55 + rotation,
        )
        glow.set_alpha(0.018 + 0.018 * (0.5 + 0.5 * np.sin(phase * 1.4)))
        sparkles.set_sizes(2.5 + 4.0 * (0.5 + 0.5 * np.sin(phase + dust[:, 0] * 4)))
        sparkles.set_alpha(0.25 + 0.3 * (0.5 + 0.5 * np.sin(phase * 1.7)))
        return glow, sparkles

    animation = FuncAnimation(
        fig,
        animate,
        frames=240,
        interval=40,
        blit=False,
        repeat=True,
    )
    return fig, animation


def main():
    fig, animation = create_rose_animation()
    plt.show()
    return fig, animation


if __name__ == "__main__":
    main()
