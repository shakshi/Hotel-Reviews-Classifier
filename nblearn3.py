import sys
import os
import string
import re

ans={}
wordlist={}

# Read data 
dir_path= sys.argv[1]

stopwords2= ["is", "that", "and", "this", "we", "i", "him", "her", "he", "she", "it", "the", 
    "hotel", "location", "of", "my", "were", "was", "is", "here", "there", "their", "a", "an", 
    "on", "as", "in", "with", "to", "am", "are", "had", "has", "have", "us", "them", "all", "our",
     "me", "you", "at", "your", "can", "could", "will", "would", "should", "shall", "for", "even", "why", "what", 
     "where", "when", "how", "pm", "so", "just", "himself", "herself", "myself", "yourself", "itself", "room",
      "hotel", "name", "however", "whatever", "whenever", "did", "do", "done", "towards", "around", "any", "rooms", "they", 
      "then", "if", "else", "from", "by", "or", "which", "also", "than", "hotels", "city", "went", "too", "trip", 
      "reservation", "I'll", "he'll", "be", "only", "ever", "intoupto", "must", "off", "one", "two", "three", "four", "five",
       "six", "seven", "eight", "nine", "up", "some", "been", "after", "before", "about", "other", "into", "affinia", "allegro", "amalfi",
        "ambassador", "conrad", "fairmont", "hardrock", "hilton", "homewood", "hyatt", "intercontinental", "james", "knickerbocker", "monaco", 
        "omni", "palmer", "sheraton", "sofitel", "swissotel", "talbott", "out", "again", "his", 
        "hers", "down", "most", "night", "service"]


def tokenize(review):
	# get review 
	# return list of words

	# that are not stopwords and have punctuation removed 
	review= review.lower()
	pattern = '[0-9]'
	review = re.sub(pattern, '', review)
	review = re.sub(",", ' ', review)
	#review= re.sub("--", ' ', review)

	words= review.split()
	l=[]

	# we can try not removing '
	# only remove /,!. - 4 things 
	table = str.maketrans('', '', string.punctuation) 

	for w in words:
		if w not in stopwords2:
			w =  w.translate(table)
			if len(w) > 0:
				
				l.append(w)

	return l

count=[0,0,0,0]  # total count of each class
wordcount=[0,0,0,0]  # no of words in each class 
total=0 
'''
i need the count of no of words in positive reviews 
no of words in negative reviews

no of words in truthful reviews 
no of words in negative reviews
'''
def naiveBayes(path, class1, class2):

	global total
	#print(path)

	for folder_name in os.listdir(path):

		folder_path= path + '/' + folder_name
		if os.path.isdir(folder_path):
		
			for filename in os.listdir(folder_path):

				# increment reviewss 
				count[class1] += 1
				count[class2] += 1
				total+=1 

				# read the file 
				file_path= folder_path + '/'  + filename
				with open(file_path, 'r') as f:
					
					#print(file_path)	
					content = f.read()
					words = tokenize(content)

					for word in words:

						if word not in stopwords2:
							if word not in wordlist:
								wordlist[word] = [0,0,0,0]
							
							wordlist[word][class1] += 1
							wordlist[word][class2] += 1

							# this word is in class 1
							wordcount[class1] += 1
							wordcount[class2] += 1

							# this word is in class 2

positive_path = dir_path + "/positive_polarity"
negative_path  = dir_path + "/negative_polarity"

p1 = positive_path + "/truthful_from_TripAdvisor"
p2 = positive_path + "/deceptive_from_MTurk"

n1 = negative_path + "/truthful_from_Web"
n2 = negative_path + "/deceptive_from_MTurk"

naiveBayes(p1, 0, 2)
naiveBayes(p2, 0, 3)
naiveBayes(n1, 1, 2)
naiveBayes(n2, 1, 3)


f= open("nbmodel.txt", 'w')
f.write(str(total) + "\n")
f.write(str(count[0]) + "\n")
f.write(str(count[1]) + "\n")
f.write(str(count[2]) + "\n")
f.write(str(count[3]) + "\n")

f.write(str(wordcount[0]) + "\n")
f.write(str(wordcount[1]) + "\n")
f.write(str(wordcount[2]) + "\n")
f.write(str(wordcount[3]) + "\n")

n= len(wordlist)
f.write(str(n) + "\n")

for word in wordlist:
	c= wordlist[word]
	f.write(word + " ")
	f.write(str(c[0]) + " ")
	f.write(str(c[1]) + " ")
	f.write(str(c[2]) + " ")
	f.write(str(c[3]) + "\n")

f.close()