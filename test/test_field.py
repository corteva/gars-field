import pytest
import shapely.geometry
import shapely.wkt

from gars_field import GARSField, GARSGrid, GEDGARSGrid


def box_latlon(minx, miny, maxx, maxy):
    """When generating a box shape in geographic coordinates, it does not account for the
    -180/180 dateline.

    This function is meant to account for that.


    Parameters
    ----------
    minx, miny, maxx, maxy: float
        Bounding coordinates geographic coordinates.

    Returns
    -------
    shapely.geometry.Polygon or shapely.geometry.Multipolygon

    """
    # check if bounds go over -180/180 line
    if maxx < minx <= 180:
        return shapely.geometry.MultiPolygon(
            [
                shapely.geometry.box(minx, miny, 180, maxy),
                shapely.geometry.box(-180, miny, maxx, maxy),
            ]
        )
    return shapely.geometry.box(minx, miny, maxx, maxy)


def assert_gars_expected(field: GARSField, resolution, expected):
    for _ in range(2):
        # repeat to ensure cached geometry is the same
        assert [str(gg) for gg in getattr(field, f"gars_{resolution}")] == expected


MULTI_POLY = shapely.wkt.loads(
    "MULTIPOLYGON (((-179.9999999 -81.96439234540721, "
    "-179.4398378760588 -81.96439234540721, "
    "-179.4398378760588 -83.03189537565682, "
    "-179.9999999 -83.03189537565682, "
    "-179.9999999 -81.96439234540721)), "
    "((179.9999999 -83.03189537565682, "
    "179.999996136815 -83.03189537565682, "
    "179.999996136815 -81.96439234540721, "
    "179.9999999 -81.96439234540721, "
    "179.9999999 -83.03189537565682)))"
)

MULTI_POLY_DUPLICATE = shapely.wkt.loads(
    "MULTIPOLYGON (((-179.9999999 -81.96439234540721, "
    "-179.4398378760588 -81.96439234540721, "
    "-179.4398378760588 -83.03189537565682, "
    "-179.9999999 -83.03189537565682, "
    "-179.9999999 -81.96439234540721)), "
    "((-179.9999999 -81.96439234540721, "
    "-179.4398378760588 -81.96439234540721, "
    "-179.4398378760588 -83.03189537565682, "
    "-179.9999999 -83.03189537565682, "
    "-179.9999999 -81.96439234540721)))"
)


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        # check going across longitude zones
        (shapely.geometry.box(minx=-175, miny=-76, maxx=-150, maxy=-75), ["GD1A"]),
        # check for going across latitude zones
        (shapely.geometry.box(minx=-175, miny=-86, maxx=-174.5, maxy=-50), ["GD1A"]),
        # check for 180 edge case
        (shapely.geometry.box(minx=179, miny=89, maxx=180, maxy=90), ["GD6C"]),
        # check for dateline case
        (box_latlon(minx=179.5, miny=7, maxx=-179.6, maxy=8), ["GD1B", "GD6B"]),
    ],
)
def test_gars_field__gars_60deg(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "60deg", expected)


@pytest.mark.parametrize(
    "multi_poly, expected",
    [
        (MULTI_POLY, ["GD1A", "GD6A"]),
        (MULTI_POLY_DUPLICATE, ["GD1A"]),
    ],
)
def test_gars_field__gars_60deg_multipoly(multi_poly, expected):
    garsf = GARSField(multi_poly)
    assert_gars_expected(garsf, "60deg", expected)


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        # check going across longitude zones
        (
            shapely.geometry.box(minx=-175, miny=-76, maxx=-150, maxy=-75),
            ["GD1A3", "GD1A4"],
        ),
        # check for going across latitude zones
        (
            shapely.geometry.box(minx=-175, miny=-86, maxx=-174.5, maxy=-50),
            ["GD1A1", "GD1A3"],
        ),
        # check for 180 edge case
        (shapely.geometry.box(minx=179, miny=89, maxx=180, maxy=90), ["GD6C2"]),
        # check for dateline case
        (box_latlon(minx=179.5, miny=7, maxx=-179.6, maxy=8), ["GD1B1", "GD6B2"]),
    ],
)
def test_gars_field__gars_30deg(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "30deg", expected)


