#!/usr/bin/python
"""
Phantom User Generator

Andrew Morris
amorris[at]endgame com
morr.drew[at]gmail com

"""
import random 
import string
import argparse

try:
	import smbpasswd
except ImportError:
	print "[!] Error: pysmbpasswd module not found"
	print "[+] Download from here: https://code.google.com/p/py-smbpasswd/"
        print "[+] Or install with 'pip install smbpasswd'"
	exit()


######### Some global variables

firstNameFile = 'male-names.txt'
lastNameFile = 'last-names.txt'
shitty = ['welcome','changeme','12345','secret','qwerty','123456','aaaaaa','internet','asd123', 'root', 'admin']
commonSymbols = '!?@$&*+-' 
uncommonSymbols = '%^()"/<>~`[]{}|_'
emptyLM = 'AAD3B435B51404EEAAD3B435B51404EE'

def pass_Username(user):
	password = user+"1"
	return password

def pass_Password():
	password = "password"+str(random.randint(1,9))
	return password

def pass_DictWord(randomWords):
	password = random.choice(randomWords)+str(random.randint(1,99))
	return password

def pass_DictWord_Upper(randomWords): # I'll figure out a better way to do this later
	password = random.choice(randomWords)+str(random.randint(1,99))
	return password

# Let's get some real ass randomness up in here
def random_Password_ULDS(size=random.randint(5,12), chars=string.ascii_lowercase + string.ascii_uppercase + string.digits + commonSymbols): 
	return ''.join(random.choice(chars) for x in range(size))

