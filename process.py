import spacy
import os
import json

nlp = spacy.load('en')

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
        numberOfSyllables = 0
        numberOfWords = 0

        for sentence in processed.sents:
            numberOfSentences += 1
        output.append(numberOfSentences)

        for token in processed:
            if token.is_punct is False:
                numberOfWords += 1
        output.append(numberOfWords)

        print (output)

        processedOutput.append(numberOfSentences)

        reviewNumber += 1