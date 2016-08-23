from sys import argv
from collections import OrderedDict
import json

class Serializer():
	"""docstring for Serializer"""
	def __init__(self):
		pass

	def readFile(self, fileName, mode):
		try:
			file = open(fileName, mode)
		except IOError:
			print fileName + ": file does not exist."
			exit(0)
		return file

	def serializeJSON(self, inFileName, outFileName):
		inFile = self.readFile(inFileName, 'r')
		outFile = self.readFile(outFileName, 'w')
		allRecords = []
		lines = inFile.readlines()
		for line in lines:
			line = line[:-1]
			colonSeparated = line.split(':')
			record = OrderedDict()
			record["Name"] = colonSeparated[0].split(',')[0]
			if len(colonSeparated) < 2:
				continue
			record["CourseMarks"] = []
			for i in range(1, len(colonSeparated)):
				markRecord = OrderedDict()
				markRecord["CourseScore"] = int(colonSeparated[i].split(',')[1])
				markRecord["CourseName"] = colonSeparated[i].split(',')[0]
				record["CourseMarks"].append(markRecord)
			record["RollNo"] = int(colonSeparated[0].split(',')[1])
			allRecords.append(record)
		json.dump(allRecords, outFile, separators=(',', ':'))
		outFile.close()
		inFile.close()

	def deSerializeJSON(self, inFileName, outFileName):
		inFile = self.readFile(inFileName, 'r')
		outFile = self.readFile(outFileName, 'w')
		data = json.load(inFile)
		allRecords = []
		for jsonRecord in data:
			record = ""
			record += jsonRecord["Name"]
			record += "," + str(jsonRecord["RollNo"])
			if "CourseMarks" in jsonRecord:
				for course in jsonRecord["CourseMarks"]:
					record += ":"
					record += course["CourseName"]
					record += ","
					record += str(course["CourseScore"])
			allRecords.append(record)
		for record in allRecords:
			outFile.write(record + "\n")
		outFile.close()
		inFile.close()

s = Serializer()
s.deSerializeJSON('out', 'in') 