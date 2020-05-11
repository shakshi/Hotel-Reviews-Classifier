import sys
import os
import math
import string
import re
import operator

stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
"you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
"it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is',
'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
"should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
"shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

stopwords2= ["is", "that", "and", "this", "we", "i", "him", "her", "he", "she", "it", "the", 
    "hotel", "location", "of", "my", "were", "was", "is", "here", "there", "their", "a", "an", 
    "on", "as", "in", "with", "to", "am", "are", "had", "has", "have", "us", "them", "all", "our",
     "me", "you", "at", "your", "can", "could", "will", "would", "should", "shall", "for", "even", "why", "what", 
     "where", "when", "how", "pm", "so", "just", "himself", "herself", "myself", "yourself", "itself", "room",
      "hotel", "name", "however", "whatever", "whenever", "did", "do", "done", "towards", "around", "any", "rooms", "they", 
      "then", "if", "else", "from", "by", "or", "which", "also", "than", "hotels", "city", "went", "too", "trip", 
      "reservation", "I'll", "he'll", "be", "only", "ever", "intoupto", "must", "off", "one", "two", "three", "four", "five",
       "six", "seven", "eight", "nine", "up", "some", "been", "after", "before", "about", "other", "into", "affinia", "allegro",     "amalfi","ambassador", "conrad", "fairmont", "hardrock", "hilton", "homewood", "hyatt", "intercontinental", "james", "knickerbocker", "monaco", "omni", "palmer", "sheraton", "sofitel", "swissotel", "talbott", "out", "again", "his", "hers", "down", 
        "most", "night", "service"]

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
			w=  w.translate(table)
			if len(w) > 0:
					
				l.append(w)
	return l

# Read the model.txt 
f= open('nbmodel.txt', 'r')

total= int(f.readline())

count= [0,0,0,0]
count[0]= int(f.readline())
count[1]= int(f.readline())
count[2]= int(f.readline())
count[3]= int(f.readline())

wordcount=[0,0,0,0]
wordcount[0]= int(f.readline())
wordcount[1]= int(f.readline())
wordcount[2]= int(f.readline())
wordcount[3]= int(f.readline())


#print(count)
n= int(f.readline())

line = f.readline()
wordlist= {}
newwordlist={}

while line:
	x= line.split()
	word= x[0]

	wordlist[word] = [0,0,0,0,0]
	wordlist[word][0] = int(x[1])
	wordlist[word][1] = int(x[2])
	wordlist[word][2] = int(x[3])
	wordlist[word][3] = int(x[4])
	
	newwordlist[word] = (int(x[1]) + int(x[2]))
	line= f.readline()

lowfreq_words = sorted(newwordlist, key=newwordlist.get, reverse=True)[:20]


for x in lowfreq_words:
    print(x, newwordlist[x])

prior_pos= math.log(count[0]/total)
prior_neg = math.log(count[1]/total)
prior_truthful = math.log(count[2]/total)
prior_deceptive = math.log(count[3]/total)

#print(prior_pos, ' ', prior_neg, ' ', prior_truthful, ' ', prior_deceptive)

out= open('nboutput.txt', 'w')

dir_path= sys.argv[1]
# it contains folder - positve/negative polarity - masked

for folder in os.listdir(dir_path):

	folder_path= dir_path + '/' + folder

	if os.path.isdir(folder_path):

		#it contains folder deceptive or truthful - masked
		for inner_folder in os.listdir(folder_path):
			
			# it contains folders named folds 
			inner_path= folder_path + '/' + inner_folder

			if os.path.isdir(inner_path):

				for fold in os.listdir(inner_path):
					
					fold_path= inner_path + '/' + fold
					if os.path.isdir(fold_path):
						#then it will contain files
						for filename in os.listdir(fold_path):
			
							# read the file 
							file_path= fold_path + '/'  + filename

							with open(file_path, encoding="latin-1") as f:
							
								prob_pos= prior_pos; 
								prob_neg= prior_neg
								prob_truthful = prior_truthful; 
								prob_deceptive= prior_deceptive

								content = f.read()
								words = tokenize(content)

								for word in words:
									if word not in stopwords2:

										if word in wordlist:
											num= wordlist[word]

											'''
											if word count in truthful and deceptive is almost same 
											does not contribute to the prob 
											thus ignore
											if diff will contribute 
											same for positive and negative
											'''
											tmp= wordcount[0]+ wordcount[1]

											if tmp > 2:
												prob_pos += math.log(num[0] + 1 ) - math.log(wordcount[0]+ n) 
												prob_neg += math.log(num[1] + 1)  - math.log(wordcount[1]+ n) 
												prob_truthful += math.log(num[2] + 1 )- math.log(wordcount[2]+ n)  
												prob_deceptive += math.log(num[3] + 1)- math.log(wordcount[3]+ n) 
											
								#print(prob_pos, ' ', prob_neg)
								#print(prob_truthful, ' ', prob_deceptive)	

								if prob_truthful > prob_deceptive:
									out.write("truthful ")
								else:
									out.write("deceptive ")

								if prob_pos > prob_neg:
									out.write("positive ")
								else:
									out.write("negative ")

								out.write(file_path + '\n')

out.close()
