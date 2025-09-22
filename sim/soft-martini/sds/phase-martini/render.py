import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *


# method = 'mdpd'
method = 'martini'

concentration = 75

ovito.scene.load(f'{concentration}/view2.ovito')
pipeline = ovito.scene.pipelines[0]

data = pipeline.compute(0)
data = pipeline.compute(pipeline.source.num_frames)

pipeline.add_to_scene()

# mdpd 75
vp = Viewport()
vp.type = Viewport.Type.Perspective
vp.camera_dir = (0.614, 0.511, 0.6)
vp.camera_pos = (-105, -75, -104)
vp.camera_up = (0.268, -0.852, 0.45)
vp.fov = math.radians(35.0)

# # mdpd 45
# vp = Viewport()
# vp.type = Viewport.Type.Perspective
# vp.camera_dir = (-0.634, 0.6, 0.48)
# vp.camera_pos = (230, -138, -99)
# vp.camera_up = (0.77, 0.52, 0.36)
# vp.fov = math.radians(35.0)

# mdpd 25
# vp = Viewport()
# vp.type = Viewport.Type.Perspective
# vp.camera_dir = (0.612, -0.51, 0.6)
# vp.camera_pos = (-148, 219, -142)
# vp.camera_up = (.4, 0.85, 0.32)
# vp.fov = math.radians(35.0)

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
    size=(2000,2000), 
    filename=f'{method}-{concentration}.pdf', 
    background=(1,1,1), 
    frame=700,
    renderer=renderer2)

# vp.render_anim(
#     size=(1920,1080), 
#     filename="hydrophilic.mp4", 
#     range=(0,200),
#     background=(0,0,0),
#     fps = 30, 
#     renderer=renderer)
