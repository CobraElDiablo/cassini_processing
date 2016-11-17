from isis3._core import isis_command
import os

def spiceinit(from_cube, is_ringplane=False):
    shape = "ringplane" if is_ringplane else "system"
    s = isis_command("spiceinit", {"from": from_cube, "shape": shape})
    return s


def cam2map(from_cube, to_cube, projection="equirectangular", map=None, resolution="CAMERA"):

    if map is None:
        map = "%s/../data/base/templates/maps/%s.map"%(os.environ["ISISROOT"], projection)

    params = {
        "from": from_cube,
        "to": to_cube,
        "map": map
    }

    if resolution == "MAP":
        params["pixres"] = "map"

    s = isis_command("cam2map", params)
    return s