def random_Password_ULD(size=random.randint(5,12), chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def random_Password_LD(size=random.randint(5,12), chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def random_ShittyWord():
	password = random.choice(shitty)
	return password

def blank_Password(): # Not really sure why I actually defined this function...
	password = ""
	return password

def pass_DictWord_DigitsFirst(randomWords):
	password = str(random.randint(1,99))+random.choice(randomWords)
	return password

def hunter2():
    password = "hunter2"
    return password

def generatePassword(username, randomWords):
    
    # Establish list of lists. In order: function obj, args (if any), count
    choices = [
        [pass_Username, username, 3],
        [pass_Password, None, 3],
        [pass_DictWord_DigitsFirst, randomWords, 6],
        [pass_DictWord, randomWords, 52],
        [random_Password_ULD, None, 10],
        [random_ShittyWord, None, 6],
        [random_Password_LD, None, 7],
        [blank_Password, None, 1],
        [hunter2, None, 1],
        [pass_DictWord_Upper, randomWords, 9],
        [random_Password_ULDS, None, 2]]

    # Add each list to the population based on its count
    population = []
    for obj in choices:
        for i in range(obj[2]):
            population.append(obj) #TODO: remove last item from list before adding

    # Pick randomly from the populatioin
    theChosen = random.choice(population)

    # Check whether our chosen function accepts an argument. If any of the password generation methods ever
    # required more than one argument this would break horribly. Maybe this should be a class
    if theChosen[1] is None:
        password = theChosen[0]()
    else:
        password = theChosen[0](theChosen[1])

    return password


def generateHashNTLM(username, randomWords):
    
    password = generatePassword(username, randomWords)
    try:
        print username+':'+str(random.randint(1000,2000))+'%s:%s:::' % (emptyLM, smbpasswd.nthash(password))
    except AttributeError:
        print username+':'+str(random.randint(1000,2000))+'%s:%s:::' % (smbpasswd.nthash(password))


def generateHashLM(username, randomWords):

    password = generatePassword(username, randomWords)
    print username+':'+str(random.randint(1000,2000))+':'+'%s:%s:::' % smbpasswd.hash(password)


def generatePlaintext(username, randomNumber, randomWords):
	if randomNumber <=3: # 3%
		password = pass_Username(username)
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=6: # 3%
		password = pass_Password()
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=12: # 6%
		password = pass_DictWord_DigitsFirst(randomWords)
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=64: # 52%
		password = pass_DictWord(randomWords)
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=74: # 10%
		password = random_Password_ULD()
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=80: # 6%
		password = random_ShittyWord()
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=87: # 7%
		password = random_Password_LD()
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=88: # 1%
		password = ""
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=89: # 1%
		password = "hunter2"
		print "[+] %s\t%s " % (username, password)
	elif randomNumber <=98: # 9%
		password = pass_DictWord_Upper(randomWords)
		try: 
			print "[+] %s\t%s " % (username, password)
		except AttributeError: # This is in case the word starts with something other than a letter
			print "[+] %s\t%s " % (username, password)
	elif randomNumber <=100: # 2%
		password = random_Password_ULDS()
		print "[+] %s\t%s " % (username, password)

def generateCmd(username, randomNumber, randomWords):
	if randomNumber <=3: # 3%
		password = pass_Username(username)
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=6: # 3%
		password = pass_Password()
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=12: # 6%
		password = pass_DictWord_DigitsFirst(randomWords)
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=64: # 52%
		password = pass_DictWord(randomWords)
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=74: # 10%
		password = random_Password_ULD()
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=80: # 6%
		password = random_ShittyWord()
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=87: # 7%
		password = random_Password_LD()
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=88: # 1%
		password = ""
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=89: # 1%
		password = "hunter2"
		print "net user %s %s /add" % (username, password)
	elif randomNumber <=98: # 9%
		password = pass_DictWord_Upper(randomWords)
		try: 
			print "net user %s %s /add" % (username, password)
		except AttributeError: # This is in case the word starts with something other than a letter
			print "net user %s %s /add" % (username, password)
	elif randomNumber <=100: # 2%
		password = random_Password_ULDS()
		print "net user %s %s /add" % (username, password)

def generateCmdDomain(username, randomNumber, randomWords):
	if randomNumber <=3: # 3%
		password = pass_Username(username)
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=6: # 3%
		password = pass_Password()
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=12: # 6%
		password = pass_DictWord_DigitsFirst(randomWords)
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=64: # 52%
		password = pass_DictWord(randomWords)
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=74: # 10%
		password = random_Password_ULD()
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=80: # 6%
		password = random_ShittyWord()
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=87: # 7%
		password = random_Password_LD()
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=88: # 1%
		password = ""
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=89: # 1%
		password = "hunter2"
		print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=98: # 9%
		password = pass_DictWord_Upper(randomWords)
		try: 
			print "net user %s %s /add /domain" % (username, password)
		except AttributeError: # This is in case the word starts with something other than a letter
			print "net user %s %s /add /domain" % (username, password)
	elif randomNumber <=100: # 2%
		password = random_Password_ULDS()
		print "net user %s %s /add /domain" % (username, password)

def generateUser(lastNames, firstNames):
	firstName = random.choice(firstNames)
	lastName = random.choice(lastNames)
	name = firstNames[0]+lastNames
	return name.lower()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--hashes', help='output password hashes in pwdump format', action='store_true', default=False, dest='hashes')
	parser.add_argument('--ntlm', help='include NTLM password hashes', action='store_true', default=False, dest='ntlm')
	parser.add_argument('--lm', help='include deprecated LM hashes', action='store_true', default=False, dest='lm')
	parser.add_argument('--count', help='amount of items to generate', type=int, action='store', default=10, dest='count')
	parser.add_argument('--first', help='file where first names are stored, default is data/male-names.txt', action='store', default="data/male-names.txt", dest='firstNameFile')
	parser.add_argument('--last', help='file where last names are stored, default is data/last-names.txt', action='store', default="data/last-names.txt", dest='lastNameFile')
	parser.add_argument('--wordlist', help="seed file for passwords to be generated from, default is data/word.lst", action='store', default="data/word.lst", dest='wordlistFile')
	parser.add_argument('--cmd', help="output username and password in 'net user jsmith password /add' format for use on Windows", action="store_true", default=False, dest='cmd')
	parser.add_argument('--cmd-domain', help="output username and password in 'net user jsmith password /add /domain' format for use on Windows AD", action="store_true", default=False, dest='cmdDomain')
	args = parser.parse_args()	

	try:
		with open(args.wordlistFile, 'r') as f:
			randomWords = [line.strip() for line in f]
	except IOError:
		print "[!] Error: Wordlist file not found: %s" % args.wordlistFile
		exit()
	
	try:
		with open(args.firstNameFile, 'r') as f:
			firstNames = [line.strip() for line in f]
	except IOError:
		print "[!] Error: First names file not found: %s" % args.firstNameFile
		exit()
	
	try:
		with open(args.lastNameFile, 'r') as f:
			lastNames = [line.strip() for line in f]
	except IOError:
		print "[!] Error: Last names file not found: %s" % args.lastNameFile
		exit()

	if args.hashes:
		for i in range(0, args.count):
			name = generateUser(random.choice(lastNames), random.choice(firstNames))
			#randomNumber = random.randint(0,100)
			if args.ntlm:
				generateHashNTLM(name, randomWords)
			if args.lm:
				generateHashLM(name, randomWords)
	elif args.cmd:
		for i in range(0, args.count):
			name = generateUser(random.choice(lastNames), random.choice(firstNames))
			randomNumber = random.randint(0,100)
			generateCmd(name, randomNumber, randomWords)
	elif args.cmdDomain:
		for i in range(0, args.count):
			name = generateUser(random.choice(lastNames), random.choice(firstNames))
			randomNumber = random.randint(0,100)
			generateCmdDomain(name, randomNumber, randomWords)		
	else:
		for i in range(0, args.count):
			name = generateUser(random.choice(lastNames), random.choice(firstNames))
			randomNumber = random.randint(0,100)
			generatePlaintext(name, randomNumber, randomWords)

if __name__ == "__main__":
	main()

