from nltk.tokenize import TweetTokenizer
from collections import defaultdict
from collections import deque
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#sentence start, use all end punctuation
#

class MarkovLearner():

    SENTENCE_END = ['?', '.', '!']
    SENTENCE_NO_SPACE = [',', ';', ':', '?', '.', '!']
    SENTENCE_ALL_PUNCTUATION = [',', ';', ':', '?', '.', '!', '/', '...', '(', ')', '<', '>', '[', ']', '-', '{', '}', "'", '"']
    #tokens
    #sentenceStartWords
    #nextTermFrequency

    def __init__(self, fileName, length = 1):
        self.length = length
        self.fileName = fileName
        self.train(fileName)

    '''
    Take in a file and train the markov chain with it
    '''
    def train(self, fileName):
        
        tokens = self.tokenizeFile(fileName)
        self.tokens = tokens
        #print('TOkens: ' + str(self.tokens))
        self.saveSentenceStarts()
        #print(self.tokens)
        nextTermFrequency = dict()

        lengthCounter = 0
        present = deque()
        future = None
        for token in tokens:

            if (lengthCounter < self.length):
                present.append(token)
                lengthCounter += 1
            else:
                future = token
                presentTuple = self.convertToTuple(present)
                if (presentTuple not in nextTermFrequency):
                    nextTermFrequency[presentTuple] = dict()
                nextTermFrequency[presentTuple][future] = nextTermFrequency[presentTuple].get(future, 0) + 1
                present.popleft()
                present.append(future)

        #print(str(nextTermFrequency))
        for presentTokenKey in nextTermFrequency.keys():
            futureTokenFrequency = nextTermFrequency[presentTokenKey]
            frequencySum = sum(futureTokenFrequency.values())
            for futureTokenKey in futureTokenFrequency:
                futureTokenFrequency[futureTokenKey] = futureTokenFrequency[futureTokenKey] / float(frequencySum)

        self.nextTermFrequency = nextTermFrequency
        #print(nextTermFrequency['"'])

    '''
    Deques can't be hashed since they are mutable
    '''
    def convertToTuple(self, myDeque):
        return tuple(myDeque)

    '''
    Store all word chains that start a sentence (ie follow a .)
    '''
    def saveSentenceStarts(self):
        window = deque()
        sentenceStartWords = []
        lengthCounter = 0
        foundEnd = False
        for token in self.tokens:
            if (lengthCounter < self.length):
                window.append(token)
                lengthCounter += 1
                if (lengthCounter == self.length):
                    if ('.' not in window):
                        sentenceStartWords.append(list(window))
                    else:
                        foundEnd = True
            else:
                window.popleft()
                window.append(token)
                if (foundEnd):
                    if ('.' not in window):
                        sentenceStartWords.append(list(window))
                        foundEnd = False
                else:
                    if ('.' in window):
                        foundEnd = True                        

        self.sentenceStartWords = sentenceStartWords
        #print("sentence start words: " + str(sentenceStartWords[:25]))

    #def containsInterme

    '''
    Take in a file name and spit out all the tokens in a list
    '''
    def tokenizeFile(self, fileName):
        tokenizer = TweetTokenizer()
        
        fileString = ''
        with open(fileName, 'r') as wordFile:
            fileString = wordFile.read().replace('\n', ' ')

        return [token for token in tokenizer.tokenize(fileString) if token != "'" and token != '"' and token != 'Â']

    '''
    Generates the next token in the sentence given the current state
    '''
    def getNextToken(self, currentState):
        futureTokenFrequency = self.nextTermFrequency[currentState]
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
    def generateSentence(self):

        sentence = ''
        randomStart = self.getRandomStart()
        for startingToken in randomStart:
            if (startingToken in self.SENTENCE_NO_SPACE):
                sentence += startingToken
            else:
                sentence += ' ' + startingToken
            if (startingToken in self.SENTENCE_END):
                return sentence
        currentWindow = deque(randomStart)
        nextToken = None
        while (nextToken not in self.SENTENCE_END):
            nextToken = self.getNextToken(self.convertToTuple(currentWindow))
            if (nextToken in self.SENTENCE_NO_SPACE):
                sentence += nextToken
            else:
                sentence += ' ' + nextToken
            currentWindow.popleft()
            currentWindow.append(nextToken)

        return sentence

    '''
    Gets a random start to a sentence
    '''
    def getRandomStart(self):

        done = False
        foundStart = []

        while (not done):
            foundStart = random.choice(self.sentenceStartWords)
            if (foundStart[0] not in self.SENTENCE_ALL_PUNCTUATION):
                done = True
        #print("random start: " + str(foundStart))
        return foundStart

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

    '''
    Generate a word cloud of the provided text
    '''
    def generateWordCloud(self):

        # Generate a word cloud image
        plt.imshow(WordCloud().generate(open(self.fileName).read()))
        plt.axis("off")
        plt.show()



if __name__ == "__main__":

    LENGTH = 2

    gen = MarkovLearner("text/HuckleberryFin.txt", length=LENGTH)

    outputFile = open('random_huckleberry.txt', 'w')
    iterations = 10
    for x in range(iterations):
        outputFile.write(gen.generateParagraph() + '\n')
    outputFile.close()
    gen.generateWordCloud()

    '''
    gen = MarkovLearner("text/JustinBieber.txt", length=LENGTH)

    outputFile = open('random_bieber.txt', 'w')
    iterations = 10
    for x in range(iterations):
        outputFile.write(gen.generateParagraph() + '\n')
    outputFile.close()

    gen = MarkovLearner("text/ProblemsOfPhilosophy.txt", length=LENGTH)

    outputFile = open('random_philosophy.txt', 'w')
    iterations = 10
    for x in range(iterations):
        outputFile.write(gen.generateParagraph() + '\n')
    outputFile.close()
    '''

    gen = MarkovLearner("text/DonaldTrumpTwitter.txt", length=LENGTH)

    outputFile = open('random_trump_twitter.txt', 'w')
    iterations = 10
    for x in range(iterations):
        outputFile.write(gen.generateParagraph() + '\n')
    outputFile.close()
    