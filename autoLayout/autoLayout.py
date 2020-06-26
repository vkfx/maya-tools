'''
    File name: autoLayout
    Author: Vaibhav Kotak
    Date created: 8/16/2016
    Date last modified: 9/18/2016

    Description: Automatically layout selected objects or shells based on selection
'''

from maya import cmds

def ui():
    if cmds.window("autoLayoutWin", exists=True):
        cmds.deleteUI("autoLayoutWin")
    if cmds.windowPref("autoLayoutWin", exists=True):
        cmds.windowPref("autoLayoutWin", remove=True)
    winWidth = 170
    winHeight = 210

    cmds.window("autoLayoutWin", width=winWidth, height=winHeight, menuBar=True, sizeable=False, title="AUV Layout")

    mainForm = cmds.formLayout("mainForm")

    returnButton = cmds.button("returnButton", label = "Return all UVs to 0 to 1", command=("autoLayout.normalizeUVs()"), width = 120, height = 35)

    perRadioCollection = cmds.radioCollection("perRadioCollection")

    objectButton = cmds.radioButton("objectButton", collection = perRadioCollection, label = "Per Object")
    polygonButton = cmds.radioButton("polygonButton", collection = perRadioCollection, label = "Per Poly Shell", onCommand = "cmds.optionMenu('modeMenu', edit = True, enable = False)", offCommand = "cmds.optionMenu('modeMenu', edit = True, enable = True)")

    modeMenu = cmds.optionMenu("modeMenu", label = "Mode:", width = 152)
    zeroToOne = cmds.menuItem("zeroToOne", label = "0 to 1")
    udimItem = cmds.menuItem("udimItem", label = "UDIM")

    layoutMenu = cmds.optionMenu("layoutMenu", label = "Layout:", width = 152)
    oneItem = cmds.menuItem("1x1", label = "1 x 1")
    twoItem = cmds.menuItem("2x2", label = "2 x 2")
    threeItem = cmds.menuItem("3x3", label = "3 x 3")

    sep1 = cmds.separator("sep1", style="in")
    sep2 = cmds.separator("sep2", style="in")

    okButton = cmds.button("okButton", label = "OK", command=("autoLayout.checkPer()"), width = 75, height = 28)
    cancelButton = cmds.button("cancelButton", label = "Close", command=("cmds.deleteUI('autoLayoutWin')"), width = 72, height = 28)

    cmds.formLayout(mainForm, edit=True, attachForm=[(returnButton, "left", 7), (returnButton, "right", 7), (returnButton, "top", 10)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(sep2, "left", 2), (sep2, "right", 2)], attachControl=[(sep2, "top", 10, returnButton)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(objectButton, "left", 5)], attachControl=[(objectButton, "top", 10, sep2)])
    cmds.formLayout(mainForm, edit=True, attachControl=[(polygonButton, "top", 10, sep2), (polygonButton, "left", 5, objectButton)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(modeMenu, "left", 10)], attachControl=[(modeMenu, "top", 10, polygonButton)])
    cmds.formLayout(mainForm, edit=True, attachForm=[(layoutMenu, "left", 10)], attachControl=[(layoutMenu, "top", 10, modeMenu)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(sep1, "left", 2), (sep1, "right", 2)], attachControl=[(sep1, "top", 10, layoutMenu)])

    cmds.formLayout(mainForm, edit=True, attachForm=[(okButton, "left", 5)], attachControl=[(okButton, "top", 10, sep1)])
    cmds.formLayout(mainForm, edit=True, attachControl=[(cancelButton, "top", 10, sep1), (cancelButton, "left", 20, okButton)])

    cmds.radioButton(objectButton, edit = True, select = True)

    cmds.showWindow("autoLayoutWin")

def normalizeUVs():
    sel = cmds.ls(selection = True)
    for item in sel:
        cmds.select(item)
        cmds.polyNormalizeUV(normalizeType = 1, preserveAspectRatio = 1)

