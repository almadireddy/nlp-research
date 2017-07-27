import json

data = []
with open('data/reviews_Electronics_5.json') as f:
    iterator = 0
    lastAsin = "0528881469"
    tmp = []
    trainFile = open("unfilteredGen.txt", "a")
    totalLength = 0

    usedAsins = []

    for line in f:
        if totalLength < 1000:
            data.append(json.loads(line))
            currentAsin = json.dumps(data[iterator]["asin"])

            if currentAsin == lastAsin and currentAsin not in usedAsins:
                tmp.append(json.dumps(data[iterator]))
                lastAsin = currentAsin

                if len(tmp) >= 20:
                    usedAsins.append(currentAsin)

                    for item in tmp:
                        trainFile.write(str(item).encode(encoding='UTF-8', errors='strict') + "\n")
                    totalLength += len(tmp)
                    del tmp[:]

            elif len(tmp) < 20:
                del tmp[:]
                lastAsin = currentAsin

            iterator += 1
