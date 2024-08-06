import math
import os
os.environ['OVITO_GUI_MODE'] = '1' # Request a session with OpenGL support
import ovito
from ovito.io import *
from ovito.modifiers import *
from ovito.vis import *


ovito.scene.load('dib-view.ovito')
pipeline = ovito.scene.pipelines[0]

# pipeline = import_file('system.data', 
#     atom_style = 'hybrid', 
#     atom_substyles = ('angle', 'mdpd'))

# trj = LoadTrajectoryModifier()
# trj.source.load('bilayer.lammpstrj')
# pipeline.modifiers.append(trj)

# slice1 = SliceModifier(distance=-4, normal=(0,0,1), slab_width=10, select=True)
# pipeline.modifiers.append(slice1)

# slice2 = SliceModifier(normal=(1,0,0), only_selected=True)
# pipeline.modifiers.append(slice2)

# smooth = SmoothTrajectoryModifier(window_size=2)
# pipeline.modifiers.append(smooth)

# pipeline.modifiers.append(ClearSelectionModifier())

# select = SelectTypeModifier(types={5})
# pipeline.modifiers.append(select)

# surface = ConstructSurfaceModifier(
#     radius = 0.8, 
#     only_selected = True,
#     smoothing_level = 5)
# pipeline.modifiers.append(surface)

# pipeline.modifiers.append(ClearSelectionModifier())

# ambient = AmbientOcclusionModifier(intensity = .6)
# pipeline.modifiers.append(ambient)


data = pipeline.compute(0)
data = pipeline.compute(pipeline.source.num_frames)

# data.particles.vis.radius = 0.2
# data.cell.vis.enabled = False 

pipeline.add_to_scene()

vp = Viewport()
vp.type = Viewport.Type.Perspective
vp.camera_dir = (-0.7, 0.27, 0.66)
vp.camera_pos = (51.6, -15, -41)
vp.camera_up = (0.69, 0.003, 0.73)
vp.fov = math.radians(35.0)

renderer = OSPRayRenderer(
    ambient_brightness=0.9,
    dof_enabled=False,
    direct_light_intensity=1.5,
    material_shininess=10,
    material_specular_brightness=.03,
    sky_light_enabled=False,
    samples_per_pixel=2
)

# vp.render_image(
#     size=(2560,1440), 
#     filename="figure.png", 
#     background=(0,0,0), 
#     frame=549,
#     renderer=renderer)

vp.render_anim(
    size=(2560,1440), 
    filename="dib-big.mp4", 
    background=(0,0,0),
    fps = 50, 
    renderer=renderer)