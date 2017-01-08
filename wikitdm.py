import os

import nltk
import nltk.data
#from nltk.tag.perceptron import PerceptronTagger
from nltk.probability import FreqDist

#Set tokenizers, tagger and stemmer
tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
sentTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = nltk.stem.snowball.EnglishStemmer()
#tagger = PerceptronTagger()

import pandas as pd
import string
import re

os.chdir('/Users/Seth/Documents/wikitdm/')

punctuation = set(string.punctuation)

def rawToTokenList(rawData):
    textList=nltk.word_tokenize(rawData)
    tokenList=[]
    for token in textList:
        try:
            #tokenList.append(str(token))
            #tokenList.append(unicode(token)) #### changed this to get rid of most CODEC ERRORs
            thisToken = unicode(token)
            uselessUnicode = [u'\u2013', u'\u201d'] ### don't include these when they are alone
            if thisToken not in uselessUnicode:
                thisToken = thisToken.replace(u'\u201d','') # delete this (unicode quote)
                tokenList.append(thisToken)
        except:
            tokenList.append('**CODEC_ERROR**')
            # #######################prints word on CODEC ERROR
            print('**CODEC_ERROR**')
            print(token) 
            print('****')
    return tokenList

def cleanTokens(tokenList):
    #Convert all text to lower case
    textList=[word.lower() for word in tokenList]
    
    #Remove punctuation
    textList=[word for word in textList if word not in punctuation]
    textList=["".join(c for c in word if c not in punctuation) for word in textList ]
    
    #convert digits into NUM
    textList=[re.sub("\d+", "NUM", word) for word in textList]  
    
    #Stem words 
    textList=[stemmer.stem(word) for word in textList]
    
    #Remove blanks
    textList=[word for word in textList if word!= ' ']
    textList=[word for word in textList if word!= '']
    
    #Extract tokens
    return textList

def drop_pronouns(textList):
    #print(textList)
    try:
        tags = tagger.tag(textList)
    except:
        print("%%%%%%\n!!!!!!!!!!!\nTAGGER FAILED\n!!!!!!!!!!!\n%%%%%%")
        print(textList)
        return textList
    keep = []
    for i in range(0,len(textList)):
        if (tags[i][1] != 'PRP') & (tags[i][1] != 'PRP$'):
            #pronouns.append(tags[i][0])
            keep = keep + [i]
    return [textList[i] for i in keep]

