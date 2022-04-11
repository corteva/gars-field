import pytest
import shapely.wkt

from gars_field import GARSGrid


@pytest.mark.parametrize(
    "gars_id,long_gars_id,expected_resolution",
    [
        ("720HN2603", "720HN2603", 1),
        ("720HN26", "720HN2603", 5),
        ("720HN2", "720HN26", 15),
        ("720HN", "720HN2", 30),
        ("720HN", "720HN26", 30),
    ],
)
def test_gars(gars_id, long_gars_id, expected_resolution):
    # check resolution calc
    gg = GARSGrid(gars_id)
    assert str(gg) == gars_id
    assert gg.resolution == expected_resolution

    # check resolution forcing
    ggf = GARSGrid(long_gars_id, max_resolution=expected_resolution)
    assert str(ggf) == gars_id
    assert ggf.resolution == expected_resolution


@pytest.mark.parametrize(
    "lat,lon,resolution,expected_id",
    [
        (-89.55, -179.57, 5, "001AA23"),
        (-89.55, -179.57, 15, "001AA2"),
        (-89.55, -179.57, 30, "001AA"),
        (-90, -179, 5, "003AA37"),
        (89, -180, 5, "001QY37"),
        (-90, 179.55, 5, "720AA37"),
        (-90, 179, 5, "719AA37"),
        (-90.005, 179.9, 5, "720QZ22"),
        (0.303, 179.9, 5, "720HN28"),
        (0.4083333333333334, 179.975, 1, "720HN2604"),
    ],
)
def test_gars_from_latlon(lat, lon, resolution, expected_id):
    assert str(GARSGrid.from_latlon(lat, lon, resolution=resolution)) == expected_id


@pytest.mark.parametrize(
    "gars_id, expected_polygon",
    [
        (
            "720HN2604",
            "POLYGON ((179.9833333333333 0.4, "
            "179.9833333333333 0.4166666666666667, "
            "179.9666666666667 0.4166666666666667, "
            "179.9666666666667 0.4, "
            "179.9833333333333 0.4))",
        ),
        (
            "720HN26",
            "POLYGON ((180 0.3333333333333333, 180 0.4166666666666666, "
            "179.9166666666667 0.4166666666666666, "
            "179.9166666666667 0.3333333333333333, "
            "180 0.3333333333333333))",
        ),
        ("720HN2", "POLYGON ((180 0.25, 180 0.5, 179.75 0.5, 179.75 0.25, 180 0.25))"),
        ("720HN", "POLYGON ((180 0, 180 0.5, 179.5 0.5, 179.5 0, 180 0))"),
    ],
)
def test_gars_polygon(gars_id, expected_polygon):
    assert GARSGrid(gars_id).polygon.equals_exact(
        shapely.wkt.loads(expected_polygon), tolerance=0.5 * 10**-12
    )


@pytest.mark.parametrize(
    "gars_id, expected_utm_epsg",
    [
        ("720HN2604", "EPSG:32660"),
        ("250GN26", "EPSG:32721"),
        ("001HN2", "EPSG:32601"),
        ("004BA", "EPSG:32701"),
        ("020AB", "EPSG:32761"),
        ("045QZ", "EPSG:32661"),
    ],
)
def test_gars_utm_epsg(gars_id, expected_utm_epsg):
    assert str(GARSGrid(gars_id).utm_epsg) == expected_utm_epsg


@pytest.mark.parametrize(
    "invalid_gars_id",
    [
        "720HN96",
        "720IN16",
        "720HO16",
        "720RS16",
        "720AI16",
        "720HN10",
        "720HN01",
        "720HN111",
        "H720HN1",
        "721QY",
        "720HN1126",
        "720HN11251",
    ],
)
def test_gars_to_polygon__invalid_id(invalid_gars_id):
    with pytest.raises(ValueError):
        GARSGrid(invalid_gars_id)
