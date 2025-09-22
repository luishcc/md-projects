import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *


# method = 'mdpd'
method = 'martini'

concentration = 'sds'
ovito.scene.load(f'view2.ovito')
pipeline = ovito.scene.pipelines[0]

data = pipeline.compute(0)
data = pipeline.compute(pipeline.source.num_frames)

pipeline.add_to_scene()

# mdpd 75
vp = Viewport()
vp.type = Viewport.Type.Ortho
vp.camera_dir = (0.89, -0.31, -0.31)
vp.camera_pos = (14.4, 3.575, -3)
vp.camera_up = (0.296, 0.95, -0.1)
vp.fov = 200 # math.radians(200)


renderer = OSPRayRenderer(
    ambient_brightness=.9,
    dof_enabled=False,
    direct_light_intensity=.6,
    material_shininess=1.8,
    material_specular_brightness=.02,
    sky_light_enabled=False,
    samples_per_pixel=2,
)

renderer2 = TachyonRenderer()

vp.render_image(
    size=(3500,2000), 
    filename=f'{method}-{concentration}.png', 
    background=(1,1,1), 
    frame=0,
    renderer=renderer2)

# vp.render_anim(
#     size=(1920,1080), 
#     filename="hydrophilic.mp4", 
#     range=(0,200),
#     background=(0,0,0),
#     fps = 30, 
#     renderer=renderer)
