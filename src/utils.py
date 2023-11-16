import os
from pathlib import Path

import xarray as xr

DATA_DIR = Path(os.getenv("AA_DATA_DIR"))
PUB_RAW_DIR = DATA_DIR / "public" / "raw" / "bdi"
CODAB_DIR = PUB_RAW_DIR / "cod_ab"
PRI_RAW_DIR = DATA_DIR / "private" / "raw" / "bdi"
LAKE_DIR = PRI_RAW_DIR / "c3s"


def load_lake_level():
    filename = (
        "C3S_LWL_S-AFRICA_TANGANIKA_altimetry_"
        "4.0_19921017_20221229_R20230126.nc"
    )
    ds = xr.load_dataset(LAKE_DIR / filename)
    return ds
