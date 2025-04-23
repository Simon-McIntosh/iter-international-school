"""Access MAST shot data from object store."""

from dataclasses import dataclass, field
from operator import attrgetter
from functools import cached_property

import fsspec
import numpy as np
import pandas as pd
import xarray as xr
import zarr


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
        return zarr.storage.FSStore(fs=self.filesystem, url=self.url)

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
