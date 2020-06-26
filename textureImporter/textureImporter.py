'''
File name: textureImporter
Author: Vaibhav Kotak
Date created: 2/24/2017

Description: Import textures from selected folder

Note: This tool has not been updated to use PBR workflow
'''

from maya import cmds
import re

def getDirectory():
    folder = cmds.fileDialog2(fileMode=3, dialogStyle=2)
    folder = folder[0]
    cmds.textField("folderTextBox", edit=True, text=folder)

def ui():
    if cmds.window("textureImporterWin", exists=True):
        cmds.deleteUI("textureImporterWin")
    if cmds.windowPref("textureImporterWin", exists=True):
        cmds.windowPref("textureImporterWin", remove=True)
    winWidth = 450
    winHeight = 100

    cmds.window("textureImporterWin", width=winWidth, height=winHeight, menuBar=True, sizeable=False, title="Texture Importer")

    mainForm = cmds.formLayout("mainForm")

    bumpTypeRadioCollection = cmds.radioCollection("bumpTypeRadioCollection")
    normalButton = cmds.radioButton("normalButton", label = "Normal", enable=False, select=True)
    bumpButton = cmds.radioButton("bumpButton", label = "Bump", enable=False)
    bumpTypeText = cmds.text("bumpTypeText", label = "Bump type:")

    rendererRadioCollection = cmds.radioCollection("rendererRadioCollection")
    vrayButton = cmds.radioButton("vrayButton", label = "Vray", select=True)
    redButton = cmds.radioButton("redButton", label = "Redshift")
    rendererText = cmds.text("rendererText", label = "Renderer:")

    tilingTypeRadioCollection = cmds.radioCollection("tilingTypeRadioCollection")
    mariButton = cmds.radioButton("mariButton", label = "UDIM (Mari)", enable=False, select=True)
    mudboxButton = cmds.radioButton("mudboxButton", label = "1-Based (Mudbox)", enable=False)

    folderText = cmds.text("folderText", label="Folder:")

    diffCheckBox = cmds.checkBox("diffCheckBox", label="Diffuse", onCommand="cmds.textField('diffTextbox', edit=True, enable=True)", offCommand="cmds.textField('diffTextbox', edit=True, enable=False)")
    reflectionCheckBox = cmds.checkBox("reflectionCheckBox", label="Reflection Amount", onCommand="cmds.textField('reflectionTextbox', edit=True, enable=True)", offCommand="cmds.textField('reflectionTextbox', edit=True, enable=False)")
    reflectionGlossCheckBox = cmds.checkBox("reflectionGlossCheckBox", label="Reflection Glossiness/Rougness", onCommand="cmds.textField('reflectionGlossTextbox', edit=True, enable=True)", offCommand="cmds.textField('reflectionGlossTextbox', edit=True, enable=False)")
    refractionCheckBox = cmds.checkBox("refractionCheckBox", label="Refraction Amount", onCommand="cmds.textField('refractionTextbox', edit=True, enable=True)", offCommand="cmds.textField('refractionTextbox', edit=True, enable=False)")
    refractionGlossCheckBox = cmds.checkBox("refractionGlossCheckBox", label="Refraction Glossiness/Roughness", onCommand="cmds.textField('refractionGlossTextbox', edit=True, enable=True)", offCommand="cmds.textField('refractionGlossTextbox', edit=True, enable=False)")
    normalCheckBox = cmds.checkBox("normalCheckBox", label="Bump", onCommand="cmds.textField('normalTextbox', edit=True, enable=True)\ncmds.radioButton('normalButton', edit=True, enable=True)\ncmds.radioButton('bumpButton', edit=True, enable=True)", offCommand="cmds.textField('normalTextbox', edit=True, enable=False)\ncmds.radioButton('bumpButton', edit=True, enable=False)\ncmds.radioButton('normalButton', edit=True, enable=False)")
    tilingCheckBox = cmds.checkBox("tilingCheckBox", label="Tiling Mode:", onCommand="cmds.radioButton('mariButton', edit=True, enable=True)\ncmds.radioButton('mudboxButton', edit=True, enable=True)", offCommand="cmds.radioButton('mariButton', edit=True, enable=False)\ncmds.radioButton('mudboxButton', edit=True, enable=False)")

    diffTextbox = cmds.textField("diffTextbox", width=215, enable=False, text="Diffuse")
    reflectionTextbox = cmds.textField("reflectionTextbox", width=215, enable=False, text="Reflection")
    reflectionGlossTextbox = cmds.textField("reflectionGlossTextbox", width=215, enable=False, text="Glossiness")
    refractionTextbox = cmds.textField("refractionTextbox", width=215, enable=False, text="Refraction")
    refractionGlossTextbox = cmds.textField("refractionGlossTextbox", width=215, enable=False, text="refractionGlossiness")
    normalTextbox = cmds.textField("normalTextbox", width=215, enable=False, text="Normal")

    fileDialogButton = cmds.symbolButton("fileDialogButton", image="menuIconFile.png", command="textureImporter.getDirectory()")

    folderTextBox = cmds.textField("folderTextBox")

    sep1 = cmds.separator("sep1", style="in")
    sep2 = cmds.separator("sep2", style="in")

    okButton = cmds.button("okButton", label = "OK", command=("textureImporter.run()"), width = 215, height = 35)
    closeButton = cmds.button("closeButton", label = "Close", command=("cmds.deleteUI('textureImporterWin')"), width = 215, height = 35)

    cmds.formLayout(mainForm, edit=True, attachForm=[(okButton, "left", 5), (okButton, "bottom", 5)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(closeButton, "right", 5), (closeButton, "bottom", 5)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(sep2, "left", 2), (sep2, "right", 2)], attachControl=[(sep2, "top", 5, okButton)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(bumpTypeText, "left", 7)], attachControl=[(bumpTypeText, "bottom", 17, tilingCheckBox)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(normalButton, "right", 158)], attachControl=[(normalButton, "bottom", 15, tilingCheckBox)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(bumpButton, "right", 78)], attachControl=[(bumpButton, "bottom", 15, tilingCheckBox)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(tilingCheckBox, "left", 7)], attachControl=[(tilingCheckBox, "bottom", 17, rendererText)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(mariButton, "right", 135)], attachControl=[(mariButton, "bottom", 15, rendererText)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(mudboxButton, "right", 15)], attachControl=[(mudboxButton, "bottom", 15, rendererText)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(rendererText, "left", 7)], attachControl=[(rendererText, "bottom", 17, okButton)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(vrayButton, "right", 175)], attachControl=[(vrayButton, "bottom", 15, okButton)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(redButton, "right", 65)], attachControl=[(redButton, "bottom", 15, okButton)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(normalCheckBox, "left", 5)], attachControl=[(normalCheckBox, "bottom", 12, bumpTypeText)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(normalCheckBox, "left", 5)], attachControl=[(normalCheckBox, "bottom", 12, bumpTypeText)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(reflectionGlossCheckBox, "left", 5)], attachControl=[(reflectionGlossCheckBox, "bottom", 12, refractionCheckBox)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(refractionCheckBox, "left", 5)], attachControl=[(refractionCheckBox, "bottom", 12, refractionGlossCheckBox)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(refractionGlossCheckBox, "left", 5)], attachControl=[(refractionGlossCheckBox, "bottom", 12, normalCheckBox)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(reflectionCheckBox, "left", 5)], attachControl=[(reflectionCheckBox, "bottom", 12, reflectionGlossCheckBox)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(diffCheckBox, "left", 5)], attachControl=[(diffCheckBox, "bottom", 12, reflectionCheckBox)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(folderText, "left", 5), (folderText, "top", 5)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(fileDialogButton, "right", 2), (fileDialogButton, "top", 5)])

    cmds.formLayout(mainForm, edit=True, attachControl=[(normalTextbox, "bottom", 10, bumpTypeText)], attachForm=[(normalTextbox, "right", 5)])
    cmds.formLayout(mainForm, edit=True, attachControl=[(refractionGlossTextbox, "bottom", 10, normalTextbox)], attachForm=[(refractionGlossTextbox, "right", 5)])
    cmds.formLayout(mainForm, edit=True, attachControl=[(refractionTextbox, "bottom", 10, refractionGlossTextbox)], attachForm=[(refractionTextbox, "right", 5)])
    cmds.formLayout(mainForm, edit=True, attachControl=[(reflectionGlossTextbox, "bottom", 10, refractionTextbox)], attachForm=[(reflectionGlossTextbox, "right", 5)])
    cmds.formLayout(mainForm, edit=True, attachControl=[(reflectionTextbox, "bottom", 10, reflectionGlossTextbox)], attachForm=[(reflectionTextbox, "right", 5)])
    cmds.formLayout(mainForm, edit=True, attachControl=[(diffTextbox, "bottom", 10, reflectionTextbox)], attachForm=[(diffTextbox, "right", 5)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(folderTextBox, "top", 2)], attachControl=[(folderTextBox, "right", 15, fileDialogButton), (folderTextBox, "left", 15, folderText)])

    cmds.radioButton(normalButton, edit = True, select = True)

    cmds.window("textureImporterWin", edit=True, width=450)

    cmds.showWindow("textureImporterWin")

