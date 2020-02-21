import bpy
from . import operators
from .data import get_dcc_sync_props
import logging

logger = logging.Logger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger.setLevel(logging.INFO)


class ROOM_UL_ItemRenderer(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.row()
        split.label(text=item.name)  # avoids renaming the item by accident


class USERS_UL_ItemRenderer(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.row()
        split.label(text=item.name)  # avoids renaming the item by accident


class SettingsPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "DCC Sync"
    bl_idname = "DCCSYNC_PT_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DCC Sync"

    def draw(self, context):
        logger.debug("SettingsPanel::draw()")
        layout = self.layout

        dcc_sync_props = get_dcc_sync_props()

        row = layout.row()
        row.label(text="VRtist", icon='SCENE_DATA')

        row = layout.column()
        row.operator(operators.LaunchVRtistOperator.bl_idname, text="Launch VRTist")

        row = layout.row()
        row.label(text="DCC Sync", icon='SCENE_DATA')

        row = layout.column()

        connected = operators.shareData.client is not None and operators.shareData.client.isConnected()
        if not connected or not operators.shareData.currentRoom:

            # Room list
            row = layout.row()
            row.template_list("ROOM_UL_ItemRenderer", "", dcc_sync_props,
                              "rooms", dcc_sync_props, "room_index", rows=4)

            # Join room
            col = row.column()
            col.operator(operators.ConnectOperator.bl_idname, text="Connect")
            col.operator(operators.JoinRoomOperator.bl_idname, text="Join Room")

            row = layout.row()
            col = row.column()
            col.label(text="Room Users: ")
            col.template_list("USERS_UL_ItemRenderer", "", dcc_sync_props,
                              "users", dcc_sync_props, "user_index", rows=4)

            row = layout.row()
            row.prop(dcc_sync_props, "room", text="Room")
            row.operator(operators.CreateRoomOperator.bl_idname, text='Create Room')
            row = layout.row()
            row.prop(dcc_sync_props, "user", text="User")

            col = layout.column()
            row = col.row()
            row.prop(dcc_sync_props, "advanced",
                     icon="TRIA_DOWN" if dcc_sync_props.advanced else "TRIA_RIGHT",
                     icon_only=True, emboss=False)
            row.label(text="Advanced options")
            if dcc_sync_props.advanced:
                col.prop(dcc_sync_props, "host", text="Host")
                col.prop(dcc_sync_props, "port", text="Port")
                col.prop(dcc_sync_props, "VRtist", text="VRtist Path")
                col.prop(dcc_sync_props, "showServerConsole", text="Show server console")

        else:
            col = row.column()
            col.operator(operators.LeaveRoomOperator.bl_idname,
                         text=f"Leave Room : {operators.shareData.currentRoom}")
            col.label(text="Room Users: ")
            col.template_list("USERS_UL_ItemRenderer", "", dcc_sync_props,
                              "users", dcc_sync_props, "user_index", rows=4)


classes = (
    ROOM_UL_ItemRenderer,
    USERS_UL_ItemRenderer,
    SettingsPanel
)


def register():
    for _ in classes:
        bpy.utils.register_class(_)


def unregister():
    for _ in classes:
        bpy.utils.unregister_class(_)
