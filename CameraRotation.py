import bpy, mathutils, math
from mathutils import *
from math import *
 
 # track the camera to head
def addTrackToConstraint(ob, name, target):
    cns = ob.constraints.new('TRACK_TO')
    cns.name = name
    cns.target = target
    cns.subtarget = 'Head'
    cns.track_axis = 'TRACK_NEGATIVE_Z'
    cns.up_axis = 'UP_Y'
    cns.owner_space = 'WORLD'
    cns.target_space = 'WORLD'
    
    return

 # limit the max distance to 5
def limitDist(ob, name, target):
    cns = ob.constraints.new('LIMIT_DISTANCE')
    cns.name = name
    cns.target = target
    cns.subtarget = 'Head'
    cns.distance = 5
    return

 # stack head and empty 
def fixedLocation(ob, name, target):
    cns = ob.constraints.new('COPY_LOCATION')
    cns.name = name
    cns.target = target
    cns.subtarget = 'Head'
    return
 
 
 
def createCamera(origin, target):
    # Create object and camera
    bpy.ops.object.add(
        type='CAMERA',
        location=origin,
        rotation=(0,0,0))        
    ob = bpy.context.object
    ob.name = 'rot_cam'
    cam = ob.data
    cam.name = 'rot_cam'
    addTrackToConstraint(ob, 'HeadTracker', target)

    limitDist(ob,'DistanceLimit',target)
 
    # Lens
    cam.type = 'PERSP'
    cam.lens = 75
    cam.lens_unit = 'MILLIMETERS'
    cam.shift_x = -0.05
    cam.shift_y = 0.1
    cam.clip_start = 0.0
    cam.clip_end = 250.0
    
    
    # Display
    #cam.show_title_safe = True
    cam.show_name = True
 
    # Make this the current camera
    scn = bpy.context.scene
    scn.camera = ob
    return ob
 
def run(origin):
    # Delete all old cameras and lamps
    scn = bpy.context.scene
    for ob in scn.objects:
        if ob.type == 'CAMERA' or ob.type == 'LAMP' or ob.type == 'EMPTY':
            scn.objects.unlink(ob)
    
    # Add an empty at the middle of all render objects
    
    skel_obj= bpy.data.objects['131_09_60fps']
    
    # scale model down
    skel_obj.scale = ((0.15,0.15,0.15))
    bpy.ops.object.add(
        type='EMPTY',
        rotation=(0,0,0)
        )

    
    empty = bpy.context.object
    target = skel_obj
 
    #target.name = 'Target'
    r_cam = createCamera(Vector((0,5,0)), empty)
    fixedLocation(empty,'EmptyBinder',skel_obj)
    r_cam.parent = empty
    
    # rotate 360 in 1147 frame, 0.314 degree per frame
    mat_rot_x = Matrix.Rotation(radians(0.314), 4, 'Z')
    empty.animation_data_clear() 
    empty.rotation_euler = [0, 0, 0]
    bpy.context.scene.frame_set(1)
    empty.keyframe_insert(data_path="rotation_euler", frame=1)
    f = 1
    
    for i in range(1147):
        empty.matrix_world *= mat_rot_x
        empty.rotation_euler = empty.matrix_world.to_euler()
        empty.keyframe_insert(data_path="rotation_euler", frame=f)a
        f+=1

 
if __name__ == "__main__":
    run(Vector((0,0,0)))