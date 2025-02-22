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

    #def set_project_settings(self, in_frame=None, out_frame=None, head_handles=None, tail_handles=None, fps=None, **kwargs):
    def set_project_settings(self, data, **kwargs):

        print "\n\n"
        print data
        print "\n\n"

        import ast
        data = ast.literal_eval(data)


    
        #############################################
        print "Nuke Color Management"
        #############################################
        "Color Management"
        nuke_colorManagement = data["sg_nuke_color_management"]
        if "$" in nuke_colorManagement:
            nuke_colorManagement = os.environ[nuke_colorManagement.replace("$", "")]
        if nuke_colorManagement == None:
            nuke_colorManagement = nuke.root()["colorManagement"].getValue()
        
        "OCIO config"
        nuke_ocio_config = data["sg_nuke_ocio_config"]
        if "$" in nuke_ocio_config:
            nuke_ocio_config = os.environ[nuke_ocio_config.replace("$", "")]
        if nuke_ocio_config == None:
            nuke_ocio_config = nuke.root()["OCIO_config"].getValue()
        
        "Custom OCIO Config"
        nuke_custom_ocio_config_path = data["sg_custom_ocio_config_path"]
        if "$" in nuke_custom_ocio_config_path:
            nuke_custom_ocio_config_path = os.environ[nuke_custom_ocio_config_path.replace("$", "")]
        if nuke_custom_ocio_config_path == None:
            nuke_custom_ocio_config_path = ""


        #############################################
        print "Get FPS from dict"
        #############################################
        fps = data.get("sg_fps")
        print "FPS from dict:", fps

        
        try:    
            #############################################
            print "Get Frames from dict"
            #############################################
            first_frame = data.get("sg_in_frame")
            last_frame = data.get("sg_out_frame")
            head_handles = data.get("sg_head_handles")
            tail_handles = data.get("sg_tail_handles")
            print "Got frame info from dict", first_frame, last_frame, head_handles, tail_handles
        except:
            fps = nuke.root()["fps"].value()



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
        """.format(nuke.root()["colorManagement"].value(), nuke.root()["OCIO_config"].value(), nuke_colorManagement, nuke_ocio_config, str(nuke.root()["fps"].value()), fps, str(int(nuke.root()["first_frame"].value())), first_frame, str(int(nuke.root()["last_frame"].value())), last_frame, head_handles, tail_handles)

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
                    nuke.root()["customOCIOConfigPath"].setValue(nuke_custom_ocio_config_path)
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
                    nuke.root()["first_frame"].setValue(first_frame)
                except:
                    pass
                try:
                    nuke.root()["last_frame"].setValue(last_frame)
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
                    stringed_frange = str(int(first_frame+head_handles))+"-"+str(int(last_frame-tail_handles))
                    v['frame_range'].setValue(str(stringed_frange))
                except:
                    pass

        except Exception as e:
            print e
