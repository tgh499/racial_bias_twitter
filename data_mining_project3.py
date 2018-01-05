import tweepy
import json
import csv
import pandas as pd
import re
from _operator import pos
from jedi.parser.tokenize import number

### Using StreamListener class for collecting the tweets.
class listener(tweepy.StreamListener):
        def on_data(self, data):
                global n ### Since we have to use this variable in main function, we set it as global varible.
                if (n < count):
                    #print (data)
                    status = json.loads(data)
                    try:
                        try:
                            with open('tweets.csv', 'a+',newline='') as f: ### Create a csv file which will contain streamed tweets.
                                writer = csv.writer(f)
                                writer.writerow([status['user']['screen_name'],status['created_at'], status['user']['location'], status['favorite_count'], status['retweet_count'], status['text']])
                            #print (status['user']['screen_name'],status['created_at'], status['user']['location'], status['favorite_count'], status['retweet_count'], status['text'],"\n")
                            #print ('')
                            n += 1 ### If only the tweets is collected without errors, increse the number of total colleted tweets.
                        except UnicodeEncodeError:
                            pass
                    except KeyError:
                        pass

                    return True

                else :
                    return False

        def on_error(self, status):
            print('error : ', status)

def printss():
    print("Hello")

'''
Given a list of strings, the follwoing subroutine outputs the frequency of each item in the list.
input: list
output: dictionary

example: input: ['a', 'a', 'b']
output: {('a':2), ('b':1)}
'''

def frequencyCounter(ArrayOfStrings):
    #print(type(ArrayOfStrings[2]))
    dictionary = {}
    regex = re.compile('[^a-zA-Z$]')
    for items in ArrayOfStrings:
        temp = items.split()
        for i in temp:
            i = regex.sub('', i)
            if i not in dictionary.keys():
                 dictionary[i] = 1
            else:
                dictionary[i] += 1
    return(dictionary)


'''
This subroutine calculates the total number of different words in the dictionary.
input: dictionary
output: count, which is an int variable.
'''
def totalNumberOfDifferentWords(dictionary):
    count = 0
    for i in dictionary.values():
        count = count + int(i)
    return count


'''
The following subroutine is called by the determinePolarity subroutine.
This simply calculates the probability of words according to Naive Bayes Classifier.
input: dictionary, size of dictionary, differentWords in dictionary, test string
output: probability of the words occuring. It'a a single float variable.
'''
def classifierForPolarity(dictionary, totalSize, differentWords, strings):
    regex = re.compile('[^a-zA-Z$]')
    wordList = strings.split()
    divider = differentWords + totalSize
    count = 1
    probabilityList = []
    for i in wordList:
        i = regex.sub('', i)
        if str(i) in dictionary.keys():
            temp = dictionary[str(i)]
            count += int(temp)
        else:
            count = count
        classify = count / divider
        probabilityList.append(classify)
        classify = 0
        count = 1
    totalProb = 1
    for i in probabilityList:
        totalProb = totalProb * i
    return(totalProb*0.5)


'''
This subroutine is called by the main program. It uses all available lists, dictionaries and other
data to determine the polarity of a tweet.
Probability of a tweet is calculated by the classifierForPolarity subroutine. Both the dictionaries
are used for this part.
Depending on which probability is larger, polarity of the tweet is determined.
If there is 50% or more similarity between the probabilities,
polarity is determined as neutral.
input: dictionries, lists, int variables
output: list
'''

