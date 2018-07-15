from math  import log

def calcShannonEnt(dataSet):
	numEntries = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:
		#print (featVec)
		currentLabel = featVec[-1]
		#print (currentLabel)
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel]=0
		labelCounts[currentLabel] +=1
	shannonEnt = 0.0
	#print (labelCounts)
	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries
		shannonEnt -= prob*log(prob,2)
	return shannonEnt

def createDataSet():
	dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
	labels = ['no surfacing','flippers']
	return dataSet,labels

def splitDataSet(dataSet,axis,value):
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis]==value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet

def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0])-1
	bastEntropy = calcShannonEnt(dataSet)
	bastInfoGain = 0.0
	bastFeature = -1
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet,i,value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy +=prob * calcShannonEnt(subDataSet)
		infoGain = bastEntropy - newEntropy
		if infoGain>bastInfoGain:
			bastInfoGain = infoGain
			bastFeature = i
	return bastFeature

def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] +=1
	sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0]

def createTree(dataSet,labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0])==len(classList):
		return classList[0]
	if len(dataSet[0])==1:
		return majorityCnt(classList)
	bastFeat = chooseBestFeatureToSplit(dataSet)
	bastFeatLabel = labels[bastFeat]
	myTree = {bastFeatLabel:{}}
	del(labels[bastFeat])
	featValues = [example[bastFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bastFeatLabel][value]=createTree(splitDataSet(dataSet,bastFeat,value),subLabels)
	return myTree


if __name__=='__main__':
	dataSet,labels = createDataSet()
	print (dataSet,labels)
	#shannonEnt = calcShannonEnt(dataSet);
	#print shannonEnt;

	#splitData1 = splitDataSet(dataSet,0,1)
	#print splitData1

	#splitData2 = splitDataSet(dataSet,0,0)
	#print splitData2

	#bastFeature = chooseBestFeatureToSplit(dataSet)
	#print bastFeature

	#featVec = majorityCnt(dataSet)
	#print featVec

	myTree = createTree(dataSet,labels)
	print (myTree)
