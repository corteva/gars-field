import pytest

from gars_field import GEDGARSGrid


@pytest.mark.parametrize(
    "gars_id,long_gars_id,expected_resolution",
    [("GD2B2", "GD2B2", 30), ("GD2B", "GD2B2", 60), ("GD2B", "GD2B", 60)],
)
def test_garsgd(gars_id, long_gars_id, expected_resolution):
    # check resolution calc
    gg = GEDGARSGrid(gars_id)
    assert str(gg) == gars_id
    assert gg.resolution == expected_resolution

    # check resolution forcing
    ggf = GEDGARSGrid(long_gars_id, max_resolution=expected_resolution)
    assert str(ggf) == gars_id
    assert ggf.resolution == expected_resolution


@pytest.mark.parametrize(
    "lat,lon,resolution,expected_id",
    [
        (-89.55, -179.57, 30, "GD1A3"),
        (-89.55, -179.57, 60, "GD1A"),
        (-90, -179, 30, "GD1A3"),
        (89, -180, 60, "GD1C"),
        (-90, 179.55, 30, "GD6A4"),
        (-90, 179, 60, "GD6A"),
        (0.005, 179.9, 30, "GD6B2"),
        (0.303, 179.9, 30, "GD6B2"),
    ],
)
def test_garsd_from_latlon(lat, lon, resolution, expected_id):
    assert str(GEDGARSGrid.from_latlon(lat, lon, resolution=resolution)) == expected_id


@pytest.mark.parametrize(
    "gars_id, expected_polygon",
    [
        ("GD2B2", "POLYGON ((-60 0, -60 30, -90 30, -90 0, -60 0))"),
        ("GD2B", "POLYGON ((-60 -30, -60 30, -120 30, -120 -30, -60 -30))"),
    ],
)
def test_garsd_polygon(gars_id, expected_polygon):
    assert str(GEDGARSGrid(gars_id).polygon) == expected_polygon


@pytest.mark.parametrize(
    "invalid_gars_id", ["720HN96", "D20BN26", "GD02F2", "GD8A6", "GD2B999"]
)
def test_garsd_to_polygon__invalid_id(invalid_gars_id):
    with pytest.raises(ValueError):
        GEDGARSGrid(invalid_gars_id)


def test_garsd_utm_epsg():
    assert GEDGARSGrid("GD2B").utm_epsg is None