def determinePolarity(dictEthnicity, dictReligion, dictSexualOrientation, dictOtherRacialBias, dictPositiveTweet, dictNeutralTweet, dictNegativeTweet, sizeOfEthnicity, sizeOfReligion, sizeOfSexualOrientation, sizeOfOtherRacialBias, sizeOfPositiveTweet, sizeOfNeutralTweet, sizeOfNegativeTweet, differentWordsInEthnicity, differentWordsInReligion, differentWordsInSexualOrientation, differentWordsInOtherRacialBias, differentWordsInPositiveTweet, differentWordsInNegativeTweet, differentWordsInNeutralTweet, arrayTestData):

    result = []
    regex = re.compile('[^a-zA-Z$]')

    tempCount = 0
    for i in arrayTestData:
        testString = str(i)
        probEthnicity = classifierForPolarity(dictEthnicity, sizeOfEthnicity, differentWordsInEthnicity, testString)
        probReligion = classifierForPolarity(dictReligion, sizeOfReligion, differentWordsInReligion, testString)
        probSexualOrientation = classifierForPolarity(dictSexualOrientation, sizeOfSexualOrientation, differentWordsInSexualOrientation, testString)
        probOtherRacialBias = classifierForPolarity(dictOtherRacialBias, sizeOfOtherRacialBias, differentWordsInOtherRacialBias, testString)
        probPositiveTweet = classifierForPolarity(dictPositiveTweet, sizeOfPositiveTweet, differentWordsInPositiveTweet, testString)
        probNeutralTweet = classifierForPolarity(dictNeutralTweet, sizeOfNeutralTweet, differentWordsInNeutralTweet, testString)
        probNegativeTweet = classifierForPolarity(dictNegativeTweet, sizeOfNegativeTweet, differentWordsInNegativeTweet, testString)

        temp = [tempCount, probEthnicity, probReligion, probSexualOrientation, probOtherRacialBias, probPositiveTweet, probNeutralTweet, probNegativeTweet]

        result.append(temp)
        temp = []
        tempCount += 1

    return(result)


'''
The following program sorts results of a 2d array based on a parameter.
'''
def sortResult(result, parameter):
    sortedTweets = sorted(result, key=lambda x: x[parameter], reverse=True)
    return(sortedTweets)


### Authentication details.
consumer_key = 'uAJx6MwKhYDMKamBrarSiGUTd'
consumer_secret = 'na8DAWlfuHSQllqVgcAcUtCSCblL6RtaFmvePFoA1fBUn03d1d'
access_token = '121692329-Q4fTuw0FmJeGkIHLnmxgX7u9ajpHiyIDrLwsnLVp'
access_token_secret = 'fA26olnFJH26y8t1tPOLXs7oXorHLrjyeSk5YKEokrSMX'
count = 0
n = 1


### was previously part of main program
print ("How many tweets do you want to collect?:")
### global count
count = int(input())
print ("Start to collect the tweets")

