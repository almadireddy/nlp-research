import spacy
import json
from textstat.textstat import textstat
import enchant
import math

nlp = spacy.load('en')
dictionary = enchant.Dict('en_US')
reviews = []

with open('generated/filteredTrainingData.json', 'r') as data:
    reviewNumber = 0

    for line in data:
        reviews.append(json.loads(line))

    reviews = [reviews[i:i+20] for i in xrange(0, len(reviews), 20)]

    numOfGroups = len(reviews)
    numOfReviews = 20

    for group in range(0, numOfGroups):

        for i in range(0, 20):
            reviewText = reviews[group][i]["reviewText"]
            processedReview = nlp(reviewText)

            output = []

            numberOfSentences = 0
            numberOfWords = 0
            numberOfSpellingErrors = 0.0

            # Number of Sentences
            for sentence in processedReview.sents:
                numberOfSentences += 1

            unfilteredLemmaList = []
            filteredLemmaList = []

            # Number of Words and Spelling Errors
            for token in processedReview:
                if token.is_punct is False:
                    numberOfWords += 1
                    unfilteredLemmaList.append(token.lemma_)

                    if [token.lemma_] not in filteredLemmaList:
                        filteredLemmaList.append([token.lemma_])

                    if dictionary.check(token) is False and str(token) != "$":
                        numberOfSpellingErrors += 1.0

            spellingErrorToWordRatio = numberOfSpellingErrors / numberOfWords

            # TF-IDF Statistic

            # for lemma in unfilteredLemmaList:
            #     if [lemma] not in filteredLemmaList:
            #         filteredLemmaList.append([lemma])

            numberOfLemmas = float(len(filteredLemmaList))

            for lemma in filteredLemmaList:
                lemma.append(unfilteredLemmaList.count(lemma[0]))
                lemma.append(lemma[1] / numberOfLemmas)
                lemma.append(0)

                reviewLemmas = []

                for product in range(0, 20):
                    text = reviews[group][product]["reviewText"]
                    doc = nlp(text)

                    for t in doc:
                        reviewLemmas.append(t.lemma_)

                    if lemma[0] in reviewLemmas:
                        lemma[3] += 1
                        del reviewLemmas[:]
                        continue

                    del reviewLemmas[:]

                lemma.append(math.log10(20.0 / lemma[3]))

                lemma.append(lemma[2] * lemma[4])

                print lemma

            # Flesch Kincaid Reading Grade
            readingScore = textstat.flesch_kincaid_grade(reviewText)

            # Star Rating
            starRating = reviews[group][i]["overall"]

            # Output construction
            output.append(numberOfSentences)
            output.append(numberOfWords)
            output.append(readingScore)
            output.append(spellingErrorToWordRatio)
            output.append(int(starRating))

            print (output)
            print " "
            print " "
            print " "
            reviewNumber += 1
