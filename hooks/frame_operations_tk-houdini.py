# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import hou
import os

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class FrameOperation(HookBaseClass):
    """
    Hook called to perform a frame operation with the
    current scene
    """

    def set_project_settings(self, in_frame=None, out_frame=None, head_handles=None, tail_handles=None, fps=None, **kwargs):
        
        "Houdini Vars"
        current_framerange = hou.playbar.frameRange()
        current_fps = hou.fps()



        msg = """
        <strong>The Following settings have been fetched from Shotgun and will be applied:</strong>
        \n
        <strong>FPS</strong>\n
        {} --> {}
        \n
        <strong>Framerange</strong>\n
        First frame: {} --> {}\n
        Last frame: {} --> {}\n
        Head handles: {} -- Tail handles: {}
        \n
        <strong>Apply?</strong>
        """.format(current_fps, fps, current_framerange[0], str(in_frame), current_framerange[1], str(out_frame), head_handles, tail_handles)

        hou.ui.displayConfirmation(msg, severity=hou.severityType.Message, help=None, title=None, details=None, details_label=None, suppress=hou.confirmType.OverwriteFile)



    def get_frame_range(self, **kwargs):
        """
        get_frame_range will return a tuple of (in_frame, out_frame)

        :returns: Returns the frame range in the form (in_frame, out_frame)
        :rtype: tuple[int, int]
        """
        current_in, current_out = hou.playbar.playbackRange()
        return (current_in, current_out)

    def set_frame_range(self, in_frame=None, out_frame=None, **kwargs):
        """
        set_frame_range will set the frame range using `in_frame` and `out_frame`

        :param int in_frame: in_frame for the current context
            (e.g. the current shot, current asset etc)

        :param int out_frame: out_frame for the current context
            (e.g. the current shot, current asset etc)

        """

        # We have to use hscript until SideFX gets around to implementing hou.setGlobalFrameRange()
        hou.hscript("tset `((%s-1)/$FPS)` `(%s/$FPS)`" % (in_frame, out_frame))
        hou.playbar.setPlaybackRange(in_frame, out_frame)
