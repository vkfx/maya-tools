'''
    File name: addRemapRamp
    Author: Vaibhav Kotak
    Date created: 8/9/2016
    Date last modified: 8/9/2016

    Description: Add a remap ramp to any selected texture node
'''

from maya import cmds

def run():
    sel = cmds.ls(selection=True)
    for item in sel:
        rgb = cmds.shadingNode("rgbToHsv",asUtility=True,name=(item + "_remapHSV"))
        ramp = cmds.shadingNode("ramp",asUtility=True,name=(item + "_remapRamp"))
        cmds.connectAttr("%s.outColor" % (item), "%s.inRgb" % (rgb))
        cmds.connectAttr("%s.outHsvH" % (rgb),"%s.uCoord" % (ramp))
        cmds.connectAttr("%s.outHsvV" % (rgb),"%s.vCoord" % (ramp))
        