def clusterize(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def checkPer():
    sel = cmds.radioCollection("perRadioCollection", query = True, select = True)
    if sel == "objectButton":
        autoObjLayout()
    elif sel == "polygonButton":
        autoPolyLayout()

def autoObjLayout():
    mode = cmds.optionMenu("modeMenu", query = True, select = True)
    layout = cmds.optionMenu("layoutMenu", query = True, select = True)

    u = 0
    v = 0
    sel = cmds.ls(selection = True)

    if mode == 1 and layout == 1:
        layout1x1(u, v, sel, 1)
    elif mode == 1 and layout == 2:
        layout2x2(u, v, sel, 2)
    elif mode == 1 and layout == 3:
        layout3x3(u, v, sel, 3)
    elif mode == 2 and layout == 1:
        udimLayout1x1(u, v, sel, 10)
    elif mode == 2 and layout == 2:
        udimLayout2x2(u, v, sel, 20)
    elif mode == 2 and layout == 3:
        udimLayout3x3(u, v, sel, 30)

def layoutU(sel, u, scale, move, limit):
    for item in sel:
        cmds.select("%s.f[*]" % (item))
        cmds.polyEditUV(scaleU = scale, scaleV = scale)
        if u < limit:
            cmds.polyEditUV(u=u)
            u = u + move
        else:
            u = 0
            cmds.polyEditUV(u=u)
            u = u + move

def layoutV(selCluster, v, move, limit):
    for cluster in selCluster:
        for item in cluster:
            cmds.select("%s.f[*]" % (item))
            if v < limit:
                cmds.polyEditUV(v=v)
            else:
                v = 0
                cmds.polyEditUV(v=v)
        v = v + move

def udimLayout1x1(u, v, sel, cluster):
    layoutU(sel, u, 1, 1, 10)
    selCluster = clusterize(sel, cluster)
    layoutV(selCluster, v, 1, 9999)

def udimLayout2x2(u, v, sel, cluster):
    layoutU(sel, u, .49, .5, 10)
    selCluster = clusterize(sel, cluster)
    layoutV(selCluster, v, .5, 9999)

def udimLayout3x3(u, v, sel, cluster):
    layoutU(sel, u, .32, .34, 10)
    selCluster = clusterize(sel, cluster)
    layoutV(selCluster, v, .33, 9999)

def layout1x1(u, v, sel, cluster):
    button = cmds.radioCollection("perRadioCollection", query = True, select = True)
    if button == "objectButton":
        layoutU(sel, u, 1, 1, 1)
        selCluster = clusterize(sel, cluster)
        layoutV(selCluster, v, 1, 1)
    elif button == "polygonButton":
        cmds.select("%s.f[*]" % (sel)[0])
        polys = cmds.ls(selection=True)
        faces = seperateFaces(polys)
        selCluster = clusterize(faces, cluster)
        selClusterV = clusterize(selCluster, 1)
        layoutUPoly(selCluster, u, 1, 1, 1)
        layoutVPoly(selClusterV, v, 1, 1)

def layout2x2(u, v, sel, cluster):
    button = cmds.radioCollection("perRadioCollection", query = True, select = True)
    if button == "objectButton":
        layoutU(sel, u, .49, .5, 1)
        selCluster = clusterize(sel, cluster)
        layoutV(selCluster, v, .5, 1)
    elif button == "polygonButton":
        cmds.select("%s.f[*]" % (sel)[0])
        polys = cmds.ls(selection=True)
        faces = seperateFaces(polys)
        selCluster = clusterize(faces, cluster)
        selClusterV = clusterize(selCluster, 2)
        layoutUPoly(selCluster, u, .49, .5, 1)
        layoutVPoly(selClusterV, v, .5, 1)


def layout3x3(u, v, sel, cluster):
    button = cmds.radioCollection("perRadioCollection", query = True, select = True)
    if button == "objectButton":
        layoutU(sel, u, .32, .34, 1)
        selCluster = clusterize(sel, cluster)
        layoutV(selCluster, v, .34, 1)
    elif button == "polygonButton":
        cmds.select("%s.f[*]" % (sel)[0])
        polys = cmds.ls(selection=True)
        faces = seperateFaces(polys)
        selCluster = clusterize(faces, cluster)
        selClusterV = clusterize(selCluster, 3)
        layoutUPoly(selCluster, u, .31, .34, 1)
        layoutVPoly(selClusterV, v, .34, 1)

def autoPolyLayout():
    polyCount = checkPolyCount()
    obj = [selObj()]

    mode = cmds.optionMenu("modeMenu", query = True, select = True)
    layout = cmds.optionMenu("layoutMenu", query = True, select = True)

    u = 0
    v = 0
    cmds.select(obj)

    if layout == 1:
        layout1x1(u, v, obj, polyCount)
    elif layout == 2:
        layout2x2(u, v, obj, polyCount)
    elif layout == 3:
        layout3x3(u, v, obj, polyCount)

def layoutUPoly(selCluster, u, scale, move, limit):
    for cluster in selCluster:
        cmds.select(cluster)
        cmds.polyEditUV(scaleU = scale, scaleV = scale)
        if u < limit:
            cmds.polyEditUV(u=u)
            u = u + move
        else:
            u = 0
            cmds.polyEditUV(u=u)
            u = u + move

def layoutVPoly(selCluster, v, move, limit):
    for clusterSet in selCluster:
        for cluster in clusterSet:
            cmds.select(cluster)
            if v < limit:
                cmds.polyEditUV(v=v)
            else:
                v = 0
                cmds.polyEditUV(v=v)
        v = v + move

def checkPolyCount():
    polyCount = cmds.polyEvaluate(faceComponent = True)
    return polyCount

def selObj():
    sel = cmds.ls(selection = True)
    oneFace = sel[0]
    obj, sep, face = oneFace.partition(".")
    return obj

def seperateFaces(polys):
    polys = polys[0]
    obj, dot, faces = polys.partition(".")
    beg, sep, end = polys.partition(":")

    surf, openB, first = beg.partition("[")
    last, closeB, nothing = end.partition("]")

    first = int(first)
    last = int(last)
    last = last + 1
    faces = []
    for i in range(first, last, 1):
        faceName = "%s.f[%d]" % (obj, i)
        faces.append(faceName)
    return faces
