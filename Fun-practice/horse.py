import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def add_ellipsoid(ax, center, radii, color, rotation=0.0):
    u = np.linspace(0, 2 * np.pi, 52)
    v = np.linspace(-np.pi / 2, np.pi / 2, 36)
    U, V = np.meshgrid(u, v)

    x = radii[0] * np.cos(V) * np.cos(U)
    y = radii[1] * np.cos(V) * np.sin(U)
    z = radii[2] * np.sin(V)
    X = center[0] + x * np.cos(rotation) + z * np.sin(rotation)
    Y = center[1] + y
    Z = center[2] - x * np.sin(rotation) + z * np.cos(rotation)

    surface = ax.plot_surface(
        X,
        Y,
        Z,
        color=color,
        linewidth=0,
        edgecolor="none",
        antialiased=False,
        shade=True,
    )
    return surface, X, Y, Z


def set_surface_vertices(surface, X, Y, Z):
    vertices = np.stack((X, Y, Z), axis=-1)
    quads = np.stack(
        (
            vertices[:-1, :-1],
            vertices[1:, :-1],
            vertices[1:, 1:],
            vertices[:-1, 1:],
        ),
        axis=2,
    )
    surface.set_verts(quads.reshape(-1, 4, 3))
    surface.set_edgecolor("none")
    surface.set_linewidth(0)
    surface.set_antialiased(False)


def move_surface(surface_data, offset):
    surface, X, Y, Z = surface_data
    set_surface_vertices(
        surface,
        X + offset[0],
        Y + offset[1],
        Z + offset[2],
    )


def limb_mesh(start, end, radius_start, radius_end):
    t = np.linspace(0, 1, 20)
    angle = np.linspace(0, 2 * np.pi, 24)
    start = np.asarray(start, dtype=float)
    direction = np.asarray(end, dtype=float) - start
    direction /= np.linalg.norm(direction)

    reference = np.array([0.0, 1.0, 0.0])
    side = np.cross(direction, reference)
    side /= np.linalg.norm(side)
    normal = np.cross(direction, side)

    centers = start + t[:, None] * (np.asarray(end) - start)
    radii = radius_start + (radius_end - radius_start) * t
    X = (
        centers[:, None, 0]
        + radii[:, None] * np.cos(angle)[None, :] * side[0]
        + radii[:, None] * np.sin(angle)[None, :] * normal[0]
    )
    Y = (
        centers[:, None, 1]
        + radii[:, None] * np.cos(angle)[None, :] * side[1]
        + radii[:, None] * np.sin(angle)[None, :] * normal[1]
    )
    Z = (
        centers[:, None, 2]
        + radii[:, None] * np.cos(angle)[None, :] * side[2]
        + radii[:, None] * np.sin(angle)[None, :] * normal[2]
    )
    return X, Y, Z


def add_limb(ax, start, end, radius_start, radius_end, color):
    X, Y, Z = limb_mesh(start, end, radius_start, radius_end)
    surface = ax.plot_surface(
        X,
        Y,
        Z,
        color=color,
        linewidth=0,
        edgecolor="none",
        antialiased=False,
        shade=True,
    )
    return surface, radius_start, radius_end


def update_limb(limb, start, end):
    surface, radius_start, radius_end = limb
    X, Y, Z = limb_mesh(start, end, radius_start, radius_end)
    set_surface_vertices(surface, X, Y, Z)


def add_meadow(ax, rng):
    count = 1400
    ground_x = rng.uniform(-2.15, 2.15, count)
    ground_y = rng.uniform(-1.55, 1.55, count)
    ground_color = rng.choice(
        ["#456b3a", "#527b40", "#3b6035", "#628449"],
        count,
    )
    ax.scatter(
        ground_x,
        ground_y,
        np.zeros_like(ground_x),
        c=ground_color,
        s=rng.uniform(3, 9, len(ground_x)),
        alpha=0.48,
        depthshade=False,
        edgecolors="none",
    )

    t = np.linspace(0, 1, 8)
    for color, count in (("#345b31", 60), ("#507c3e", 45), ("#66864a", 35)):
        x0 = rng.uniform(-2.05, 2.05, count)
        y0 = rng.uniform(-1.45, 1.45, count)
        lean_x = rng.uniform(-0.15, 0.15, count)
        lean_y = rng.uniform(-0.13, 0.13, count)
        height = rng.uniform(0.08, 0.24, count)
        X = x0[:, None] + lean_x[:, None] * t
        Y = y0[:, None] + lean_y[:, None] * t
        Z = height[:, None] * t
        separator = np.full((count, 1), np.nan)
        ax.plot(
            np.concatenate((X, separator), axis=1).ravel(),
            np.concatenate((Y, separator), axis=1).ravel(),
            np.concatenate((Z, separator), axis=1).ravel(),
            color=color,
            linewidth=0.7,
            alpha=0.68,
        )


