from manimlite.renderer import Renderer


def test_set_pixel_in_bounds() -> None:
    r = Renderer(width=8, height=4, bg=" ")
    frame = r.blank_frame()
    r.set_pixel(frame, 2, 1)
    assert frame[1][2] == "#"
    assert frame[0][0] == " "


def test_set_pixel_out_of_bounds_noop() -> None:
    r = Renderer(width=8, height=4, bg=".")
    frame = r.blank_frame()
    for x, y in [(-1, 0), (8, 0), (0, -1), (0, 4), (100, 100)]:
        r.set_pixel(frame, x, y, "#")
    assert all(cell == "." for row in frame for cell in row)


def test_set_pixel_uses_first_character() -> None:
    r = Renderer(width=4, height=2, bg=" ")
    frame = r.blank_frame()
    r.set_pixel(frame, 0, 0, "@!")
    assert frame[0][0] == "@"


def test_set_pixel_empty_ch_noop() -> None:
    r = Renderer(width=4, height=2, bg=" ")
    frame = r.blank_frame()
    r.set_pixel(frame, 1, 1, "")
    assert frame[1][1] == " "
