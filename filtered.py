import json

data = []
with open('data/reviews_Electronics_5.json') as f:
    iterator = 0
    lastAsin = "0528881469"
    tmp = []
    trainFile = open("filteredGen.txt", "a")
    totalLength = 0

    usedAsins = []

    for line in f:
        if totalLength < 1000:
            data.append(json.loads(line))
            currentAsin = json.dumps(data[iterator]["asin"])

            if (currentAsin == lastAsin) and (currentAsin not in usedAsins):
                if data[iterator]["helpful"][0] >= 10:
                    tmp.append(data[iterator])
                lastAsin = currentAsin

                if len(tmp) >= 20:
                    usedAsins.append(currentAsin)

                    for item in tmp:
                        trainFile.write(json.dumps(item) + "\n")
                    totalLength += len(tmp)
                    del tmp[:]

            elif len(tmp) < 20:
                del tmp[:]
                lastAsin = currentAsin

            iterator += 1
