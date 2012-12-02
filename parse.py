from itertools import dropwhile
from xml.dom import minidom
import re

# Node and Transition are classes used to represent traces. __str__ added for debugging
class Node:
	def __str__(self):
		res = ""
		if self.isloopstart:
			res +=  "|:\n"

		for var in self.variables:
			res += var[0] + " = " + var[1] + "\n"

		if self.transition:
			res += str(self.transition) + "\n"
		return res

class Transition:
	def __str__(self):
		res = ""
		res += "-->" + self.process + "<--\n"
		res += str(self.nextNode)
		return res

# Parse full NuSMV output
def parse(smvoutput):
	smvlines = smvoutput.split("\n")
	smvlines = map(lambda x: x.strip(), smvlines)

	# Remove the preamble (version output etc)
	actualOutput = dropwhile(ispreamble, smvlines)

	# Separate the CTL specifications with their result
	specifications = splitAt(isspecification, actualOutput)

	# Check which spec was true and which was false, then get trace if needed
	for spec in specifications:
		specdesc = spec[0]
		if specdesc.endswith("false"):
			specdesc = specdesc[len("-- specification "):][:-len(" is false")]
			trace = extractTrace(spec[2:])
			yield (specdesc, trace)
		else:
			specdesc = specdesc[len("-- specification "):][:-len(" is true")]
			yield (specdesc, None)

# Parse NuSMV errors
def parseErrors(smvoutput):
	smvlines = smvoutput.split("\n")
	smvlines = map(lambda x: x.strip(), smvlines)

	actualOutput = dropwhile(ispreamble, smvlines)

	lines = []
	# find all occurrences of "line [0-9]+:" and get the line numbers
	for line in actualOutput:
		m = re.search('line ([0-9]+): (.*)$', line)
		if m:
			lineNo = int(m.group(1))
			msg = m.group(2)
			lines.append((lineNo, msg))
	return sorted(list(set(lines)))

def ispreamble(line):
	return "***" in line or "WARNING" in line or "NuSMV" in line

def isspecification(line):
	return line.startswith("-- specification")

# Parse the XML trace and create Node/Transition objects. Returns the first Node.
def extractTrace(speclines):
	trace = "".join(speclines)
	xmldoc = minidom.parseString(trace)

	loops = xmldoc.getElementsByTagName("loops")
	if len(loops) > 0:
		loops = loops[0].firstChild.nodeValue
		loops = map(lambda x: x.strip(), loops.split(","))

	nodes = xmldoc.getElementsByTagName("node")
	prevTransition = None
	for node in nodes:
		tracenode = Node()
		tracenode.variables = []
		tracenode.transition = None

		state = node.getElementsByTagName("state")[0]
		tracenode.isloopstart = state.attributes["id"].value.strip() in loops
		transition = node.getElementsByTagName("input")

		variables = state.getElementsByTagName("value")
		for var in variables:
			tracenode.variables.append((var.attributes["variable"].value, var.firstChild.nodeValue))

		if prevTransition:
			prevTransition.nextNode = tracenode
		else:
			res = tracenode

		if len(transition) > 0:
			transition = transition[0]
			tracenode.transition = Transition()
			tracenode.transition.process = transition.firstChild.firstChild.nodeValue
			prevTransition = tracenode.transition

	return res

# Split lists at points where a proposition is true
def splitAt(prop, lst):
	res = []
	chunk = []
	for item in lst:
		if prop(item) and len(chunk) > 0:
			res.append(chunk)
			chunk = []
		chunk.append(item)
	if len(chunk) > 0:
		res.append(chunk)
	return res
