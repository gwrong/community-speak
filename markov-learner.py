from nltk.tokenize import TweetTokenizer
from collections import defaultdict
import random

class MarkovLearner():

    SENTENCE_END = ['?', '.', '!']
    SENTENCE_NO_SPACE = [',', ';', ':', '?', '.', '!']
    SENTENCE_ALL_PUNCTUATION = [',', ';', ':', '?', '.', '!', '/', '...', '(', ')', '<', '>', '[', ']', '-', '{', '}', "'", '"']
    #tokens
    #sentenceStartWords
    #nextTermFrequency

    def __init__(self, fileName):
        self.train(fileName)

    '''
    Take in a file and train the markov chain with it
    '''
    def train(self, fileName):
        
        tokens = self.tokenizeFile(fileName)
        self.tokens = tokens
        print('TOkens: ' + str(self.tokens))
        self.saveSentenceStartWords(tokens)
        #print(self.tokens)
        nextTermFrequency = dict()
        first = True

        present = None
        future = None
        for token in tokens:

            if (first):
                first = False
                present = token
            else:
                future = token
                if (present not in nextTermFrequency):
                    nextTermFrequency[present] = dict()
                nextTermFrequency[present][future] = nextTermFrequency[present].get(future, 0) + 1
                present = future

        for presentTokenKey in nextTermFrequency.keys():
            futureTokenFrequency = nextTermFrequency[presentTokenKey]
            frequencySum = sum(futureTokenFrequency.values())
            for futureTokenKey in futureTokenFrequency:
                futureTokenFrequency[futureTokenKey] = futureTokenFrequency[futureTokenKey] / float(frequencySum)

        self.nextTermFrequency = nextTermFrequency
        #print(nextTermFrequency['"'])

    '''
    Store all words that start a sentence (ie follow a .)
    '''
    def saveSentenceStartWords(self, tokens):
        prev = None
        current = None
        sentenceStartWords = []
        for token in self.tokens:
            current = token
            if ((prev == None or prev == '.') and current[0].isupper()):
                sentenceStartWords.append(current)
            prev = current
        self.sentenceStartWords = sentenceStartWords
        #print("sentence start words: " + str(sentenceStartWords))

    '''
    Take in a file name and spit out all the tokens in a list
    '''
    def tokenizeFile(self, fileName):
        tokenizer = TweetTokenizer()
        
        fileString = ''
        with open(fileName, 'r') as wordFile:
            fileString = wordFile.read().replace('\n', ' ')

        return [token for token in tokenizer.tokenize(fileString) if token != 'Â']

    '''
    Generates the next token in the sentence given the current state
    '''
    def getNextToken(self, currentWord):
        futureTokenFrequency = self.nextTermFrequency[currentWord]
        randomValue = random.random()
        nextToken = None
        runningSum = 0

        for tokenItem in futureTokenFrequency.items():
            runningSum += tokenItem[1]
            nextToken = tokenItem[0]
            if (runningSum > randomValue):
                break
        return nextToken

    '''
    Generate a sentence based on the trained corpus
    '''
    def generateSentence(self, startingWord = None):

        sentence = startingWord
        if (sentence == None):
            sentence = self.getRandomWord()
        currentToken = sentence
        nextToken = None
        while (nextToken not in self.SENTENCE_END):
            nextToken = self.getNextToken(currentToken)
            if (nextToken in self.SENTENCE_NO_SPACE):
                sentence += nextToken
            else:
                sentence += ' ' + nextToken
            currentToken = nextToken

        return sentence

    '''
    Gets a random word from the tokenized corpus
    '''
    def getRandomWord(self, sentenceStart = True):
        foundWord = '.'
        wordCorpus = None

        if (sentenceStart):
            wordCorpus = self.sentenceStartWords
        else:
            wordCorpus = self.tokens

        while (foundWord in self.SENTENCE_ALL_PUNCTUATION):
            foundWord = random.choice(wordCorpus)
        #print("random word: " + foundWord)
        return foundWord

    '''
    Generates a paragraph
    '''
    def generateParagraph(self):
        paragraph = None
        numSentences = random.randint(5, 15)
        for x in range(numSentences):
            if (paragraph == None):
                paragraph = self.generateSentence()
            else:
                paragraph += ' ' + self.generateSentence()
        return paragraph


if __name__ == "__main__":
    gen = MarkovLearner("HuckleberryFin.txt")

    outputFile = open('random_huckleberry.txt', 'w')
    iterations = 10
    for x in range(iterations):
        outputFile.write(gen.generateParagraph() + '\n')
    outputFile.close()