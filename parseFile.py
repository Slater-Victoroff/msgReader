import os 

def parseFileToPlainText(fileName, relativePath = "", absolutePath = os.path.dirname(os.path.abspath(__file__))+"/"):
	'''Makes the assumption that it is being run in the same directory as the 
	message files, relative path can be passed as second argument, or absolute
	path can be passed as a replacement for the third. In theory you
	can also specify a path relative to a different absolute path, but
	that seems a little silly to me.'''
	with open(absolutePath+relativePath+fileName) as source:
		for line in source:
			print line

relativePath = "../DesktopClient/GraphInterface/src/testData/Field2Emails/"
parseFileToPlainText("Update.msg", relativePath)
