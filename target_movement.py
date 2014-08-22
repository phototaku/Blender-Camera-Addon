import bpy
from utils import *

cameraRigPropertyName = "Camera Rig Type"
targetCameraType = "TARGET" 

targetCameraSaver = None

def insertTargetMovementCamera():
	if not getTargetCamera():
		camera = newCamera()
		movement = newEmpty(name = "Movement Empty", location = [0, 0, 0])
		
		setParentWithoutInverse(camera, movement)
		camera.location.z = 4
		
		setCustomProperty(camera, cameraRigPropertyName, targetCameraType)

def newCamera():
	bpy.ops.object.camera_add(location = [0, 0, 0])
	camera = bpy.context.object
	camera.name = "Target Camera"
	camera.rotation_euler = [0, 0, 0]
	return camera

def getTargetCamera():
	global targetCameraSaver
	if targetCameraSaver is not None:
		if not targetCameraSaver.get(cameraRigPropertyName) == targetCameraType:
			targetCameraSaver = None
	if targetCameraSaver is None:
		for object in bpy.data.objects:
			if isTargetCamera(object):
				targetCameraSaver = object
	return targetCameraSaver
				
			
def isTargetCamera(camera):
	if camera:
		if camera.get(cameraRigPropertyName) == targetCameraType:
			return True
	return False
	
def selectTargetCamera():
	camera = getTargetCamera()
	if camera:
		deselectAll()
		camera.select = True
		setActive(camera)

# interface

class TargetCameraPanel(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Animation"
	bl_label = "Target Camera"
	bl_context = "objectmode"
	
	@classmethod
	def poll(self, context):
		return getTargetCamera()
	
	def draw(self, context):
		layout = self.layout
		
		layout.operator("animation.select_target_movement_camera")
	
# operators
		
class AddTargetMovementCamera(bpy.types.Operator):
	bl_idname = "animation.add_target_movement_camera"
	bl_label = "Add Target Camera"
	
	def execute(self, context):
		insertTargetMovementCamera()
		return{"FINISHED"}
		
class SelectTargetMovementCamera(bpy.types.Operator):
	bl_idname = "animation.select_target_movement_camera"
	bl_label = "Select Target Camera"
	
	def execute(self, context):
		selectTargetCamera()
		return{"FINISHED"}


def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)