@pytest.mark.parametrize(
    "multi_poly, expected",
    [
        (MULTI_POLY, ["GD1A3", "GD6A4"]),
        (MULTI_POLY_DUPLICATE, ["GD1A3"]),
    ],
)
def test_gars_field__gars_30deg_multipoly(multi_poly, expected):
    garsf = GARSField(multi_poly)
    assert_gars_expected(garsf, "30deg", expected)


def test_gars_field_gars_30deg__check_all_4():
    gars5 = GARSField(GEDGARSGrid("GD1A").polygon.buffer(-0.0001))
    for _ in range(2):
        # repeat to ensure cached geometry is the same
        assert len(gars5.gars_60deg) == 1
        assert len(gars5.gars_30deg) == 4


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        # check going across longitude zones
        (
            shapely.geometry.box(minx=-175, miny=-76, maxx=-150, maxy=-75),
            ["D01AC", "D02AC", "D03AC", "D04AC", "D05AC", "D06AC"],
        ),
        # check for going across latitude zones
        (
            shapely.geometry.box(minx=-175, miny=-86, maxx=-174.5, maxy=-50),
            ["D01AA", "D01AB", "D01AC", "D01AD", "D01AE", "D01AF", "D01AG"],
        ),
        # check for 180 edge case
        (shapely.geometry.box(minx=179, miny=89, maxx=180, maxy=90), ["D60BK"]),
        # check for dateline case
        (box_latlon(minx=179.5, miny=7, maxx=-179.6, maxy=8), ["D01AS", "D60AS"]),
    ],
)
def test_gars_field__gars_6deg(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "6deg", expected)


@pytest.mark.parametrize(
    "multi_poly, expected",
    [
        (MULTI_POLY, ["D01AB", "D60AB"]),
        (MULTI_POLY_DUPLICATE, ["D01AB"]),
    ],
)
def test_gars_field__gars_6deg_multipoly(multi_poly, expected):
    garsf = GARSField(multi_poly)
    assert_gars_expected(garsf, "6deg", expected)


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        # check going across longitude zones
        (
            shapely.geometry.box(minx=-175, miny=-76, maxx=-169, maxy=-75),
            ["D01AC2", "D01AC4", "D02AC1", "D02AC2", "D02AC3", "D02AC4"],
        ),
        # check for going across latitude zones
        (
            shapely.geometry.box(minx=-175, miny=-86, maxx=-174.5, maxy=-70),
            ["D01AA2", "D01AB2", "D01AB4", "D01AC2", "D01AC4", "D01AD4"],
        ),
        # check for 180 edge case
        (shapely.geometry.box(minx=179, miny=89, maxx=180, maxy=90), ["D60BK2"]),
        # check for dateline case
        (box_latlon(minx=179.5, miny=7, maxx=-179.6, maxy=8), ["D01AS3", "D60AS4"]),
    ],
)
def test_gars_field__gars_3deg(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "3deg", expected)


@pytest.mark.parametrize(
    "multi_poly, expected",
    [
        (MULTI_POLY, ["D01AB3", "D60AB4"]),
        (MULTI_POLY_DUPLICATE, ["D01AB3"]),
    ],
)
def test_gars_field__gars_3deg_multipoly(multi_poly, expected):
    garsf = GARSField(multi_poly)
    assert_gars_expected(garsf, "3deg", expected)


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        # check going across longitude zones
        (
            shapely.geometry.box(minx=-175, miny=-76, maxx=-173, maxy=-75),
            [
                "D01AC28",
                "D01AC29",
                "D01AC42",
                "D01AC43",
                "D01AC45",
                "D01AC46",
                "D02AC17",
                "D02AC18",
                "D02AC31",
                "D02AC32",
                "D02AC34",
                "D02AC35",
            ],
        ),
        # check for going across latitude zones
        (
            shapely.geometry.box(minx=-175, miny=-86, maxx=-174.5, maxy=-84),
            [
                "D01AA22",
                "D01AA23",
                "D01AA25",
                "D01AA26",
                "D01AA28",
                "D01AA29",
                "D01AB48",
                "D01AB49",
            ],
        ),
        # check for 180 edge case
        (
            shapely.geometry.box(minx=179, miny=89, maxx=180, maxy=90),
            ["D60BK22", "D60BK23", "D60BK25", "D60BK26"],
        ),
        # check for dateline case
        (
            box_latlon(minx=179.5, miny=7, maxx=-179.6, maxy=8),
            ["D01AS31", "D01AS34", "D01AS37", "D60AS43", "D60AS46", "D60AS49"],
        ),
    ],
)
def test_gars_field__gars_1deg(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "1deg", expected)


