import libxml2
import subprocess
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def analyzeExample(ctxt, exampleXMLElement):
	ctxt.setContextNode(exampleXMLElement)
	res = ctxt.xpathEval(".//codeblock")
	expected = ctxt.xpathEval(".//codeblock/systemoutput")


	print "\n\n====================="
	print bcolors.HEADER + "Testing Command: " +res[0].content + bcolors.ENDC + "\n" 
	#print "Expecting output:"
	#print expected[0].content + "\n"
	
	commands = '''
	cd testdir
	''' + res[0].content
	
	process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out, err = process.communicate(commands)
	response = out
	
	if response.strip() == expected[0].content.strip():
		print "RESULT: " + bcolors.OKBLUE + "SUCCESS" + bcolors.ENDC
	else:
		print "RESULT: " + bcolors.FAIL + "FAIL" + bcolors.ENDC
		print "Expected:\n" + expected[0].content.strip()
		print "Got: \n" + response.strip()

	return;

def analyzeDITAFile(filename):
	print "__________________________________________________"
	print bcolors.UNDERLINE + bcolors.BOLD + bcolors.HEADER +  "Analyzing: " + filename + bcolors.ENDC + bcolors.ENDC + bcolors.ENDC + "\n"
	
	doc = libxml2.parseFile(filename)
	ctxt = doc.xpathNewContext()
	examples = ctxt.xpathEval("//example")
	for ex in examples:
		analyzeExample(ctxt, ex)
	doc.freeDoc()
	ctxt.xpathFreeContext()


	print "End: " + filename
	print "__________________________________________________"
	print "\n\n"
	
	return;


for filename in os.listdir('.'):
	if filename.endswith("dita"):
		analyzeDITAFile(filename)






