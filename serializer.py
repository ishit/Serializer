from sys import argv
from collections import OrderedDict
import json, time, os

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

	def serializeJSON(self, inFileName, outFileName, timer = False):
		inFile = self.readFile(inFileName, 'r')
		outFile = self.readFile(outFileName, 'w')
		allRecords = []
		lines = inFile.readlines()
		t0 = time.time()
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
		t1 = time.time()
		if timer:
			size = os.path.getsize(inFileName)
			elapsedTime = (t1 - t0) * 1000
			print "Time Taken: " + str(elapsedTime)[:-8] + "ms"
			print "Serialization Rate: " + str(int(size/elapsedTime)) + "Kbps"
		json.dump(allRecords, outFile, separators=(',', ':'))
		outFile.close()
		inFile.close()

	def deSerializeJSON(self, inFileName, outFileName, timer = False	):
		inFile = self.readFile(inFileName, 'r')
		outFile = self.readFile(outFileName, 'w')
		data = json.load(inFile)
		allRecords = []
		t0 = time.time()
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
		t1 = time.time()
		if timer:
			size = os.path.getsize(inFileName)
			elapsedTime = (t1 - t0) * 1000
			print "Time Taken: " + str(elapsedTime)[:-8] + "ms"
			print "De-serialization Rate: " + str(int(size/elapsedTime)) + "Kbps"
		for record in allRecords:
			outFile.write(record + "\n")
		outFile.close()
		inFile.close()

def printTemplate():
	print """Run as:
	python serialize.py -m [method(json/protobuf)] [OPTION] -i [input file name] -o [output file name]
	OPTIONS:
		-t : Timer in millseconds.
		-d : Deserialize. Default is serialization."""

def parseArguments():
	s = Serializer()
	method = ""
	for i in range(1, len(argv)):
		if argv[i] == "-i":
			inFileName = argv[i + 1]
		elif argv[i] == "-o":
			outFileName = argv[i + 1]
		elif argv[i] == "-m":
			method = argv[i + 1]

	if method == "json":
		if "-d" in argv:
			if "-t" in argv:
				s.deSerializeJSON(inFileName, outFileName, True)
			else:
				s.deSerializeJSON(inFileName, outFileName)
		else:
			if "-t" in argv:
				s.serializeJSON(inFileName, outFileName, True) 
			else:
				s.serializeJSON(inFileName, outFileName)

	else:
		printTemplate()

parseArguments()