@pytest.mark.parametrize(
    "multi_poly, expected",
    [
        (
            MULTI_POLY,
            [
                "D01AB31",
                "D01AB34",
                "D01AB37",
                "D60AB43",
                "D60AB46",
                "D60AB49",
            ],
        ),
        (MULTI_POLY_DUPLICATE, ["D01AB31", "D01AB34", "D01AB37"]),
    ],
)
def test_gars_field__gars_1deg_multipoly(multi_poly, expected):
    garsf = GARSField(multi_poly)
    assert_gars_expected(garsf, "1deg", expected)


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        # check going across longitude zones
        (
            shapely.geometry.box(minx=-175, miny=-76, maxx=-170, maxy=-75),
            [
                "011BE",
                "011BF",
                "011BG",
                "012BE",
                "012BF",
                "012BG",
                "013BE",
                "013BF",
                "013BG",
                "014BE",
                "014BF",
                "014BG",
                "015BE",
                "015BF",
                "015BG",
                "016BE",
                "016BF",
                "016BG",
                "017BE",
                "017BF",
                "017BG",
                "018BE",
                "018BF",
                "018BG",
                "019BE",
                "019BF",
                "019BG",
                "020BE",
                "020BF",
                "020BG",
                "021BE",
                "021BF",
                "021BG",
            ],
        ),
        # check for going across latitude zones
        (
            shapely.geometry.box(minx=-175, miny=-86, maxx=-174.5, maxy=-70),
            [
                "011AJ",
                "011AK",
                "011AL",
                "011AM",
                "011AN",
                "011AP",
                "011AQ",
                "011AR",
                "011AS",
                "011AT",
                "011AU",
                "011AV",
                "011AW",
                "011AX",
                "011AY",
                "011AZ",
                "011BA",
                "011BB",
                "011BC",
                "011BD",
                "011BE",
                "011BF",
                "011BG",
                "011BH",
                "011BJ",
                "011BK",
                "011BL",
                "011BM",
                "011BN",
                "011BP",
                "011BQ",
                "011BR",
                "011BS",
                "012AJ",
                "012AK",
                "012AL",
                "012AM",
                "012AN",
                "012AP",
                "012AQ",
                "012AR",
                "012AS",
                "012AT",
                "012AU",
                "012AV",
                "012AW",
                "012AX",
                "012AY",
                "012AZ",
                "012BA",
                "012BB",
                "012BC",
                "012BD",
                "012BE",
                "012BF",
                "012BG",
                "012BH",
                "012BJ",
                "012BK",
                "012BL",
                "012BM",
                "012BN",
                "012BP",
                "012BQ",
                "012BR",
                "012BS",
            ],
        ),
        # check for 180 edge case
        (
            shapely.geometry.box(minx=179, miny=89, maxx=180, maxy=90),
            ["719QY", "719QZ", "720QY", "720QZ"],
        ),
        # check for dateline case
        (
            box_latlon(minx=179.5, miny=7, maxx=-179.6, maxy=8),
            ["001JC", "001JD", "001JE", "720JC", "720JD", "720JE"],
        ),
    ],
)
def test_gars_field__gars_30min(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "30min", expected)


