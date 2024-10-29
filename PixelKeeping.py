bl_info={
    "name":"Pixel Keeping",
    "author":"ura",
    "version":(1,0,0),
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
        bpy.ops.object.mode_set(mode='EDIT')

        for uv_num in range(uv_num):
            if keep_pix+f".{uv_num}" not in obj.data.uv_layers:
                obj.data.uv_layers.new(name=keep_pix+f".{uv_num}",do_init=True)

            bm=bmesh.from_edit_mesh(obj.data)

            fp_layer=bm.loops.layers.uv[keep_pix+f".{uv_num}"]

            s=t/sub
            margin=mrgn/sub
            offset=margin/s

            x,y=0,0
            u,v=0,0
            uu,vv=0,0

            uu=uv_num%10
            vv=uv_num//10

            for face in bm.faces:
                if len(face.loops)!=4:
                    continue

                bind_loops=[(u,v),(1+u,v),(1+u,1+v),(u,1+v)]
                    
                for i,loop in enumerate(face.loops):
                    uv=loop[fp_layer].uv
                    x,y=bind_loops[i]

                    uv.x=(x/s)+uu+offset*(u+1)
                    uv.y=(y/s)+vv+offset*(v+1)

                if (v+2)*(1+margin)+1>s+margin:
                    u+=1
                    v=0
                else:
                    v+=1
                
        

            bmesh.update_edit_mesh(obj.data)

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