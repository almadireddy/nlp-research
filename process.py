import spacy
import os
import json
from textstat.textstat import textstat
import enchant

nlp = spacy.load('en')
dict = enchant.Dict('en_US')
reviews = []
processedOutput = []

with open('generated/filteredTrainingData.json', 'r') as data:
    reviewNumber = 0

    for line in data:
        reviews.append(json.loads(line))
        reviewText = reviews[reviewNumber]['reviewText']
        output = []

        processed = nlp(reviewText)

        numberOfSentences = 0
        numberOfWords = 0
        numberOfSpellingErrors = 0.0

        for sentence in processed.sents:
            numberOfSentences += 1
        output.append(numberOfSentences)

        for token in processed:
            if token.is_punct is False:
                numberOfWords += 1

            if dict.check(token) is False and token.is_punct is False and str(token) != "$":
                numberOfSpellingErrors += 1.0

        spellingErrorToWordRatio = numberOfSpellingErrors / numberOfWords

        output.append(numberOfWords)

        # numberOfSyllables = textstat.syllable_count(reviewText)
        # wordsPerSentence = numberOfWords / numberOfSentences
        # syllablesPerWord = numberOfSyllables / numberOfWords
        # readingScore = (0.39 * wordsPerSentence) + (11.8 * syllablesPerWord) - 15.59

        readingScore = textstat.flesch_kincaid_grade(reviewText)

        output.append(readingScore)

        output.append(spellingErrorToWordRatio)

        print (output)

        reviewNumber += 1