def check(button):
    return cmds.radioCollection(button, query=True, select=True)

def checkFiles(box):
    val = cmds.checkBox(box, query=True, value=True)
    return val

def checkRenderer():
    renderer = check("rendererRadioCollection")
    return renderer

def createMtl(renderer):
    if renderer == "vrayButton":
        mtl = cmds.shadingNode("VRayMtl", asShader=True)
    else:
        mtl = cmds.shadingNode("RedshiftMaterial", asShader=True)
    return mtl

def getSelectedItems():
    checkBoxes = ["diffCheckBox", "reflectionCheckBox", "reflectionGlossCheckBox", "refractionCheckBox", "refractionGlossCheckBox", "normalCheckBox"]

    textBoxDict = {}

    selectedBoxes = []
    for box in checkBoxes:
        if checkFiles(box):
            selectedBoxes.append(box)

    selectedMaps = []
    for box in checkBoxes:
        if checkFiles(box):
            typeMap, checkBox, emptySpace = box.partition("CheckBox")
            selectedMaps.append(typeMap)

    textBoxes = []

    for item in selectedMaps:
        textBox = cmds.textField("%sTextbox" % (item), query=True, text=True)
        textBoxes.append(textBox)

    for item in selectedMaps:
        i = selectedMaps.index(item)
        textBoxDict[item] = textBoxes[i]

    return selectedMaps, textBoxDict


