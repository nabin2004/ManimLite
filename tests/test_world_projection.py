"""Deterministic checks for centered world viewport math."""

from __future__ import annotations

import pytest

from motiongram.world import WorldSpec, screen_to_world, world_pixel_affine_coeffs, world_to_screen


def test_world_to_screen_corners_y_down() -> None:
    spec = WorldSpec(world_width=10.0, world_height=10.0, y_down=True)
    fw, fh = 1000, 500
    assert world_to_screen(-5.0, 0.0, spec=spec, frame_w=fw, frame_h=fh) == (0.0, 250.0)
    assert world_to_screen(5.0, 0.0, spec=spec, frame_w=fw, frame_h=fh) == (1000.0, 250.0)
    assert world_to_screen(0.0, -2.5, spec=spec, frame_w=fw, frame_h=fh) == (500.0, 125.0)
    assert world_to_screen(0.0, 2.5, spec=spec, frame_w=fw, frame_h=fh) == (500.0, 375.0)


def test_world_to_screen_math_up() -> None:
    spec = WorldSpec(world_width=10.0, world_height=10.0, y_down=False)
    fw, fh = 1000, 500
    assert world_to_screen(0.0, 2.5, spec=spec, frame_w=fw, frame_h=fh) == (500.0, 125.0)
    assert world_to_screen(0.0, -2.5, spec=spec, frame_w=fw, frame_h=fh) == (500.0, 375.0)


def test_screen_to_world_round_trip() -> None:
    spec = WorldSpec(world_width=10.0, world_height=8.0, y_down=True)
    fw, fh = 960, 540
    for wx, wy in ((-3.2, 1.1), (0.0, 0.0), (4.4, -2.0)):
        sx, sy = world_to_screen(wx, wy, spec=spec, frame_w=fw, frame_h=fh)
        rw_x, rw_y = screen_to_world(sx, sy, spec=spec, frame_w=fw, frame_h=fh)
        assert rw_x == pytest.approx(wx)
        assert rw_y == pytest.approx(wy)


def test_affine_coeffs_matches_point_map() -> None:
    spec = WorldSpec(world_width=10.0, world_height=10.0, y_down=False)
    fw, fh = 800, 400
    ax, bx, cx, ay, by, cy = world_pixel_affine_coeffs(spec, fw, fh)

    def aff(x: float, y: float) -> tuple[float, float]:
        return (ax * x + bx * y + cx, ay * x + by * y + cy)

    for wx, wy in ((0.0, 1.25), (-4.5, -3.3)):
        mapped = aff(wx, wy)
        desired = world_to_screen(wx, wy, spec=spec, frame_w=fw, frame_h=fh)
        assert mapped == pytest.approx(desired)


def test_zoom_and_camera_in_helpers() -> None:
    spec = WorldSpec(world_width=10.0, world_height=10.0, y_down=True)
    fw, fh = 100, 100
    a = world_to_screen(1.0, 0.0, spec=spec, frame_w=fw, frame_h=fh)
    b = world_to_screen(1.0, 0.0, spec=spec, frame_w=fw, frame_h=fh, cam_x=1.0, zoom=2.0)
    assert b[0] == pytest.approx(50.0)
    assert a[0] == pytest.approx(60.0)
