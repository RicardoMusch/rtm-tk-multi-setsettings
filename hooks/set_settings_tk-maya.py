# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.


"""
Maya's Frames Per Second units are:
    game:   15 fps
    film:   24 fps
    pal:    25 fps
    ntsc:   30 fps
    show:   48 fps
    palf:   50 fps
    ntscf:  60 fps
"""



import pymel.core as pm
import maya.cmds as cmds

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class FrameOperation(HookBaseClass):
    """
    Hook called to perform a frame operation with the
    current scene
    """

    def set_project_settings(self, data, **kwargs):

        import ast
        data = ast.literal_eval(data)


        ####################
        "      FPS         "
        ####################
        current_fps = cmds.currentUnit( query=True, linear=True )
        fps = data["sg_fps"]
        if 15 in fps:
            fps = "game"
        if 23.9 in fps:
            fps = "film"
        if 24 in fps:
            fps = "film"
        if 25 in fps:
            fps = "pal"
        if 29.9 in fps:
            fps = "ntsc"
        if 30 in fps:
            fps = "ntsc"
        if 48 in fps:
            fps = "show"
        if 50 in fps:
            fps = "palf"
        if 59 in fps:
            fps = "ntscf"
        if 60 in fps:
            fps = "ntscf"


        msg = """
        The Following settings have been fetched from Shotgun and will be applied:\n
        FPS\n
        {} --> {}
        \n
        Framerange\n
        First frame: {} --> {}\n
        Last frame: {} --> {}\n
        Head handles: {} -- Tail handles: {}
        \n
        Apply?
        """.format(current_fps, fps, current_framerange[0], str(in_frame), current_framerange[1], str(out_frame), head_handles, tail_handles)


        confirm = confirmDialog("Should I copy shaders?")
        if confirm == "Yes":
            for tgt in tgts:
                shp = cmds.listRelatives(src, s=True)[0]
                sg = cmds.listConnections(shp, t="shadingEngine")[0]
                tshp = cmds.listRelatives(tgt, s=True)[0]
                cmds.sets(tshp, e=True, forceElement=sg)


    def get_frame_range(self, **kwargs):
        """
        get_frame_range will return a tuple of (in_frame, out_frame)

        :returns: Returns the frame range in the form (in_frame, out_frame)
        :rtype: tuple[int, int]
        """
        current_in = cmds.playbackOptions(query=True, minTime=True)
        current_out = cmds.playbackOptions(query=True, maxTime=True)
        return (current_in, current_out)

    def set_frame_range(self, in_frame=None, out_frame=None, **kwargs):
        """
        set_frame_range will set the frame range using `in_frame` and `out_frame`

        :param int in_frame: in_frame for the current context
            (e.g. the current shot, current asset etc)

        :param int out_frame: out_frame for the current context
            (e.g. the current shot, current asset etc)

        """

        # set frame ranges for plackback
        pm.playbackOptions(minTime=in_frame,
                           maxTime=out_frame,
                           animationStartTime=in_frame,
                           animationEndTime=out_frame)

        # set frame ranges for rendering
        defaultRenderGlobals = pm.PyNode('defaultRenderGlobals')
        defaultRenderGlobals.startFrame.set(in_frame)
        defaultRenderGlobals.endFrame.set(out_frame)
