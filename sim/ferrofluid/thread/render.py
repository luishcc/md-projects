import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *


# ovito.scene.load('break-presentation.ovito')
# ovito.scene.load('break-2.ovito')
# ovito.scene.load('break-4.ovito')
ovito.scene.load('break-1.ovito')
# ovito.scene.load('break-8.ovito')
pipeline = ovito.scene.pipelines[0]

data = pipeline.compute(0)
data = pipeline.compute(pipeline.source.num_frames)

pipeline.add_to_scene()

vp = Viewport()
vp.type = Viewport.Type.Ortho
vp.camera_dir = (1, 0, 0)
vp.camera_pos = (-50, 0, 88)
vp.camera_up = (0, 1, 0)
vp.fov = math.radians(800.0)

renderer = OSPRayRenderer(
    ambient_brightness=1.0,
    dof_enabled=False,
    direct_light_intensity=.7,
    material_shininess=2,
    material_specular_brightness=.01,
    sky_light_enabled=False,
    samples_per_pixel=2
)

# vp.render_image(
#     size=(2560,400), 
#     filename="figure.png", 
#     background=(0,0,0), 
#     frame=200,
#     renderer=renderer)

vp.render_anim(
    size=(1920,300), 
    filename="break-1.mp4", 
    range=(0,150),
    background=(0,0,0),
    fps = 25, 
    renderer=renderer)
