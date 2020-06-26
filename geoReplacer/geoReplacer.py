'''
    File name: geoReplacer
    Author: Vaibhav Kotak
    Date created: 8/16/2016
    Date last modified: 9/7/2016

    Description: Replace geo randomly with piece of geo from a selection
'''

from maya import cmds
import random

def ui():
    geoReplacerWin = "geoReplacerWin"
    if cmds.window("geoReplacerWin", exists=True):
        cmds.deleteUI("geoReplacerWin")
    if cmds.windowPref("geoReplacerWin", exists=True):
        cmds.windowPref("geoReplacerWin", remove=True)
    winWidth = 250
    winHeight = 140

    listOne = [""]
    listTwo = [""]

    cmds.window("geoReplacerWin", width=winWidth, height=winHeight, menuBar=True, sizeable=False, title="Geo Replacer")

    mainForm = cmds.formLayout("mainForm")

    listOneTextLabel = ""
    listTwoTextLabel = ""

    listOneTextLabelReset = "Hi"
    listTwoTextLabelReset = "Hi"

    replaceButton = cmds.button("replaceButton", label = "Replace", command=("geoReplacer.replace(listOne, listTwo)"), width = 145, height = 30)
    cancelButton = cmds.button("cancelButton", label = "Close", command=("cmds.deleteUI('geoReplacerWin')"), width = 145, height = 30)

    listOneText = cmds.text("listOneText", label=listOneTextLabel)
    listTwoText = cmds.text("listTwoText", label=listTwoTextLabel)

    rotationText = cmds.text("rotationText", label = "Keep Rotation:")
    scaleText = cmds.text("scaleText", label = "Keep Scale:")

    rXcb = cmds.checkBox("rXcb", label = "Rotation X")
    rYcb = cmds.checkBox("rYcb", label = "Rotation Y")
    rZcb = cmds.checkBox("rZcb", label = "Rotation Z")

    sXcb = cmds.checkBox("sXcb", label = "Scale X")
    sYcb = cmds.checkBox("sYcb", label = "Scale Y")
    sZcb = cmds.checkBox("sZcb", label = "Scale Z")

    listOneButton = cmds.button("listOneButton", label = "Set objects to be replaced", command=("listOne = geoReplacer.setList();" + \
                                                                                                "listOneTextLabelReset = geoReplacer.resetTextLabel(listOne);" + \
                                                                                                "cmds.text(\"listOneText\", edit=True, label=listOneTextLabelReset)"), width = 150, height = 30)
    listTwoButton = cmds.button("listTwoButton", label = "Set objects to replace", command=("listTwo = geoReplacer.setList();" \
                                                                                            "listTwoTextLabelReset = geoReplacer.resetTextLabel(listTwo);" + \
                                                                                            "cmds.text(\"listTwoText\", edit=True, label=listTwoTextLabelReset)"), width = 150, height = 30)

    sep = cmds.separator("sep", style="in")

    cmds.formLayout(mainForm, edit=True, attachForm=[(listOneButton, "left", 5), (listOneButton, "top", 5)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(listTwoButton, "left", 5)], attachControl=[(listTwoButton, "top", 15, listOneButton)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(rotationText, "left", 25)], attachControl=[(rotationText, "top", 15, listTwoButton)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(scaleText, "right", 25)], attachControl=[(scaleText, "top", 15, listTwoButton)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(rXcb, "left", 25)], attachControl=[(rXcb, "top", 5, rotationText)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(rYcb, "left", 25)], attachControl=[(rYcb, "top", 5, rXcb)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(rZcb, "left", 25)], attachControl=[(rZcb, "top", 5, rYcb)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(sXcb, "right", 25)], attachControl=[(sXcb, "top", 5, rotationText)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(sYcb, "right", 25)], attachControl=[(sYcb, "top", 5, sXcb)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(sZcb, "right", 25)], attachControl=[(sZcb, "top", 5, sYcb)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(listOneText, "right", 5), (listOneText, "top", 10)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(listTwoText, "right", 5)], attachControl=[(listTwoText, "top", 20, listOneButton)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(sep, "left", 2), (sep, "right", 2)], attachControl=[(sep, "top", 18, rZcb)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(replaceButton, "left", 5)], attachControl=[(replaceButton, "top", 5, sep)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(cancelButton, "right", 5)], attachControl=[(cancelButton, "top", 5, sep)])

    cmds.showWindow("geoReplacerWin")

def setList():
    sel = cmds.ls(selection = True, transforms = True)
    return sel

def getRotation(item, axis):
    r = cmds.getAttr("%s.rotate%s" % (item, axis))
    return r

def setRotation(item, axis, number):
    cmds.setAttr("%s.rotate%s" % (item, axis), number)

def getScale(item, axis):
    s = cmds.getAttr("%s.scale%s" % (item, axis))
    return s

def setScale(item, axis, number):
    cmds.setAttr("%s.scale%s" % (item, axis), number)

def checkState(attr, axis):
    state = cmds.checkBox("%s%scb" % (attr, axis), query = True, value = True)
    print state
    return state

def replace(listOne, listTwo):
    cmds.constructionHistory(toggle=0)
    dups = []
    axes = ["X","Y","Z"]
    state = []
    for item in listOne:
        replacer = random.choice(listTwo)
        cmds.select(replacer, replace=True)
        replacerDup = cmds.duplicate(returnRootsOnly=True)
        dups.append(replacerDup[0])
        for axis in axes:
            stateR = checkState("r", axis)
            stateS = checkState("s", axis)
            if stateR == 0:
                rotation = getRotation(item, axis)
                setRotation(replacerDup[0], axis, rotation)
            if stateS == 0:
                scale = getScale(item, axis)
                setScale(replacerDup[0], axis, scale)
        makePointConstraint(replacerDup[0], item)
        cmds.delete(item)
    print dups
    cmds.select(dups)
    cmds.constructionHistory(toggle=1)

def resetTextLabel(item):
    total = len(item)
    if len(item) > 1:
        listTextLabel = ("%s + ... (total: %d)") % (item[0], total)
    else:
        listTextLabel = item[0]
    return listTextLabel

def makePointConstraint(target, parent):
    constraint = cmds.pointConstraint(parent, target, weight = 1, offset = [0,0,0])
    cmds.delete(constraint[0])