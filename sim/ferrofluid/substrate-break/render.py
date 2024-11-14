import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *


ovito.scene.load('hydrophilic-presentation.ovito')
ovito.scene.load('hydrophobic-presentation.ovito')
pipeline = ovito.scene.pipelines[0]

data = pipeline.compute(0)
data = pipeline.compute(pipeline.source.num_frames)

pipeline.add_to_scene()

vp = Viewport()
vp.type = Viewport.Type.Perspective
vp.camera_dir = (0, -1, 0)
vp.camera_pos = (0, 36, 6)
vp.camera_up = (0., 0.0, 1)
vp.fov = math.radians(35.0)

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
#     size=(2560,1440), 
#     filename="figure.png", 
#     background=(0,0,0), 
#     frame=280,
#     renderer=renderer)

vp.render_anim(
    size=(1920,1080), 
    filename="hydrophobic.mp4", 
    range=(0,200),
    background=(0,0,0),
    fps = 30, 
    renderer=renderer)
