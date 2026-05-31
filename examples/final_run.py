from manimlite.core import Node 
from manimlite import CameraZoom, Rotate, Scene, SkiaRenderer, renderer
from manimlite.export import PyAVEncoder
from manimlite.shapes import Circle, Line, Path, Rectangle
from manimlite.value import GradientOverlay
import sys


WIDTH = 1280
HEIGHT = 720
FPS = 30.0
DURATION = 30.0

BG = (30, 30, 30)

def get_skia_renderer() -> SkiaRenderer:
    return SkiaRenderer(clear_color=BG)


scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
group = Node(x=480, y=120)
ball = Circle(x=0, y=0, r=56, fill_color="#A51C30", stroke_color="#FFFFFF", stroke_width=2.0)
group.add(ball)
scene.add_node(group)
encoder = PyAVEncoder(scene=scene, output_path="./", renderer=get_skia_renderer())
result = encoder.encode(verbose=True)
print(f"Output: {result}", file=sys.stderr)
