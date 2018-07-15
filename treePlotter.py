#coding=utf-8
import matplotlib.pyplot as plt
import trees as tree
plt.switch_backend('agg')
decisionNode = dict(boxstyle="sawtooth",fc="0.8")
leafNode = dict(boxstyle="round4",fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt,centerPt,parentPt,nodeType):
	createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPt,textcoords='axes fraction',va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)

def plotMidText(cntrPt,parentPt,txtString):
	xMid = (parentPt[0]-cntrPt[0])/2.0+cntrPt[0]
	yMid = (parentPt[1]-cntrPt[1])/2.0+cntrPt[1]
	createPlot.ax1.text(xMid,yMid,txtString)

def plotTree(myTree,parentPt,nodeTxt):
	numLeafs = getNumLeafs(myTree)
	depth = getTreeDepth(myTree)
	firstStr = list(myTree.keys())[0]
	cntrPt = (plotTree.x0ff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.y0ff)
	plotMidText(cntrPt,parentPt,nodeTxt)
	plotNode(firstStr,cntrPt,parentPt,decisionNode)
	secondDict = myTree[firstStr]
	plotTree.y0ff = plotTree.y0ff-1.0/plotTree.totalD
	for key in secondDict.keys():
		if type(secondDict[key]).__name__=='dict':
			plotTree(secondDict[key],cntrPt,str(key))
		else:
			plotTree.x0ff = plotTree.x0ff+1.0/plotTree.totalW
			plotNode(secondDict[key],(plotTree.x0ff,plotTree.y0ff),cntrPt,leafNode)
			plotMidText((plotTree.x0ff,plotTree.y0ff),cntrPt,str(key))
	plotTree.y0ff = plotTree.y0ff+1.0/plotTree.totalD

def createPlot(inTree,filename):
	fig = plt.figure(1,facecolor='white')
	fig.clf()
	axprops = dict(xticks=[],yticks=[])
	createPlot.ax1 = plt.subplot(111,frameon=False,**axprops)
	#inTree['no surfacing'][3]='maybe'
	plotTree.totalW = float(getNumLeafs(inTree))
	plotTree.totalD = float(getTreeDepth(inTree))
	#print(plotTree.totalW)
	#print(plotTree.totalD)
	plotTree.x0ff = -0.5/plotTree.totalW
	plotTree.y0ff=1.0
	plotTree(inTree,(0.5,1.0),'')
	plt.savefig(filename)

def getNumLeafs(myTree):
	numLeafs = 0
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__=='dict':
			numLeafs += getNumLeafs(secondDict[key])
		else:
			numLeafs +=1
	return numLeafs

def getTreeDepth(myTree):
	maxDepth = 0
	#myTree=list(myTree)
	#keyvalues = myTree.keys()
	#print(list(myTree.keys())[0])
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__=='dict':
			thisDepth = 1+getTreeDepth(secondDict[key])
		else:
			thisDepth=1
		if thisDepth>maxDepth:
			maxDepth=thisDepth
	return maxDepth

def retrieveTree(i):
	listOfTree=[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}]
	return listOfTree[i]

def classify(inputTree,featLabel,testVec):
	firstStr = list(inputTree.keys())[0]
	#print(firstStr)
	#print(featLabel)
	secondDict = inputTree[firstStr]
	#print(secondDict)
	featIndex = featLabel.index(firstStr)
	#print(featIndex)
	for key in secondDict.keys():
		#print(testVec)
		#print(key)	
		if testVec[featIndex]==key:
			if type(secondDict[key]).__name__=='dict':
				classLabel = classify(secondDict[key],featLabel,testVec)
			else:
				classLabel = secondDict[key]
	return classLabel

def storeTree(inputTree,filename):
	import pickle
	fw = open(filename,'wb')
	pickle.dump(inputTree,fw)
	fw.close()

def grabTree(filename):
	import pickle
	fr = open(filename,'rb')
	return pickle.load(fr)

#使用决策树预测隐形眼镜类型
def lenses():
	filename = './data/lenses.txt'
	fr=open(filename)
	lenses=[inst.strip().split('\t') for inst in fr.readlines()]
	lensesLabels=['age','prescript','astigmatic','tearRate']
	lensesTree = tree.createTree(lenses,lensesLabels)
	print(lensesTree)
	createPlot(lensesTree,'lenses.jpg')
if __name__=="__main__":
	#createPlot()
	#filename = 'myTree.txt';
	#myTree = retrieveTree(0)
	#storeTree(myTree,filename)
	#myTree['no surfacint'][3]='maybe'
	#createPlot(myTree)
	#print(myTree)
	#print(getTreeDepth(myTree))
	#print(getNumLeafs(myTree))

	#myTree = grabTree(filename)
	#labels=['no surfacing','flippers']
	#print(classify(myTree,labels,[1,0]))
	#print(classify(myTree,labels,[1,1]))
	
	lenses()