@pytest.mark.parametrize(
    "multi_poly, expected",
    [
        (
            MULTI_POLY,
            [
                "001AP",
                "001AQ",
                "001AR",
                "001AS",
                "002AP",
                "002AQ",
                "002AR",
                "002AS",
                "720AP",
                "720AQ",
                "720AR",
                "720AS",
            ],
        ),
        (
            MULTI_POLY_DUPLICATE,
            [
                "001AP",
                "001AQ",
                "001AR",
                "001AS",
                "002AP",
                "002AQ",
                "002AR",
                "002AS",
            ],
        ),
    ],
)
def test_gars_field__gars_30min_multipoly(multi_poly, expected):
    garsf = GARSField(multi_poly)
    assert_gars_expected(garsf, "30min", expected)


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        (
            shapely.geometry.box(minx=-175, miny=-76, maxx=-174, maxy=-75),
            [
                "011BE1",
                "011BE2",
                "011BE3",
                "011BE4",
                "011BF1",
                "011BF2",
                "011BF3",
                "011BF4",
                "011BG3",
                "011BG4",
                "012BE1",
                "012BE2",
                "012BE3",
                "012BE4",
                "012BF1",
                "012BF2",
                "012BF3",
                "012BF4",
                "012BG3",
                "012BG4",
                "013BE1",
                "013BE3",
                "013BF1",
                "013BF3",
                "013BG3",
            ],
        ),
        (
            shapely.geometry.box(minx=-175, miny=-86, maxx=-174.9, maxy=-70),
            [
                "011AJ1",
                "011AJ3",
                "011AK1",
                "011AK3",
                "011AL1",
                "011AL3",
                "011AM1",
                "011AM3",
                "011AN1",
                "011AN3",
                "011AP1",
                "011AP3",
                "011AQ1",
                "011AQ3",
                "011AR1",
                "011AR3",
                "011AS1",
                "011AS3",
                "011AT1",
                "011AT3",
                "011AU1",
                "011AU3",
                "011AV1",
                "011AV3",
                "011AW1",
                "011AW3",
                "011AX1",
                "011AX3",
                "011AY1",
                "011AY3",
                "011AZ1",
                "011AZ3",
                "011BA1",
                "011BA3",
                "011BB1",
                "011BB3",
                "011BC1",
                "011BC3",
                "011BD1",
                "011BD3",
                "011BE1",
                "011BE3",
                "011BF1",
                "011BF3",
                "011BG1",
                "011BG3",
                "011BH1",
                "011BH3",
                "011BJ1",
                "011BJ3",
                "011BK1",
                "011BK3",
                "011BL1",
                "011BL3",
                "011BM1",
                "011BM3",
                "011BN1",
                "011BN3",
                "011BP1",
                "011BP3",
                "011BQ1",
                "011BQ3",
                "011BR1",
                "011BR3",
                "011BS3",
            ],
        ),
    ],
)
def test_gars_field__gars_15min(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "15min", expected)


@pytest.mark.parametrize(
    "multi_poly, expected",
    [
        (
            MULTI_POLY,
            [
                "001AP1",
                "001AP2",
                "001AQ1",
                "001AQ2",
                "001AQ3",
                "001AQ4",
                "001AR1",
                "001AR2",
                "001AR3",
                "001AR4",
                "001AS3",
                "001AS4",
                "002AP1",
                "002AQ1",
                "002AQ3",
                "002AR1",
                "002AR3",
                "002AS3",
                "720AP2",
                "720AQ2",
                "720AQ4",
                "720AR2",
                "720AR4",
                "720AS4",
            ],
        ),
        (
            MULTI_POLY_DUPLICATE,
            [
                "001AP1",
                "001AP2",
                "001AQ1",
                "001AQ2",
                "001AQ3",
                "001AQ4",
                "001AR1",
                "001AR2",
                "001AR3",
                "001AR4",
                "001AS3",
                "001AS4",
                "002AP1",
                "002AQ1",
                "002AQ3",
                "002AR1",
                "002AR3",
                "002AS3",
            ],
        ),
    ],
)
def test_gars_field__gars_15min_multipoly(multi_poly, expected):
    garsf = GARSField(multi_poly)
    assert_gars_expected(garsf, "15min", expected)


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        (
            shapely.geometry.box(minx=-175, miny=-76, maxx=-174.5, maxy=-75.5),
            [
                "011BE11",
                "011BE12",
                "011BE13",
                "011BE14",
                "011BE15",
                "011BE16",
                "011BE17",
                "011BE18",
                "011BE19",
                "011BE21",
                "011BE22",
                "011BE23",
                "011BE24",
                "011BE25",
                "011BE26",
                "011BE27",
                "011BE28",
                "011BE29",
                "011BE31",
                "011BE32",
                "011BE33",
                "011BE34",
                "011BE35",
                "011BE36",
                "011BE37",
                "011BE38",
                "011BE39",
                "011BE41",
                "011BE42",
                "011BE43",
                "011BE44",
                "011BE45",
                "011BE46",
                "011BE47",
                "011BE48",
                "011BE49",
                "011BF37",
                "011BF38",
                "011BF39",
                "011BF47",
                "011BF48",
                "011BF49",
                "012BE11",
                "012BE14",
                "012BE17",
                "012BE31",
                "012BE34",
                "012BE37",
                "012BF37",
            ],
        ),
        (
            shapely.geometry.box(minx=-175, miny=-80, maxx=-174.9, maxy=-78),
            [
                "011AW11",
                "011AW12",
                "011AW14",
                "011AW15",
                "011AW17",
                "011AW18",
                "011AW31",
                "011AW32",
                "011AW34",
                "011AW35",
                "011AW37",
                "011AW38",
                "011AX11",
                "011AX12",
                "011AX14",
                "011AX15",
                "011AX17",
                "011AX18",
                "011AX31",
                "011AX32",
                "011AX34",
                "011AX35",
                "011AX37",
                "011AX38",
                "011AY11",
                "011AY12",
                "011AY14",
                "011AY15",
                "011AY17",
                "011AY18",
                "011AY31",
                "011AY32",
                "011AY34",
                "011AY35",
                "011AY37",
                "011AY38",
                "011AZ11",
                "011AZ12",
                "011AZ14",
                "011AZ15",
                "011AZ17",
                "011AZ18",
                "011AZ31",
                "011AZ32",
                "011AZ34",
                "011AZ35",
                "011AZ37",
                "011AZ38",
                "011BA37",
                "011BA38",
            ],
        ),
    ],
)
def test_gars_field__gars_5min(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "5min", expected)


