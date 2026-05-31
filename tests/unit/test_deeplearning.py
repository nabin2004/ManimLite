"""Unit tests for motiongram.deeplearning visual nodes."""

from __future__ import annotations

import importlib
import inspect
import pkgutil

import pytest

from motiongram.animate import apply_timeline
from motiongram.canvas import NullCanvas, RecordingCanvas
from motiongram.core import Node, Scene
from motiongram.deeplearning import (
    ActivationFunctions,
    AnimateAttribute,
    AnimateIntAttribute,
    Convolutions,
    HiddenLayers,
    Matrices,
    Scalars,
)
from motiongram.deeplearning import linear_algebra as la_mod


def _all_node_classes() -> list[type[Node]]:
    """Collect every Node subclass exported from deeplearning submodules."""
    import motiongram.deeplearning as dl_pkg

    classes: list[type[Node]] = []
    prefix = dl_pkg.__name__ + "."
    for mod_info in pkgutil.walk_packages(dl_pkg.__path__, prefix):
        if mod_info.name.endswith(("_draw", "animators")):
            continue
        mod = importlib.import_module(mod_info.name)
        for _, obj in inspect.getmembers(mod, inspect.isclass):
            if issubclass(obj, Node) and obj is not Node and obj.__module__ == mod_info.name:
                classes.append(obj)
    return classes


@pytest.mark.parametrize("cls", _all_node_classes(), ids=lambda c: c.__name__)
def test_node_constructs_and_draws(cls: type[Node]) -> None:
    """Each deeplearning node instantiates with defaults and draws on NullCanvas."""
    node = cls()
    node.draw(NullCanvas(), 0.0, 0.0)


def test_scalars_custom_value() -> None:
    s = Scalars(value=0.001, label="lr")
    assert s.value == 0.001
    assert s.label == "lr"
    s.draw(NullCanvas(), 10.0, 10.0)


def test_matrices_highlight_row() -> None:
    m = Matrices(
        values=[[1.0, 2.0], [3.0, 4.0]],
        highlight_row=1,
    )
    m.draw(RecordingCanvas(), 0.0, 0.0)


def test_animate_attribute_on_activation() -> None:
    act = ActivationFunctions(input_val=-2.0)
    scene = Scene()
    scene.add_node(act)
    scene.add_animation(0.0, 1.0, act, AnimateAttribute("input_val", -2.0, 3.0))
    apply_timeline(scene, 0.0, ease=None)
    assert act.input_val == pytest.approx(-2.0)
    apply_timeline(scene, 1.0, ease=None)
    assert act.input_val == pytest.approx(3.0)


def test_animate_int_on_matrix_multiplication() -> None:
    from motiongram.deeplearning import MatrixMultiplication

    mm = MatrixMultiplication(
        matrix_a=[[1.0, 2.0], [3.0, 4.0]],
        matrix_b=[[5.0, 6.0], [7.0, 8.0]],
        active_row=0,
        active_col=0,
    )
    scene = Scene()
    scene.add_node(mm)
    scene.add_animation(0.0, 1.0, mm, AnimateIntAttribute("active_row", 0, 1))
    apply_timeline(scene, 1.0, ease=None)
    assert mm.active_row == 1


def test_convolutions_kernel_position() -> None:
    conv = Convolutions(
        input_grid=[[1.0, 0.0], [0.0, 1.0]],
        kernel=[[1.0, 0.0], [0.0, 1.0]],
        kernel_row=0,
        kernel_col=0,
    )
    conv.draw(NullCanvas(), 0.0, 0.0)
    anim = AnimateIntAttribute("kernel_col", 0, 1)
    anim.apply(conv, 1.0)
    assert conv.kernel_col == 1


def test_hidden_layers_progress() -> None:
    net = HiddenLayers(layer_sizes=[3, 4, 2], progress=0.0)
    scene = Scene()
    scene.add_node(net)
    scene.add_animation(0.0, 2.0, net, AnimateAttribute("progress", 0.0, 1.0))
    apply_timeline(scene, 1.0, ease=None)
    assert 0.0 < net.progress < 1.0


def test_dot_products_progress() -> None:
    dp = la_mod.DotProducts(vec_a=[1.0, 2.0, 3.0], vec_b=[4.0, 5.0, 6.0], progress=0.0)
    anim = AnimateAttribute("progress", 0.0, 1.0)
    anim.apply(dp, 0.5)
    assert 0.0 < dp.progress < 1.0
