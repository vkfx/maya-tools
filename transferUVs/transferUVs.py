'''
    File name: transferUVs
    Author: Vaibhav Kotak
    Date created: 7/20/2016
    Date last modified: 7/20/2016

    Description: Transfer UV's from one object to multiple objects, select the object with correct UVs first
'''

from maya import cmds

def run():
	list = cmds.ls(selection = True)
	size = len(list)
	while(size):
		if (size != 1):
			cmds.transferAttributes(list[0], list[size-1], transferPositions = 0, transferNormals = 0, transferUVs = 2, transferColors = 0, sampleSpace = 4, searchMethod = 3, flipUVs = 0)
		size = size - 1