def add_torso(ax, color):
    station = np.linspace(-0.96, 0.96, 76)
    angle = np.linspace(0, 2 * np.pi, 56)
    S, A = np.meshgrid(station, angle)
    profile = np.maximum(0.0, 1.0 - (S / 0.96) ** 2) ** 0.42
    X = S
    Y = 0.36 * profile * np.cos(A)
    Z = 1.40 + 0.39 * profile * np.sin(A) + 0.035 * S
    surface = ax.plot_surface(
        X,
        Y,
        Z,
        color=color,
        linewidth=0,
        edgecolor="none",
        antialiased=False,
        shade=True,
    )
    return surface, X, Y, Z


def add_neck(ax, color):
    t = np.linspace(0, 1, 56)
    angle = np.linspace(0, 2 * np.pi, 44)
    T, A = np.meshgrid(t, angle)
    center_x = 0.42 + 0.60 * T
    center_z = 1.44 + 0.76 * T - 0.035 * np.sin(np.pi * T)
    radius_xz = 0.31 - 0.11 * T
    radius_y = 0.25 - 0.08 * T
    X = center_x + radius_xz * np.cos(A) * 0.78
    Y = radius_y * np.sin(A)
    Z = center_z - radius_xz * np.cos(A) * 0.63
    surface = ax.plot_surface(
        X,
        Y,
        Z,
        color=color,
        linewidth=0,
        edgecolor="none",
        antialiased=False,
        shade=True,
    )
    return surface, X, Y, Z


def add_head(ax, color):
    t = np.linspace(0, 1, 48)
    angle = np.linspace(0, 2 * np.pi, 36)
    T, A = np.meshgrid(t, angle)
    center_x = 0.82 + 0.57 * T
    center_z = 2.27 - 0.47 * T
    cheek = 0.035 * np.exp(-((T - 0.42) / 0.23) ** 2)
    radius = 0.14 + cheek - 0.065 * T
    X = center_x + radius * np.cos(A) * 0.66
    Y = (0.145 - 0.06 * T) * np.sin(A)
    Z = center_z + radius * np.cos(A) * 0.75
    surface = ax.plot_surface(
        X,
        Y,
        Z,
        color=color,
        linewidth=0,
        edgecolor="none",
        antialiased=False,
        shade=True,
    )
    return surface, X, Y, Z


def add_horse(ax):
    coat = "#deded8"
    coat_light = "#f0efea"
    coat_shadow = "#d2d3d0"
    mane = "#4b4d4c"

    body_surfaces = [add_torso(ax, coat)]
    head_surfaces = [
        add_neck(ax, coat),
        add_head(ax, coat_light),
        add_ellipsoid(
            ax, (1.37, 0.0, 1.79), (0.12, 0.105, 0.075), "#c8bbb0",
            rotation=0.10,
        ),
        add_ellipsoid(ax, (0.95, -0.105, 2.39), (0.045, 0.04, 0.11), mane),
        add_ellipsoid(ax, (0.95, 0.105, 2.39), (0.045, 0.04, 0.11), mane),
    ]

    for side in (-1, 1):
        ax.scatter(
            [1.05, 1.41],
            [side * 0.135, side * 0.09],
            [2.11, 1.82],
            c=["#24140e", "#402115"],
            s=[12, 9],
            depthshade=False,
        )

    mane_t = np.linspace(0, 1, 28)
    for side in (-1, 1):
        mane_y = side * (0.19 - 0.05 * mane_t)
        mane_x = 0.24 + 0.67 * mane_t
        mane_z = 1.81 + 0.35 * mane_t + 0.018 * np.sin(10 * np.pi * mane_t)
        ax.plot(mane_x, mane_y, mane_z, color=mane, linewidth=3.0)

    leg_specs = (
        (0.53, -0.22, np.pi, False),
        (0.53, 0.22, 1.2 * np.pi, False),
        (-0.57, -0.22, 0.0, True),
        (-0.57, 0.22, 0.2 * np.pi, True),
    )
    leg_models = []
    for hip_x, hip_y, phase_offset, hind_leg in leg_specs:
        color = coat_shadow if hip_y < 0 else "#a5a8a6"
        knee_x = hip_x - 0.08 if hind_leg else hip_x + 0.04
        knee_z = 0.58
        fetlock_x = hip_x
        hoof_x = hip_x
        leg_models.append(
            {
                "hip": (hip_x, hip_y, 1.06),
                "knee": (knee_x, hip_y, knee_z),
                "fetlock": (fetlock_x, hip_y, 0.23),
                "hoof": (hoof_x, hip_y, 0.07),
                "offset": phase_offset,
                "hind": hind_leg,
                "limbs": [
                    add_limb(
                        ax,
                        (hip_x, hip_y, 1.06),
                        (knee_x, hip_y, knee_z),
                        0.105 if hind_leg else 0.09,
                        0.055,
                        color,
                    ),
                    add_limb(
                        ax,
                        (knee_x, hip_y, knee_z),
                        (fetlock_x, hip_y, 0.23),
                        0.052,
                        0.034,
                        color,
                    ),
                    add_limb(
                        ax,
                        (fetlock_x, hip_y, 0.23),
                        (hoof_x, hip_y, 0.07),
                        0.040,
                        0.030,
                        color,
                    ),
                ],
                "joints": [
                    add_ellipsoid(
                        ax, (knee_x, hip_y, knee_z),
                        (0.066, 0.060, 0.072), color,
                    ),
                    add_ellipsoid(
                        ax, (fetlock_x, hip_y, 0.23),
                        (0.046, 0.043, 0.054), color,
                    ),
                ],
                "shoe": add_ellipsoid(
                    ax,
                    (hoof_x + 0.045, hip_y, 0.045),
                    (0.12, 0.09, 0.055),
                    "#403e3a",
                ),
            }
        )

    tail_artists = [
        ax.plot([], [], [], color=mane, linewidth=2.2,
                solid_capstyle="round")[0]
        for _ in range(5)
    ]

    return body_surfaces, head_surfaces, leg_models, tail_artists


