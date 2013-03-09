import re

class ReadableTextFile:
	
	def __init__(self):
		self.data = {"sender": "", "date": "", "subject": "",
					"directRecipients": [], "ccRecipients": [],
					"messageBody": ""}
		self.dynamicFields = ["subject", "directRecipients", "ccRecipients"]
		self.fieldBreaks = ["Subject: ", "To: ", "CC: ", "Content-Type: "]

	def parse(self, corpus):
		'''Assumes we are getting the current result from the trimFileEdges
		method in the parseFile file'''
		self.data["sender"] = self.grabEmails(corpus[0])
		self.data["date"] = corpus[1].strip()[5:] #Very reliable placement of these two
		field = 0
		dataField = []
		appending = False
		for line in corpus:
			if appending is False:
				if self.fieldBreaks[field] in line:
					appending = True
					#dataField.append(line[len(self.fieldBreaks[field]):])
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
		
		
		
	def grabEmails(self, line):
		'''Grabs all email addresses from a given line'''
		return re.findall(r'[\w\.-]+@[\w\.-]+', line)
