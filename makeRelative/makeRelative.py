'''
    File name: makeRelative
    Author: Vaibhav Kotak
    Date created: 7/20/2016
    Date last modified: 7/20/2016

    Description: Make all the file paths for your file textures relative to a specific directory
'''

from maya import cmds

def getAllFileNodes():
    fileNodes = cmds.ls(type = "file")
    return fileNodes

def getFolderName():
    folderName = cmds.textFieldGrp("folderNameField", query = True, text = True)
    return folderName

def run(fileNodes, folderName):
    for f in fileNodes:
        texture = cmds.getAttr(f + '.fileTextureName')
        drive, folder, textureName = texture.partition(folderName)
        if folder == folderName:
            cmds.setAttr("%s.fileTextureName" %(f), "%s%s" %(folder, textureName), type = "string")

def main():
    fileNodes = getAllFileNodes()
    folderName = getFolderName()
    run(fileNodes, folderName)

def ui():
    makeRelativeWin = "makeRelativeWin"
    if cmds.window("makeRelativeWin", exists=True):
        cmds.deleteUI("makeRelativeWin")
    if cmds.windowPref("makeRelativeWin", exists=True):
        cmds.windowPref("makeRelativeWin", remove=True)
    winWidth = 150
    winHeight = 75

    cmds.window("makeRelativeWin", width=winWidth, height=winHeight, menuBar=True, sizeable=False, title="Make Relative")

    mainForm = cmds.formLayout("mainForm")

    folderNameField = cmds.textFieldGrp("folderNameField", label = "Folder Name", width=300)

    makeRelativeButton = cmds.button("makeRelativeButton", label = "Make paths relative", command=("makeRelative.main()"), width = 107, height = 25)
    cancelButton = cmds.button("cancelButton", label = "Cancel", command=("cmds.deleteUI(\"makeRelativeWin\")"), width = 107, height = 25)

    sep = cmds.separator("sep", style="in")

    cmds.formLayout(mainForm, edit=True, attachForm=[(folderNameField, "top", 3), (folderNameField, "left", -73)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(makeRelativeButton, "left", 3)], attachControl=[(makeRelativeButton, "top", 5, sep)])
    cmds.formLayout(mainForm, edit=True, attachControl=[(cancelButton, "top", 5, sep), (cancelButton, "left", 5, makeRelativeButton)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(sep, "left", 2), (sep, "right", 2)], attachControl=[(sep, "top", 5, folderNameField)])

    cmds.showWindow("makeRelativeWin")