@pytest.mark.parametrize(
    "multi_poly, expected",
    [
        (
            MULTI_POLY,
            [
                "001AP11",
                "001AP12",
                "001AP13",
                "001AP21",
                "001AP22",
                "001AP23",
                "001AQ11",
                "001AQ12",
                "001AQ13",
                "001AQ14",
                "001AQ15",
                "001AQ16",
                "001AQ17",
                "001AQ18",
                "001AQ19",
                "001AQ21",
                "001AQ22",
                "001AQ23",
                "001AQ24",
                "001AQ25",
                "001AQ26",
                "001AQ27",
                "001AQ28",
                "001AQ29",
                "001AQ31",
                "001AQ32",
                "001AQ33",
                "001AQ34",
                "001AQ35",
                "001AQ36",
                "001AQ37",
                "001AQ38",
                "001AQ39",
                "001AQ41",
                "001AQ42",
                "001AQ43",
                "001AQ44",
                "001AQ45",
                "001AQ46",
                "001AQ47",
                "001AQ48",
                "001AQ49",
                "001AR11",
                "001AR12",
                "001AR13",
                "001AR14",
                "001AR15",
                "001AR16",
                "001AR17",
                "001AR18",
                "001AR19",
                "001AR21",
                "001AR22",
                "001AR23",
                "001AR24",
                "001AR25",
                "001AR26",
                "001AR27",
                "001AR28",
                "001AR29",
                "001AR31",
                "001AR32",
                "001AR33",
                "001AR34",
                "001AR35",
                "001AR36",
                "001AR37",
                "001AR38",
                "001AR39",
                "001AR41",
                "001AR42",
                "001AR43",
                "001AR44",
                "001AR45",
                "001AR46",
                "001AR47",
                "001AR48",
                "001AR49",
                "001AS37",
                "001AS38",
                "001AS39",
                "001AS47",
                "001AS48",
                "001AS49",
                "002AP11",
                "002AQ11",
                "002AQ14",
                "002AQ17",
                "002AQ31",
                "002AQ34",
                "002AQ37",
                "002AR11",
                "002AR14",
                "002AR17",
                "002AR31",
                "002AR34",
                "002AR37",
                "002AS37",
                "720AP23",
                "720AQ23",
                "720AQ26",
                "720AQ29",
                "720AQ43",
                "720AQ46",
                "720AQ49",
                "720AR23",
                "720AR26",
                "720AR29",
                "720AR43",
                "720AR46",
                "720AR49",
                "720AS49",
            ],
        ),
        (
            MULTI_POLY_DUPLICATE,
            [
                "001AP11",
                "001AP12",
                "001AP13",
                "001AP21",
                "001AP22",
                "001AP23",
                "001AQ11",
                "001AQ12",
                "001AQ13",
                "001AQ14",
                "001AQ15",
                "001AQ16",
                "001AQ17",
                "001AQ18",
                "001AQ19",
                "001AQ21",
                "001AQ22",
                "001AQ23",
                "001AQ24",
                "001AQ25",
                "001AQ26",
                "001AQ27",
                "001AQ28",
                "001AQ29",
                "001AQ31",
                "001AQ32",
                "001AQ33",
                "001AQ34",
                "001AQ35",
                "001AQ36",
                "001AQ37",
                "001AQ38",
                "001AQ39",
                "001AQ41",
                "001AQ42",
                "001AQ43",
                "001AQ44",
                "001AQ45",
                "001AQ46",
                "001AQ47",
                "001AQ48",
                "001AQ49",
                "001AR11",
                "001AR12",
                "001AR13",
                "001AR14",
                "001AR15",
                "001AR16",
                "001AR17",
                "001AR18",
                "001AR19",
                "001AR21",
                "001AR22",
                "001AR23",
                "001AR24",
                "001AR25",
                "001AR26",
                "001AR27",
                "001AR28",
                "001AR29",
                "001AR31",
                "001AR32",
                "001AR33",
                "001AR34",
                "001AR35",
                "001AR36",
                "001AR37",
                "001AR38",
                "001AR39",
                "001AR41",
                "001AR42",
                "001AR43",
                "001AR44",
                "001AR45",
                "001AR46",
                "001AR47",
                "001AR48",
                "001AR49",
                "001AS37",
                "001AS38",
                "001AS39",
                "001AS47",
                "001AS48",
                "001AS49",
                "002AP11",
                "002AQ11",
                "002AQ14",
                "002AQ17",
                "002AQ31",
                "002AQ34",
                "002AQ37",
                "002AR11",
                "002AR14",
                "002AR17",
                "002AR31",
                "002AR34",
                "002AR37",
                "002AS37",
            ],
        ),
    ],
)
def test_gars_field__gars_5min_multipoly(multi_poly, expected):
    garsf = GARSField(multi_poly)
    assert_gars_expected(garsf, "5min", expected)


