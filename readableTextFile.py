import re

class ReadableTextFile:
	
	def __init__(self):
		self.data = {"sender": "", "date": "", "subject": "",
					"directRecipients": [], "ccRecipients": [],
					"messageBody": ""}
		self.dynamicFields = ["subject", "directRecipients", "ccRecipients"]
		self.fieldBreaks = ["Subject: ", "To: ", "CC: ", "Content-Type: "]

	def parseMetaData(self, corpus):
		'''Assumes we are getting the current result from the trimFileEdges
		method in the parseFile file, grabs everything currently in the data
		dictionary minus the message body which will be handled seperately'''
		self.data["sender"] = self.grabEmails(corpus[0])
		self.data["date"] = corpus[1].strip()[5:] #Very reliable placement of these two
		field = 0
		dataField = []
		appending = False
		body = False
		for line in corpus:
			if appending is False:
				if self.fieldBreaks[field] in line:
					appending = True
			if appending is True:
				if self.fieldBreaks[field+1] in line:
					if field == 0:
						self.data[self.dynamicFields[field]] = ' '.join(dataField)
					else:
						self.data[self.dynamicFields[field]] = dataField
					field += 1
					if field == 3:
						break
					dataField = self.grabEmails(line)
				else:
					if field == 0:
						dataField.append(line[len(self.fieldBreaks[field]):].strip())
					else:
						dataField.extend(self.grabEmails(line))
	
	def parseMessageBody(self, corpus):
		'''To be run after metadata is collected, requires an accurate 
		subject field to recognize the start of the message body.
		Corpus should still be the same as in the parsing of metaData'''
		body = []
		tripped = False
		subject = self.data["subject"].lower().strip()
		for line in corpus:
			if tripped is False:
				testLine = line.lower()
				if subject in testLine:
					erroneousMatch = "subject: " + self.data["subject"].lower()
					if erroneousMatch not in testLine:
						cutOff = testLine.find(subject) + len(subject)
						firstLine = line[cutOff:].strip()
						body.append(firstLine)
						tripped = True
			elif tripped is True:
				body.append(re.sub("\*\\t", "", line.strip()))
		self.data["messageBody"] = ' '.join(body)
		
	def grabEmails(self, line):
		'''Grabs all email addresses from a given line'''
		return re.findall(r'[\w\.-]+@[\w\.-]+', line)