### Open the csv file saved streamed tweets.
with open('tweets.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["user_id","created_at","location","favorite_count","retweet_count","text"])

l = listener()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

### Set the keywords that related with racisim that we think and collect the tweets which contain at least one of the those keywords.
stream = tweepy.Stream(auth, l)
stream.filter(track=['racism','racist','racial','race','discrimination','black','white','skinhead', 'sexism', 'LGBT','lesbian','gay','bisexual','transgender', 'homophobia', 'male', 'female', 'misogynistic', 'asian', 'african american', 'hispanic', 'native american','christian','jew','muslim','hindu','buddhist','bigotry', 'prejudice','kkk','negro','honkie','chink','yankee','ethnic','unfairness','racialism','color-blind','segregation'])
#print("Program Finished")


pandaData = pd.read_csv('groundTruth.csv', encoding = "ISO-8859-1")
chosenColumns = [0,1,2]
arrayData = pandaData.as_matrix(columns = pandaData.columns[chosenColumns])


ethnicity = []
religion = []
sexualOrientation = []
otherRacialBias = []
positiveTweet = []
negativeTweet = []
neutralTweet = []

for i,j in enumerate(arrayData):
    if j[1] == 1:
        ethnicity.append(j[0])
    elif j[1] == 2:
        religion.append(j[0])
    elif j[1] == 3:
        sexualOrientation.append(j[0])
    elif j[1] == 4:
        otherRacialBias.append(j[0])

for i,j in enumerate(arrayData):
    if j[2] == 0:
        negativeTweet.append(j[0])
    elif j[2] == 1:
        neutralTweet.append(j[0])
    elif j[2] == 2:
        positiveTweet.append(j[0])

pandaTestData = pd.read_csv('tweets.csv',encoding = "ISO-8859-1")
chosenTestColumn = [5]
arrayTestData = pandaTestData.as_matrix(columns = pandaTestData.columns[chosenTestColumn])

#print(arrayTestData)

'''
The following code segment counts the frequency of the words.
input type: list
output type: dictionary
'''
dictEthnicity = frequencyCounter(ethnicity)
dictReligion = frequencyCounter(religion)
dictSexualOrientation = frequencyCounter(sexualOrientation)
dictOtherRacialBias = frequencyCounter(otherRacialBias)
dictPositiveTweet = frequencyCounter(positiveTweet)
dictNegativeTweet = frequencyCounter(negativeTweet)
dictNeutralTweet = frequencyCounter(neutralTweet)

'''
The following code segment counts the total number of words in
each dictionary.
'''
sizeOfEthnicity = totalNumberOfDifferentWords(dictEthnicity)
sizeOfReligion = totalNumberOfDifferentWords(dictReligion)
sizeOfSexualOrientation = totalNumberOfDifferentWords(dictSexualOrientation)
sizeOfOtherRacialBias = totalNumberOfDifferentWords(dictOtherRacialBias)
sizeOfPositiveTweet = totalNumberOfDifferentWords(dictPositiveTweet)
sizeOfNegativeTweet = totalNumberOfDifferentWords(dictNegativeTweet)
sizeOfNeutralTweet = totalNumberOfDifferentWords(dictNeutralTweet)


differentWordsInEthnicity = len(dictEthnicity)
differentWordsInReligion = len(dictReligion)
differentWordsInSexualOrientation = len(dictSexualOrientation)
differentWordsInOtherRacialBias = len(dictOtherRacialBias)
differentWordsInPositiveTweet = len(dictPositiveTweet)
differentWordsInNegativeTweet = len(dictNegativeTweet)
differentWordsInNeutralTweet = len(dictNeutralTweet)


result = determinePolarity(dictEthnicity, dictReligion, dictSexualOrientation, dictOtherRacialBias, dictPositiveTweet, dictNeutralTweet, dictNegativeTweet, sizeOfEthnicity, sizeOfReligion, sizeOfSexualOrientation, sizeOfOtherRacialBias, sizeOfPositiveTweet, sizeOfNeutralTweet, sizeOfNegativeTweet, differentWordsInEthnicity, differentWordsInReligion, differentWordsInSexualOrientation, differentWordsInOtherRacialBias, differentWordsInPositiveTweet, differentWordsInNegativeTweet, differentWordsInNeutralTweet, arrayTestData)

'''
sortedByEthnicity = sorted(result, key=lambda x: x[1], reverse=True)
sortedByReligion = sorted(result, key=lambda x: x[2], reverse=True)
sortedBySexualOrientation = sorted(result, key=lambda x: x[3], reverse=True)
sortedByOtherRacialBias = sorted(result, key=lambda x: x[4], reverse=True)
sortedByPositiveTweets = sorted(result, key=lambda x: x[5], reverse=True)
sortedByNeutralTweets = sorted(result, key=lambda x: x[6], reverse=True)
sortedByNegativeTweets = sorted(result, key=lambda x: x[7], reverse=True)
'''

print("How do you want to sort? \n 1 for Ethnicity \n 2 for Religion \n 3 for Sexual Orientation \n 4 for Other Racial Bias \n 5 for positive attitude \n 6 for neutral attitude \n 7 for negative attitude")

parameter = int(input())
sortedTweetsByParameter = sortResult(result, parameter)

with open('outputWithAllProbability.csv','w', newline='') as of:
    writer = csv.writer(of)
    writer.writerow(["user_id","ethnicity", "religion", "sexualOrientation", "OtherRacialBias", "Positive Attitude", "Neutral Attitude", "Negative Attitude"])
with open('outputWithAllProbability.csv', 'a+',newline='') as of:
    for i in sortedTweetsByParameter:
        print(i, file=of)

print("How many accounts do you want to find?")
numberOfAccounts = int(input())
userColumn = [0]
topAccountArray = pandaTestData.as_matrix(columns = pandaTestData.columns[userColumn])

tempList = []

for i in range(numberOfAccounts):
    tempList.append(sortedTweetsByParameter[i][0])

topAccountList = []

for i in tempList:
    temp = int(i)
    topAccountList.append(topAccountArray[temp][0])


with open('output.csv','w') as out_file:
  for i in topAccountList:
    print(i, file=out_file)

print("Please check the CSV file for the persons responsible. Thanks.")
