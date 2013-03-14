import os 
import string
import re
from readableTextFile import ReadableTextFile

def trimFileEdges(fileName, relativePath = "", absolutePath = os.path.dirname(os.path.abspath(__file__))+"/",
						tripWirePhrase = "From:", exitPhrase = "LZFu"):
	'''Makes the assumption that it is being run in the same directory as the 
	message files, relative path can be passed as second argument, or absolute
	path can be passed as a replacement for the third. In theory you
	can also specify a path relative to a different absolute path, but
	that seems a little silly to me.'''
	with open(absolutePath+relativePath+fileName) as source:
		workingFile = ([removeExtremelyStrangeCharacters(line) for line in source])
		start = False
		finished = False
		relevantPortion = []
		for line in workingFile:
			if not start:
				if tripWirePhrase in line:
					relevantPortion.append(line)
					start = True
			else:
				if exitPhrase in line:
					break
				else:
					relevantPortion.append(line)
		return relevantPortion
		
def removeExtremelyStrangeCharacters(s):
	'''First level of filtering, expects raw file'''
	return filter(lambda x: x in string.printable[0:98],s)

relativePath = "../DesktopClient/GraphInterface/src/testData/Field2Emails/"
corpus = trimFileEdges("Follow-up.msg", relativePath)
test = ReadableTextFile()
test.parseMetaData(corpus)
test.parseMessageBody(corpus)
print test.data
