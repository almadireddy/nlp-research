import spacy
import json
from textstat.textstat import textstat
import enchant

nlp = spacy.load('en')
dictionary = enchant.Dict('en_US')
reviews = []
processedOutput = []

with open('generated/filteredTrainingData.json', 'r') as data:
    reviewNumber = 0

    for line in data:
        reviews.append(json.loads(line))
        reviewText = reviews[reviewNumber]['reviewText']
        output = []

        processedReview = nlp(reviewText)

        numberOfSentences = 0
        numberOfWords = 0
        numberOfSpellingErrors = 0.0

        # Number of Sentences
        for sentence in processedReview.sents:
            numberOfSentences += 1

        # Number of Words and Spelling Errors
        for token in processedReview:
            if token.is_punct is False:
                numberOfWords += 1

            if dictionary.check(token) is False and token.is_punct is False and str(token) != "$":
                numberOfSpellingErrors += 1.0

        spellingErrorToWordRatio = numberOfSpellingErrors / numberOfWords

        # TF-IDF Statistic


        # Flesch Kincaid Reading Grade
        readingScore = textstat.flesch_kincaid_grade(reviewText)

        # Star Rating
        starRating = reviews[reviewNumber]["overall"]

        # Output construction
        output.append(numberOfSentences)
        output.append(numberOfWords)
        output.append(readingScore)
        output.append(spellingErrorToWordRatio)
        output.append(int(starRating))

        print (output)
        reviewNumber += 1