class lingualObject(object):

    def __init__(self, fileName):
		#Define parameters
		self.fileName=fileName

		self.idfFile = 'wiki-test-5-IDF.csv'
		self.idf = pd.read_csv(self.idfFile)
		self.idf = self.idf.set_index('term')


		######################
		###Get text objects###
		######################

		#define rawText, tokens, sentences, and judgements
		self.rawText={}
		self.tokens={}
		#self.sentences={}
		#self.judgements={}
		#self.pronoun_sentences={}
		#self.keyword_pronouns_sentences ={}
		#self.pronounCols = ['nous', 'vous', 'je', 'ils', 'il', 'elle', 'le']

		#set the groupId
		#path = fileName
		#path = path.split('/')
		#self.group = path[path.index('raw')-1]

		#Extract raw text and update for encoding issues            
		rawData=unicode(open(fileName).read(), "utf-8", errors="ignore")

		# tokenize and stem
		tokenList = rawToTokenList(rawData)
		txtString=' '.join(tokenList)
		self.rawText=txtString

		#Break text into sentences and extract as sentences
		#sentList=list(sentTokenizer.tokenize(txtString))
		#self.sentences[fileName]=sentList

		#Extract tokens
		self.tokens=cleanTokens(tokenList)
 

    def getKeywords(self, wordCount):
	    startCount = 0
	    # get all tokens for the fileName
	    #all_words = []
	    #for toke in self.tokens.values():
	    #    all_words = all_words + toke
	    all_words = self.tokens


	    ## create FreqDF with word frequencies from fileName
	    freq = FreqDist(all_words) 
	    columns_obj = ["term", "freq"]
	    freqDF = pd.DataFrame(freq.items(), columns=columns_obj) # convert it to a data frame
	    #freqDF = freqDF.set_index('term')

	    ## drop the pronouns
	    terms = freqDF['term'].values.tolist()
	    
	    #if noPro = T:
	    	#keepers = drop_pronouns(terms[1:])
	    #else:
	    keepers = terms
	    freqDF = freqDF.set_index('term')
	    freqDF = freqDF.ix[keepers]
	    
	    ## merge freqDF with idf data frame
	    freqit = freqDF.join(self.idf[['idf', 'logidf']])
	    # replace null values with max
	    maxidf = max(freqit['idf'].dropna())
	    maxlogidf = max(freqit['logidf'].dropna())
	    freqit.loc[pd.isnull(freqit['idf']), 'idf'] = maxidf
	    freqit.loc[pd.isnull(freqit['logidf']), 'logidf'] = maxlogidf

	    ## create tfidf columns
	    freqit['tfidf'] = freqit['freq'] * freqit['idf']
	    freqit['logtfidf'] = freqit['freq'] * freqit['logidf']

	    ## order by tfidf weight
	    freqit = freqit.sort_values(by='tfidf', ascending=False) 

	    #filter out codecerror
	    keyslist = freqit.iloc[startCount:wordCount+startCount].index.tolist()
	    keywords = []
	    for word in keyslist:
	        if (word != 'codecerror') & (word != ''):
	            keywords = keywords + [word]

	    ##
	    self.keywords = keywords

    def wikitfidf(self, log = True):
        startCount = 0
        # get all tokens for the fileName
        #all_words = []
        #for toke in self.tokens.values():
        #    all_words = all_words + toke
        all_words = self.tokens


        ## create FreqDF with word frequencies from fileName
        freq = FreqDist(all_words) 
        columns_obj = ["term", "freq"]
        freqDF = pd.DataFrame(freq.items(), columns=columns_obj) # convert it to a data frame
        #freqDF = freqDF.set_index('term')

        ## drop the pronouns
        terms = freqDF['term'].values.tolist()
        
        #if noPro = T:
            #keepers = drop_pronouns(terms[1:])
        #else:
        keepers = terms
        freqDF = freqDF.set_index('term')
        freqDF = freqDF.ix[keepers]
        
        ## merge freqDF with idf data frame
        freqit = freqDF.join(self.idf[['idf', 'logidf']])
        # replace null values with max
        maxidf = max(freqit['idf'].dropna())
        maxlogidf = max(freqit['logidf'].dropna())
        freqit.loc[pd.isnull(freqit['idf']), 'idf'] = maxidf
        freqit.loc[pd.isnull(freqit['logidf']), 'logidf'] = maxlogidf

        ## create tfidf columns
        freqit['tfidf'] = freqit['freq'] * freqit['idf']
        freqit['logtfidf'] = freqit['freq'] * freqit['logidf']

        ## order by tfidf weight
        freqit = freqit.sort_values(by='tfidf', ascending=False) 

        '''
        #filter out codecerror
        keyslist = freqit.iloc[startCount:wordCount+startCount].index.tolist()
        keywords = []
        for word in keyslist:
            if (word != 'codecerror') & (word != ''):
                keywords = keywords + [word]

        ##
        self.keywords = keywords
        '''
        if log == True:
            #print(freqit[['logidf']])
            return freqit[['logtfidf']]
        else:
            return freqit[['tfidf']]

def wikitdm(textDir, log = True):
    #
    dflist = []

    # clean out non .txt files
    filenames = [filename for filename in os.listdir(textDir) if ".txt" in filename]
    print(filenames)

    # loop through each document in the folder
    for filename in filenames:
        # get the tfidf for that doc
        lo = lingualObject(textDir + '/' + filename)
        docdf = lo.wikitfidf(log = log)
        # rename column as filename
        try:
            docdf.rename(columns={'logtfidf':filename}, inplace=True)
        except:
            docdf.rename(columns={'tfidf':filename}, inplace=True)
        # print top 5 keywords and shape (to see number of total unique words)
        print(docdf.head())
        print(docdf.shape)
        # append to master list of document df's
        dflist.append(docdf)
    # concatenate all document df's into master df
    df = pd.concat(dflist, axis = 1)
    #print(df)
    return df