def animate_horse():
    fig = plt.figure(figsize=(10, 7), facecolor="#b9d1dc")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#b9d1dc")
    ax.set_axis_off()
    ax.set_xlim(-1.65, 1.75)
    ax.set_ylim(-1.30, 1.30)
    ax.set_zlim(-0.08, 2.72)
    ax.set_box_aspect((1.35, 1.05, 0.95))
    ax.view_init(elev=19, azim=-55)

    rng = np.random.default_rng(26)
    add_meadow(ax, rng)
    body_surfaces, head_surfaces, legs, tail = add_horse(ax)
    t = np.linspace(0, 1, 18)

    def update(frame):
        gait = 2 * np.pi * frame / 24
        body_bob = 0.055 * (1 - np.cos(2 * gait))
        head_bob = body_bob + 0.035 * np.sin(gait + 0.4)
        for surface in body_surfaces:
            move_surface(surface, (0.0, 0.0, body_bob))
        for surface in head_surfaces:
            move_surface(surface, (0.0, 0.0, head_bob))

        for leg in legs:
            hip_x, hip_y, _ = leg["hip"]
            phase = gait + leg["offset"]
            stride = 0.34 * np.cos(phase)
            lift = 0.42 * max(0.0, np.sin(phase)) ** 1.2
            if leg["hind"]:
                knee_x = hip_x - 0.10 + 0.11 * np.sin(phase)
            else:
                knee_x = hip_x + 0.03 + 0.07 * np.sin(phase - 0.3)
            ankle_x = knee_x + 0.06 + 0.10 * np.cos(phase)
            hoof_x = hip_x + stride

            points = (
                (hip_x, hip_y, 1.06 + body_bob),
                (knee_x, hip_y, 0.58 + 0.35 * lift),
                (ankle_x, hip_y, 0.23 + 0.90 * lift),
                (hoof_x, hip_y, 0.07 + lift),
            )
            leg["points"] = points
            update_limb(leg["limbs"][0], points[0], points[1])
            update_limb(leg["limbs"][1], points[1], points[2])
            update_limb(leg["limbs"][2], points[2], points[3])

            for joint, point, initial in zip(
                leg["joints"],
                points[1:3],
                (leg["knee"], leg["fetlock"]),
            ):
                move_surface(
                    joint,
                    (
                        point[0] - initial[0],
                        point[1] - initial[1],
                        point[2] - initial[2],
                    ),
                )
            hoof = points[3]
            move_surface(
                leg["shoe"],
                (hoof[0] + 0.045 - leg["hoof"][0] - 0.045,
                 0.0,
                 hoof[2] + 0.045 - leg["hoof"][2] - 0.045),
            )

        tail_sway = 0.22 * np.sin(gait / 2)
        for i, line in enumerate(tail):
            strand = 0.035 * (i - 2)
            x = -0.78 - 0.38 * t
            y = strand + tail_sway * t
            z = 1.43 - 0.75 * t - 0.05 * np.sin(np.pi * t)
            line.set_data_3d(x, y, z)

        return tuple(
            [item[0] for item in body_surfaces + head_surfaces]
            + [
                artist
                for leg in legs
                for artist in leg["limbs"] + leg["joints"] + [leg["shoe"][0]]
            ]
            + tail
        )

    animation = FuncAnimation(
        fig,
        update,
        frames=240,
        interval=35,
        blit=False,
        repeat=True,
    )
    return fig, animation


def main():
    fig, animation = animate_horse()
    plt.show()
    return fig, animation


if __name__ == "__main__":
    main()
