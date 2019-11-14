# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import nuke
import os

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class FrameOperation(HookBaseClass):
    """
    Hook called to perform a frame operation with the
    current scene
    """

    def get_frame_range(self, **kwargs):
        """
        get_frame_range will return a tuple of (in_frame, out_frame)

        :returns: Returns the frame range in the form (in_frame, out_frame)
        :rtype: tuple[int, int]
        """
        current_in = int(nuke.root()["first_frame"].value())
        current_out = int(nuke.root()["last_frame"].value())
        return (current_in, current_out)

    def set_frame_range(self, in_frame=None, out_frame=None, **kwargs):
        """
        set_frame_range will set the frame range using `in_frame` and `out_frame`

        :param int in_frame: in_frame for the current context
            (e.g. the current shot, current asset etc)

        :param int out_frame: out_frame for the current context
            (e.g. the current shot, current asset etc)

        """

        # unlock
        locked = nuke.root()["lock_range"].value()
        if locked:
            nuke.root()["lock_range"].setValue(False)
        # set values
        nuke.root()["first_frame"].setValue(in_frame)
        nuke.root()["last_frame"].setValue(out_frame)
        # and lock again
        if locked:
            nuke.root()["lock_range"].setValue(True)


    def set_project_settings(self, in_frame=None, out_frame=None, head_handles=None, tail_handles=None, fps=None, **kwargs):
        
        "Get Nuke Colorspace Settings from ENV"
        try:
            nuke_colorManagement = os.environ["NUKE_COLORMANAGEMENT"]
        except:
            nuke_colorManagement = nuke.root()["colorManagement"].value()
        try:
            nuke_ocio_config = os.environ["NUKE_OCIO_CONFIG"]
        except:
            nuke_ocio_config = nuke.root()["OCIO_config"].value()



        msg = """\n
        <strong>The Following settings have been fetched from Shotgun and will be applied:</strong>
        \n
        <strong>Colorspace Settings</strong>\n
        {}: {} --> {}: {}
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
        """.format(nuke.root()["colorManagement"].value(), nuke.root()["OCIO_config"].value(), nuke_colorManagement, nuke_ocio_config, str(nuke.root()["fps"].value()), fps, str(int(nuke.root()["first_frame"].value())), str(in_frame), str(int(nuke.root()["last_frame"].value())), str(out_frame), head_handles, tail_handles)

        try:
            if nuke.ask(msg):

                ###################
                "      FPS        "
                ###################
                try:
                    nuke.root()["fps"].setValue(fps)
                except:
                    pass


                ###################
                "Colorspace"
                ###################
                try:
                    nuke.root()["colorManagement"].setValue(nuke_colorManagement)
                    nuke.root()["OCIO_config"].setValue(nuke_ocio_config)
                except:
                    pass


                ###################
                "Set Framerange"
                ###################
                # unlock
                locked = nuke.root()["lock_range"].value()
                if locked:
                    nuke.root()["lock_range"].setValue(False)
                # set values
                try:
                    nuke.root()["first_frame"].setValue(in_frame)
                except:
                    pass
                try:
                    nuke.root()["last_frame"].setValue(out_frame)
                except:
                    pass
                # and lock again
                if locked:
                    nuke.root()["lock_range"].setValue(True)


                try:
                    #####################
                    "Set Viewer Handles"
                    #####################
                    "Get the node that is the current viewer"
                    v = nuke.activeViewer().node()

                    "Set Framerange Handles"
                    v['frame_range_lock'].setValue(True)
                    stringed_frange = str(int(in_frame+head_handles))+"-"+str(int(out_frame-tail_handles))
                    v['frame_range'].setValue(str(stringed_frange))
                except:
                    pass

        except Exception as e:
            print e
