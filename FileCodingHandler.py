import os


def encoder(type, path):
    outputContent = ""

    if "f" in type:
        outputContent = outputContent + "f\n" + path + "\n" + fileEncoder(path) + "\nfinish"

    elif "d" in type:
        outputContent = outputContent + "d"
        outputContent = outputContent + directoryEncoder(path) + "\nfinish"

    return outputContent


def directoryEncoder(path):
    outputContent = ""
    for fileName in os.listdir(path):
        if os.path.isfile(path + "/" + fileName):
            tmpPath = path + "/" + fileName
            #todo : use decoder() as an internal peace of code ,not an external func
            outputContent = outputContent + "\n" + tmpPath + "\n" + fileEncoder(tmpPath)
        else:
            outputContent = outputContent + directoryEncoder(path + "/" + fileName)
    return str(outputContent)


def fileEncoder(path):
    outputContent = ""
    blockSize = os.path.getsize(path)
    with open(path, "rb") as sourceFile:
        while True:
            contents = sourceFile.read(blockSize)
            if not contents:
                break
            outputContent = outputContent + str(contents)
    return outputContent


def decoder(messageBody, basePath):
    bodyList = str(messageBody).split("\n")
    print(bodyList)
    recievedFiles = {}
    if "f" in bodyList[0]:
        recievedFiles[bodyList[1]] = bodyList[2]

    elif "d" in bodyList[0]:
        counter = 1
        while True:
            if "finish" in bodyList[counter]:
                break
            recievedFiles[bodyList[counter]] = bodyList[counter + 1]

            counter += 2
    for key in recievedFiles.keys():
        print(basePath + "/" + "/".join(key.split('/')[0:-1]))
        try:
            os.makedirs(basePath + "/" + "/".join(key.split('/')[0:-1]))
            # print("Exist")
            # print("path   :  ", basePath + "/" + key)
            # print("in  :  ", recievedFiles[key])
            # print(type(recievedFiles[key]))
            f = open(basePath + "/" + key, "wb")
            f.write(recievedFiles[key].encode("utf-8"))
            f.close()
        except FileExistsError:
            # print("NotExist")
            # print("path   :  ", basePath + "/" + key)
            # print("in  :  ", recievedFiles[key])
            # print(type(recievedFiles[key].encode("utf-8")))
            f = open(basePath + "/" + key, "wb")

            f.write(recievedFiles[key].encode("utf-8"))
            f.close()


decoder(encoder("d", "dir"), "tmp")

