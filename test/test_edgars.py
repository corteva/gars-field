import pytest

from gars_field import EDGARSGrid


@pytest.mark.parametrize(
    "gars_id,long_gars_id,expected_resolution",
    [
        ("D20BJ26", "D20BJ26", 1),
        ("D20BJ2", "D20BJ26", 3),
        ("D20BJ", "D20BJ2", 6),
        ("D20BJ", "D20BJ26", 6),
    ],
)
def test_garsd(gars_id, long_gars_id, expected_resolution):
    # check resolution calc
    gg = EDGARSGrid(gars_id)
    assert str(gg) == gars_id
    assert gg.resolution == expected_resolution

    # check resolution forcing
    ggf = EDGARSGrid(long_gars_id, max_resolution=expected_resolution)
    assert str(ggf) == gars_id
    assert ggf.resolution == expected_resolution


@pytest.mark.parametrize(
    "lat,lon,resolution,expected_id",
    [
        (-89.55, -179.57, 1, "D01AA37"),
        (-89.55, -179.57, 3, "D01AA3"),
        (-89.55, -179.57, 6, "D01AA"),
        (-90, -179, 1, "D01AA38"),
        (89, -180, 3, "D01BK1"),
        (-90, 179.55, 1, "D60AA49"),
        (-90, 179, 1, "D60AA49"),
        (0.005, 179.9, 1, "D60AR49"),
        (0.303, 179.9, 1, "D60AR49"),
    ],
)
def test_garsd_from_latlon(lat, lon, resolution, expected_id):
    assert str(EDGARSGrid.from_latlon(lat, lon, resolution=resolution)) == expected_id


@pytest.mark.parametrize(
    "gars_id, expected_polygon",
    [
        ("D20BJ26", "POLYGON ((-60 82, -60 83, -61 83, -61 82, -60 82))"),
        ("D20BJ2", "POLYGON ((-60 81, -60 84, -63 84, -63 81, -60 81))"),
        ("D20BJ", "POLYGON ((-60 78, -60 84, -66 84, -66 78, -60 78))"),
    ],
)
def test_garsd_polygon(gars_id, expected_polygon):
    assert str(EDGARSGrid(gars_id).polygon) == expected_polygon


@pytest.mark.parametrize(
    "invalid_gars_id", ["720HN96", "D20BN26", "D80AB26", "D20BJ999"]
)
def test_garsd_to_polygon__invalid_id(invalid_gars_id):
    with pytest.raises(ValueError):
        EDGARSGrid(invalid_gars_id)


@pytest.mark.parametrize(
    "gars_id, expected_utm_epsg",
    [
        ("D60AG26", "EPSG:32760"),
        ("D21AC2", "EPSG:32721"),
        ("D04BA", "EPSG:32604"),
        ("D20AB", "EPSG:32761"),
        ("D45BK", "EPSG:32661"),
    ],
)
def test_garsd_utm_epsg(gars_id, expected_utm_epsg):
    assert str(EDGARSGrid(gars_id).utm_epsg) == expected_utm_epsg
