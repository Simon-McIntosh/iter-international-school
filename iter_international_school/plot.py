"""Manage common ploting routines."""

import matplotlib.pylab as plt

import iter_international_school.mast


def flux_map(magnetic_flux, axes=None, levels=51, shot_id=30420, **kwargs):
    """Plot flux map and return contour levels and axes instance."""
    if axes is None:
        axes = plt.subplots()[1]
        axes.set_aspect("equal")
        axes.set_axis_off()
    kwargs = {"linestyles": "-", "colors": "gray"} | kwargs
    try:
        flux_grid = magnetic_flux.major_radius, magnetic_flux.z
    except AttributeError:
        equilibrium = iter_international_school.mast.Shot(shot_id)[
            "equilibrium"
        ]  # read grid from a shot instance
        flux_grid = equilibrium.major_radius, equilibrium.z
    levels = axes.contour(
        *flux_grid,
        magnetic_flux,
        levels=levels,
        **kwargs,
    ).levels
    return levels, axes
