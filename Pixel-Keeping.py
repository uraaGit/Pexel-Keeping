bl_info={
    "name":"Pixel Keeping",
    "author":"ura",
    "version":(1,1,0),
    "blender":(4,2,0),
    "location":"UV Editor",
    "category":"UV"
}

texture_size=[
    ('256',"256x256","256x256"),
    ('512',"512x512","512x512"),
    ('1024',"1024x1024","1024x1024"),
    ('2048',"2048x2048","2048x2048")
]

pixel_count=[
    ('4',"4x4","4x4"),
    ('8',"8x8","8x8"),
    ('16',"16x16","16x16"),
    ('32',"32x32","32x32"),
]

import bpy
import bmesh
from math import sqrt
from mathutils import Vector

class UV_OT_uv_pixel_keeping(bpy.types.Operator):
    bl_idname="uv.uv_pixel_keeping"
    bl_label="Arrange faces to UV"
    bl_options={'REGISTER','UNDO'}

    uv_number:bpy.props.IntProperty(
        name="UV Number",
        default=1,
        min=1,
        max=8
    )

    tex_size:bpy.props.EnumProperty(
        name="Texture Size",
        items=texture_size,
        default='1024'
    )

    pixel_keep:bpy.props.EnumProperty(
        name='Pixel Count',
        items=pixel_count,
        default='8'
    )

    margin:bpy.props.IntProperty(
        name="Margin",
        default=2,
        min=1,
        max=4
    )

    def execute(self,context):
        uv_num=self.uv_number
        t=int(self.tex_size)
        sub=int(self.pixel_keep)
        mrgn=self.margin

        arrange_faces_uv(uv_num,t,sub,mrgn)

        return {'FINISHED'}

keep_pix="pixel_keeping"

def arrange_faces_uv(uv_num,t,sub,mrgn):
    obj=bpy.context.active_object
    if obj and obj.type=='MESH':
        pre_uv=obj.data.face_pixel.pre_uv
        pre_uv.clear()

    if obj and obj.type=='MESH':
        bpy.ops.object.mode_set(mode='EDIT')

        bit=1/t
        mapchip=bit*sub
        margin=bit*mrgn
        offset=mapchip+margin

        turn_co=t/(sub+mrgn)

        if keep_pix+f".{uv_num}" not in obj.data.uv_layers:
            obj.data.uv_layers.new(name=keep_pix+f".{uv_num}",do_init=True)

        bm=bmesh.from_edit_mesh(obj.data)
        fp_layer=bm.loops.layers.uv[keep_pix+f".{uv_num}"]

        uv_co=[(ii*offset+offset/2+margin,jj*offset+offset/2+margin) for ii in range(int(turn_co)-1) for jj in range(int(turn_co)-1)]
        face_co=[
            (sum(loop[fp_layer].uv.x for loop in face.loops)/len(face.loops),
            sum(loop[fp_layer].uv.y for loop in face.loops)/len(face.loops))
            for face in bm.faces for loop in face.loops]

        unused_co=[uv for uv in uv_co if uv not in face_co]

        for uv_num in range(uv_num):
            for face in bm.faces:

                face_x=sum(loop[fp_layer].uv.x for loop in face.loops)/len(face.loops)
                face_y=sum(loop[fp_layer].uv.y for loop in face.loops)/len(face.loops)
                pre_co=(face_x,face_y)

                if pre_co in uv_co:
                    u,v=uv_co[uv_co.index(pre_co)]
                else:
                    u,v=unused_co[0]
                    unused_co.pop(0)

                
                
                if len(face.loops)!=4:
                    continue

                if len(bm.faces)>len(uv_co):
                    bpy.context.window_manager.popup_menu(
                        lambda self,context: 
                        self.layout.label(
                            text="Error: Not enough UV coodinates for faces. Reduce Texture Size or Pixel Count."),
                        title="UV Error",
                        icon='ERROR')
                    return

                # u,v=uv_co[index]

                bind_loops=[(u-mapchip/2,v-mapchip/2),(u+mapchip/2,v-mapchip/2),(u+mapchip/2,v+mapchip/2),(u-mapchip/2,v+mapchip/2)]
                    
                for i,loop in enumerate(face.loops):
                    uv=loop[fp_layer].uv
                    x,y=bind_loops[i]

                    uv.x=x+uv_num
                    uv.y=y

        bmesh.update_edit_mesh(obj.data)
        uv_co.clear()

def menu_func(self,context):
    layout=self.layout
    layout.separator()
    layout.operator(UV_OT_uv_pixel_keeping.bl_idname,text="Arrange faces to uv")

def register():
    bpy.utils.register_class(UV_OT_uv_pixel_keeping)
    bpy.types.VIEW3D_MT_uv_map.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)
    bpy.utils.unregister_class(UV_OT_uv_pixel_keeping)

if __name__=="__main__":
    register()
