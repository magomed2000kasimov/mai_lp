from pyparsing import *

module_name = Word(alphas + '_')														
full_module_name = (module_name + ZeroOrMore(Suppress('.') + module_name))('modules')	
import_as = (Optional(Suppress('as') + module_name))('import_as')						

parse_module = (Suppress('import') + full_module_name + import_as).setParseAction(lambda t: {'import': t.modules.asList(), 'as': t.import_as.asList()[0]})

s = 'import matplotlib.pyplot as plt'

res = parse_module.parseString(s).asList()

print(res)
rFile = open("fam.ged", "r",encoding="UTF-8")			
wFile = open("famres.pl", "w")	


mag = {} 


for line in rFile:
	if line[3] == 'I' and line[0] == '0' :
		personID = line[2:11]
	elif line[2:6] == 'GIVN':
		personName = line[7:].rstrip()
	elif line[2:6] == 'SURN':
		personSurname = line[7:].rstrip()
		fullName = personName + ' ' + personSurname
	elif line[2:7] == 'SEX M':
			wFile.write('male(' + '\'' + fullName + '\'' + ').\n')


wFile.write('\n')
rFile.seek(0)

for line in rFile:
	if  line[3] == 'I' and line[0] == '0':
		personID = line[2:11]
	elif line[2:6] == 'GIVN':
		personName = line[7:].rstrip()
	elif line[2:6] == 'SURN':
		personSurname = line[7:].rstrip()
		fullName = personName + ' ' + personSurname
		
		mag[personID] = fullName
	elif line[2:7] == 'SEX F':
			wFile.write('female(' + '\'' + fullName + '\'' + ').\n')


wFile.write('\n')
rFile.seek(0)

for line in rFile:
	if line[3] == 'F' and line[0] == '0' :
		for human in rFile:
			if human[2] == 'H':
				husb = mag[human[7:16]]
			elif human[2] == 'W':
				wife = mag[human[7:16]]
			elif human[2] == 'C':
				child = mag[human[7:16]]
				wFile.write('parents(' + '\'' + child + '\'' + ',' + '\'' + husb + '\'' + ',' + '\'' + wife + '\'' + ').\n')

rFile.close()
wFile.close()
