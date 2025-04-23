"""Access MAST shot data from object store."""

from dataclasses import dataclass, field
from operator import attrgetter
from functools import cached_property

import fsspec
import numpy as np
import pandas as pd
import xarray as xr
import zarr.storage


@dataclass
class Shot:
    """Methods to manage access to fair-mast data store."""

    shot_id: int
    endpoint_url: str = "https://s3.echo.stfc.ac.uk"
    storage_options: dict = field(default_factory=dict)

    def __getitem__(self, group: str):
        """Return group from object store."""
        return xr.open_zarr(self.store, group=group)

    @property
    def url(self) -> str:
        """Return store url."""
        return f"s3://mast/test/level2/shots/{self.shot_id}.zarr"

    @cached_property
    def filesystem(self):
        """Return fsspec filesystem instance."""
        return fsspec.filesystem(
            **dict(
                protocol="simplecache",
                target_protocol="s3",
                target_options=dict(anon=True, endpoint_url=self.endpoint_url),
            )
            | self.storage_options
        )

    @cached_property
    def store(self):
        """Return zarr object store."""
        return zarr.storage.FStore(fs=self.filesystem, url=self.url)

    def to_dask(self, group: str, channel: str, dropna=True):
        """Return dask array from zarr store."""
        array = attrgetter(channel)(self[group]).transpose("time", ...)
        if dropna:
            return array.dropna("time")
        return array

    def to_pandas(
        self,
        group: str,
        channels: str | list[str],
        time: np.ndarray | None = None,
        multi_index=False,
    ) -> pd.DataFrame:
        """Return channel list as a pandas DataFrame."""
        dataset = self[group]
        if isinstance(channels, str):
            channels = [channels]
        attrs = []
        for channel in channels:
            attr = attrgetter(channel)(dataset).transpose("time", ...)
            if time is not None:
                attr = attr.interp({"time": time})
            dataframe = attr.to_pandas()
            if isinstance(dataframe, pd.Series):
                dataframe = dataframe.to_frame()
            if multi_index:
                dataframe.columns = pd.MultiIndex.from_product(
                    [dataframe.columns, [attr.units], [channel]],
                    names=("name", "unit", "diagnostic_group"),
                )
            attrs.append(dataframe)
        return pd.concat(attrs, axis=1)


if __name__ == "__main__":
    # Create a Shot instance
    shot = Shot(shot_id=29034)

    # Example 1: Access a group using __getitem__
    print("Example 1: Accessing a group")
    try:
        # Replace 'bolometer' with an actual group name available in your data
        bolometer = shot["bolometer"]
        print(f"Accessed group 'bolometer' with coordinates: {list(bolometer.coords)}")
    except Exception as e:
        print(f"Could not access group: {e}")

    # Example 2: Convert data to a dask array
    print("\nExample 2: Converting to dask array")
    try:
        # Replace with actual group and channel names
        dask_array = shot.to_dask(group="magnetics", channel="ipla")
        print(f"Dask array shape: {dask_array.shape}")
        print(f"Dask array chunks: {dask_array.chunks}")
    except Exception as e:
        print(f"Could not convert to dask array: {e}")

    # Example 3: Convert data to pandas DataFrame
    print("\nExample 3: Converting to pandas DataFrame")
    try:
        # Single channel example
        df_single = shot.to_pandas(group="magnetics", channels="ipla")
        print("Single channel DataFrame head:")
        print(df_single.head())

        # Multiple channels example
        df_multi = shot.to_pandas(
            group="magnetics",
            channels=["ipla", "bvac"],  # Replace with actual channel names
            multi_index=True,
        )
        print("\nMultiple channels DataFrame with multi-index head:")
        print(df_multi.head())
    except Exception as e:
        print(f"Could not convert to pandas DataFrame: {e}")

    # Example 4: Interpolating to specific time points
    print("\nExample 4: Interpolating to specific time points")
    try:
        import numpy as np

        # Create a custom time array
        custom_time = np.linspace(0.1, 0.5, 10)  # Replace with appropriate time range

        df_interp = shot.to_pandas(group="magnetics", channels="ipla", time=custom_time)
        print("Interpolated DataFrame head:")
        print(df_interp.head())
    except Exception as e:
        print(f"Could not interpolate: {e}")