@pytest.mark.parametrize(
    "geom_bounds,expected",
    [
        (
            shapely.geometry.box(minx=-175, miny=-76, maxx=-174.97, maxy=-75.97),
            ["011BE3716", "011BE3717", "011BE3721", "011BE3722"],
        ),
        (
            shapely.geometry.box(minx=-175, miny=-80, maxx=-174.97, maxy=-79.97),
            ["011AW3716", "011AW3717", "011AW3721", "011AW3722"],
        ),
    ],
)
def test_gars_field__gars_1min(geom_bounds, expected):
    garsf = GARSField(geom_bounds)
    assert_gars_expected(garsf, "1min", expected)


def test_gars_field_gars_1min__check_all_25():
    gars5 = GARSField(GARSGrid("173MA47").polygon.buffer(-0.0001))
    for _ in range(2):
        # repeat to check cache is the same
        assert len(gars5.gars_5min) == 1
        assert len(gars5.gars_1min) == 25


@pytest.mark.parametrize(
    "multi_poly",
    [MULTI_POLY, MULTI_POLY_DUPLICATE],
)
def test_gars_field__gars_1min_multipoly(multi_poly):
    garsf = GARSField(multi_poly.buffer(-0.28))
    expected = [
        "001AQ2102",
        "001AQ2107",
        "001AQ2112",
        "001AQ2117",
        "001AQ2122",
        "001AQ2402",
        "001AQ2407",
        "001AQ2412",
        "001AQ2417",
        "001AQ2422",
        "001AQ2702",
        "001AQ2707",
        "001AQ2712",
        "001AQ2717",
        "001AQ2722",
        "001AQ4102",
        "001AR2722",
        "001AR4102",
        "001AR4107",
        "001AR4112",
        "001AR4117",
        "001AR4122",
        "001AR4402",
        "001AR4407",
        "001AR4412",
        "001AR4417",
        "001AR4422",
        "001AR4702",
        "001AR4707",
        "001AR4712",
        "001AR4717",
        "001AR4722",
    ]
    assert_gars_expected(garsf, "1min", expected)


def test_gars_1min_exists_for_point():
    story = shapely.geometry.Point(-93.729739032219, 42.01131578)
    garsf = GARSField(story)
    for _ in range(2):
        # repeat to check cache is the same
        assert len(garsf.gars_1min) == 1
        assert str(garsf.gars_1min[0]) == "173MA4722"
        assert garsf.gars_1min[0].polygon.equals_exact(
            shapely.wkt.loads(
                "POLYGON ((-93.71666666666667 42,"
                " -93.71666666666667 42.01666666666667,"
                " -93.73333333333333 42.01666666666667,"
                " -93.73333333333333 42,"
                " -93.71666666666667 42))"
            ),
            tolerance=0.5 * 10**-12,
        )