def diction(renderer):
    if renderer == "vrayButton":
        connectionsDict = dict(diff="color", reflection="reflectionColorAmount", reflectionGloss="reflectionGlossiness", refraction="refractionColorAmount", refractionGloss="refractionGlossiness", normal="bumpMap")
    else:
        connectionsDict = dict(diff="diffuse_color", reflection="refl_weight", reflectionGloss="refl_roughness", refraction="refr_weight", refractionGloss="refr_roughness", normal="bumpMap")

    return connectionsDict

def run():
    renderer = checkRenderer()
    mtl = createMtl(renderer)

    if checkFiles("tilingCheckBox"):
        tilingMode = check("tilingTypeRadioCollection")
    else:
        tilingMode = "None"

    if checkFiles("normalCheckBox"):
        bumpType = check("bumpTypeRadioCollection")
    else:
        bumpType = "None"

    fileUdimOne = []

    folderName = cmds.textField("folderTextBox", query=True, text=True)
    files = cmds.getFileList(folder=folderName)

    if checkFiles("tilingCheckBox"):
        for file in files:
            name, underscore, mapType = file.partition("_")
            mapType, dot, udim = mapType.partition(".")
            udim, dottwo, ext = udim.partition(".")
            if tilingMode == "mariButton":
                pattern = re.compile("1001")
            elif tilingMode == "mudboxButton":
                pattern = re.compile("u1_v1")
            found = pattern.search(udim)
            if found:
                fileUdimOne.append(file)
    else:
        for file in files:
            fileUdimOne.append(file)


    connectionsDict = diction(renderer)
    selectedMaps, textBoxDict = getSelectedItems()

    if renderer == "vrayButton":
        for file in fileUdimOne:
            name, underscore, mapType = file.partition("_")
            mapType, dot, udim = mapType.partition(".")
            for selectedMap in selectedMaps:
                textBox = textBoxDict[selectedMap]
                if mapType == textBox:
                    if (selectedMap == "reflectionGloss") or (selectedMap == "refractionGloss") or (selectedMap == "reflection") or (selectedMap == "refraction"):
                        fileTextureNode = cmds.shadingNode("file", asUtility=True)
                        cmds.setAttr("%s.filterType" % (fileTextureNode), 0)
                        cmds.setAttr("%s.fileTextureName" % (fileTextureNode), "%s/%s" % (folderName, file), type="string")
                        if tilingMode == "mariButton":
                            cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 3)
                        elif tilingMode == "mudboxButton":
                            cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 2)
                        connection = connectionsDict[selectedMap]
                        rgb = cmds.shadingNode("rgbToHsv",asUtility=True,name=(fileTextureNode + "_remapHSV"))
                        ramp = cmds.shadingNode("ramp",asUtility=True,name=(fileTextureNode + "_remapRamp"))
                        cmds.connectAttr("%s.outColor" % (fileTextureNode), "%s.inRgb" % (rgb))
                        cmds.connectAttr("%s.outHsvH" % (rgb),"%s.uCoord" % (ramp))
                        cmds.connectAttr("%s.outHsvV" % (rgb),"%s.vCoord" % (ramp))
                        cmds.connectAttr("%s.outAlpha" % (ramp), "%s.%s" % (mtl,connection))
                    else:
                        fileTextureNode = cmds.shadingNode("file", asUtility=True)
                        cmds.setAttr("%s.filterType" % (fileTextureNode), 0)
                        cmds.setAttr("%s.fileTextureName" % (fileTextureNode), "%s/%s" % (folderName, file), type="string")
                        if tilingMode == "mariButton":
                            cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 3)
                        elif tilingMode == "mudboxButton":
                            cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 2)
                        connection = connectionsDict[selectedMap]
                        textBox = textBoxDict[selectedMap]
                        cmds.connectAttr("%s.outColor" % (fileTextureNode), "%s.%s" % (mtl,connection))
                    if bumpType == "normalButton":
                        cmds.setAttr("%s.bumpMapType" % (mtl), 1)
    else:
        for file in fileUdimOne:
            name, underscore, mapType = file.partition("_")
            mapType, dot, udim = mapType.partition(".")
            for selectedMap in selectedMaps:
                if selectedMap == "normal":
                    textBox = textBoxDict[selectedMap]
                    if mapType == textBox:
                        sgSet = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="mtl_%s" % (folderName))
                        if bumpType == "bumpButton":
                            bumpMap = cmds.shadingNode("RedshiftBumpMap", asShader=True)
                            fileTextureNode = cmds.shadingNode("file", asUtility=True)
                            cmds.setAttr("%s.filterType" % (fileTextureNode), 0)
                            cmds.setAttr("%s.fileTextureName" % (fileTextureNode), "%s/%s" % (folderName, file), type="string")
                            if tilingMode == "mariButton":
                                cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 3)
                            elif tilingMode == "mudboxButton":
                                cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 2)
                            cmds.connectAttr("%s.outColor" % (fileTextureNode), "%s.input" % (bumpMap))
                            cmds.connectAttr("%s.out" % (bumpMap), "%s.rsBumpmapShader" % (sgSet))
                            cmds.connectAttr("%s.outColor" % (mtl), "%s.surfaceShader" % (sgSet))
                        else:
                            normalMap = cmds.shadingNode("RedshiftNormalMap", asShader=True)
                            if tilingMode == "mariButton":
                                cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 3)
                            elif tilingMode == "mudboxButton":
                                cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 2)
                            cmds.setAttr("%s.tex0" % (normalMap), "%s/%s" % (folderName, file), type="string")
                            cmds.connectAttr("%s.outDisplacementVector" % (normalMap), "%s.bump_input" % (mtl))
                            cmds.connectAttr("%s.outColor" % (mtl), "%s.surfaceShader" % (sgSet))

                elif (selectedMap == "reflectionGloss") or (selectedMap == "refractionGloss") or (selectedMap == "reflection") or (selectedMap == "refraction"):
                    textBox = textBoxDict[selectedMap]
                    if mapType == textBox:
                        fileTextureNode = cmds.shadingNode("file", asUtility=True)
                        cmds.setAttr("%s.filterType" % (fileTextureNode), 0)
                        cmds.setAttr("%s.fileTextureName" % (fileTextureNode), "%s/%s" % (folderName, file), type="string")
                        rgb = cmds.shadingNode("rgbToHsv",asUtility=True,name=(fileTextureNode + "_remapHSV"))
                        ramp = cmds.shadingNode("ramp",asUtility=True,name=(fileTextureNode + "_remapRamp"))
                        cmds.connectAttr("%s.outColor" % (fileTextureNode), "%s.inRgb" % (rgb))
                        cmds.connectAttr("%s.outHsvH" % (rgb),"%s.uCoord" % (ramp))
                        cmds.connectAttr("%s.outHsvV" % (rgb),"%s.vCoord" % (ramp))
                        if tilingMode == "mariButton":
                            cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 3)
                        elif tilingMode == "mudboxButton":
                            cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 2)
                        connection = connectionsDict[selectedMap]
                        cmds.connectAttr("%s.outAlpha" % (ramp), "%s.%s" % (mtl,connection))
                else:
                    textBox = textBoxDict[selectedMap]
                    if mapType == textBox:
                        fileTextureNode = cmds.shadingNode("file", asUtility=True)
                        cmds.setAttr("%s.filterType" % (fileTextureNode), 0)
                        cmds.setAttr("%s.fileTextureName" % (fileTextureNode), "%s/%s" % (folderName, file), type="string")
                        if tilingMode == "mariButton":
                            cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 3)
                        elif tilingMode == "mudboxButton":
                            cmds.setAttr("%s.uvTilingMode" % (fileTextureNode), 2)
                        connection = connectionsDict[selectedMap]
                        cmds.connectAttr("%s.outColor" % (fileTextureNode), "%s.%s" % (mtl,connection))