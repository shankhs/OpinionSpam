import os,sys,math
from operator import attrgetter
import shutil
import subprocess

'''
Included Features
1. Number of helpful feedbacks(i)
2. Percent of helpful feedbacks(i)
3. Length of the review title(i)
4. Length of the review body(i)
5. Position of the review in the reviews of a product sorted by date in ascending order(g)
6. Position of the review in the reviews of a product sorted by date in descending order(g)
7. Is first review(g)
8. Is only review(g)
9. Percent of positive words in review(i)
10. Percent of negative words in review(i)
11. Percent of numerals(i)
12. Percent of capitals (i)
13. Percent of all capital words(i)
14. Rating of the review(i)
15. Binary feature indicating whether a bad review was written just after the first good review(g)
16. Binary feature indicating whether a good review was written just after the first bad review(g)
17. Ratio of the number of reviews reviewer wrote which were the first reviews of the products to the total number of reviews she wrote(g)
18. ratio of the number of cases is which she was the only reviewer(g)
19. Average rating given by reviewer(g)
20. Standard deviation in rating(g)
21. Feature indicating if the reviewer always gave only good average or bad rating(g)
22. Binary feature whether reviewer gave both good and bad ratings(g)
23. Binary feature whether reviewer gave both good and average ratings(g)
24. Binary feature whether reviewer gave both average and bad ratings(g)
25. Binary feature whether reviewer gave all three ratings(g)
26. Percent of times that a reviewer wrote a review with binary features f15(g)
27. Percent of times that a reviewer wrote a review with binary features f16(g)
28. Average rating on the reviews of the product(g)
29. Standard deviation in rating on the reviews of the product(g)
Excluded Features
1. Number of feedbacks F1
2. Cosine similarity of the review and product features
3. Percent of times brand name is mentioned in the review
4. Deviation of review from product rating
5. Sales rank of the product
6. Feature indicating that the review is good, average or bad
7. Price of the product
'''

TEMP_FOLDER='.tmp'
CONNECTOR=':::'

def percentSentimentWords(text,sentimentWords):
	words = text.split()
	n = float(len(words))
	nSenWords=0
	for i in xrange(len(words)):
		if words[i] in sentimentWords:
			nSenWords+=1
	return float(nSenWords)/float(n)

def percentNumerals(text):
	nNumerals=0
	for t in text:
		if t>='0' and t<='9':
			nNumerals+=1
	return float(nNumerals)/float(len(text))

def percentCapitals(text):
	nCapitals=0;
	for t in text:
		if t>='A' and t<='Z':
			nCapitals+=1
	return float(nCapitals)/float(len(text))

def percentAllCapitalWord(text):
	words = text.split()
	nCapitalWords=0
	for w in words:
		if w.isupper():
			nCapitalWords+=1
	return float(nCapitalWords)/float(len(words))

def writePdtData(product_productId,review_time,review_userId,review_score):
	pdtData = open(os.path.join(TEMP_FOLDER,product_productId+'.txt'),'a')
	pdtData.write(str(review_time))
	pdtData.write(' ')
	pdtData.write(str(review_userId))
	pdtData.write(' ')
	pdtData.write(str(review_score))
	pdtData.write('\n')
	pdtData.close()

def writeReviewerData(review_userId,review_time,isFirstReview,product_productId,review_score):
	reviewerData = open(os.path.join(TEMP_FOLDER,review_userId+'.txt'),'a')
	reviewerData.write(str(review_time))
	reviewerData.write(' ')
	reviewerData.write(str(isFirstReview))
	reviewerData.write(' ')
	reviewerData.write(str(product_productId))
	reviewerData.write(' ')
	reviewerData.write(str(review_score))
	reviewerData.write('\n')
	reviewerData.close()

class PdtData:
	def __init__(self,pdtReviewTime,pdtReviewUserId,pdtReviewScore):
		self.pdtReviewTime = pdtReviewTime
		self.pdtReviewUserId = pdtReviewUserId
		self.pdtReviewScore = pdtReviewScore

def readPdtData(product_productId):
	pdtDatas = open(os.path.join(TEMP_FOLDER,product_productId+'.txt'),'r')
	pdtDataObjs=[]
	for pdtData in pdtDatas:
		pdtData = pdtData.split()
		pdtDataObj = PdtData(pdtData[0],pdtData[1],pdtData[2])
		pdtDataObjs.append(pdtDataObj)
	return pdtDataObjs

class RevData:
	def __init__(self,revReviewTime,revIsFirstReview,revPdtId,revRevScore):
		self.revReviewTime = revReviewTime
		self.revIsFirstReview = revIsFirstReview
		self.revPdtId = revPdtId
		self.revRevScore = revRevScore

def readReviewerData(review_userId):
	revDatas = open(os.path.join(TEMP_FOLDER,review_userId+'.txt'),'r')
	revDataObjs = []
	for revData in revDatas:
		revData = revData.split()
		revDataObj = RevData(revData[0],revData[1],revData[2],revData[3])
		revDataObjs.append(revDataObj)
	return revDataObjs

def getF5F6(pdtDataObjs,review_time,review_userId,rev):
	sorted(pdtDataObjs,key=attrgetter('pdtReviewTime'),reverse=rev)
	ind=1
	for pdtDataObj in pdtDataObjs:
		if pdtDataObj.pdtReviewTime==review_time and pdtDataObj.pdtReviewUserId==review_userId:
			f=ind
			break
		else:
			ind+=1
	return f

def getF7(pdtDataObjs,review_time,review_userId):
	sorted(pdtDataObjs,key=attrgetter('pdtReviewTime'),reverse=False)
	if pdtDataObjs[0].pdtReviewTime==review_time and pdtDataObjs[0].pdtReviewUserId==review_userId:
		return 1
	return 0

def getF8(pdtDataObjs,review_time,review_userId):
	if len(pdtDataObjs)==1 and pdtDataObjs[0].pdtReviewTime==review_time and pdtDataObjs[0].pdtReviewUserId==review_userId:
		return 1
	return 0

def getF15(pdtDataObjs,review_time,review_userId):
	if len(pdtDataObjs)>=2 and pdtDataObjs[0].pdtReviewScore>=4.0 and pdtDataObjs[0].pdtReviewScore<=2.0:
		return 1
	return 0;

def getF16(pdtDataObjs,review_time,review_userId):
	if len(pdtDataObjs)>=2 and pdtDataObjs[0].pdtReviewScore<=2.0 and pdtDataObjs[0].pdtReviewScore>=4.0:
		return 1
	return 0;

def getF17(revDataObjs,product_productId):
	nRevsUserFirst=0
	for revDataObj in revDataObjs:
		if revDataObj.revIsFirstReview==1 and revDataObj.revPdtId==product_productId:
			nRevsUserFirst+=1
	return float(nRevsUserFirst)/float(len(revDataObjs))

def getF18(revDataObjs):
	pdtIds=[]
	nOnlyUserToReview=0
	for revDataObj in revDataObjs:
		if revDataObj.revIsFirstReview==1:
			pdtIds.append(revDataObj.revPdtId)
	for pdtId in pdtIds:
		pdtData = [f.rstrip('\n') for f in open(os.path.join(TEMP_FOLDER,pdtId+'.txt'))]
		if len(pdtData)==1:
			nOnlyUserToReview+=1
	return float(nOnlyUserToReview)/float(len(revDataObjs))

def getF19(revDataObjs):
	mean=0
	for revDataObj in revDataObjs:
		mean+=float(revDataObj.revRevScore)
	return float(mean)/float(len(revDataObjs))

def getF20(revDataObjs,mean):
	variance=0
	for revDataObj in revDataObjs:
		variance+= float((float(revDataObj.revRevScore)-mean)*(float(revDataObj.revRevScore)-mean))
	return math.sqrt(float(variance)/float(len(revDataObjs)))

def getF21(revDataObjs):
	minRating=5.0
	maxRating=0.0
	for revDataObj in revDataObjs:
		minRating = min(revDataObj.revRevScore,minRating)
		maxRating = max(revDataObj.revRevScore,maxRating)
	if (minRating>=4.0 and maxRating<=4.0) or (minRating<=2.0 and maxRating<=2.0) or (minRating>2 and minRating<4.0 and maxRating>2.0 and maxRating<4.0):
		return 1
	return 0

def getF22(revDataObjs):
	isGood=False
	isBad=False
	for revDataObj in revDataObjs:
		if revDataObj.revRevScore>=4.0:
			isGood=True
		if revDataObj.revRevScore<=2.0:
			isBad=True
	if isGood and isBad:
		return 1
	return 0

def getF23(revDataObjs):
	isGood=False
	isAvg = False
	for revDataObj in revDataObjs:
		if revDataObj.revRevScore>=4.0:
			isGood=True
		if revDataObj.revRevScore>2.0 and revDataObj.revRevScore<4.0:
			isAvg=True
	if isGood and isAvg:
		return 1
	return 0

def getF24(revDataObjs):
	isBad = False
	isAvg = False
	for revDataObj in revDataObjs:
		if revDataObj.revRevScore<=2.0:
			isBad = True
		if revDataObj.revRevScore>2.0 and revDataObj.revRevScore<4.0:
			isAvg=True
	if isBad and isAvg:
		return 1
	return 0

def getF25(revDataObjs):
	isGood=False
	isBad=False
	isAvg = False
	for revDataObj in revDataObjs:
		if revDataObj.revRevScore<=2.0:
			isBad=True
		if revDataObj.revRevScore>2.0 and revDataObj.revRevScore<4.0:
			isAvg=True
		if revDataObj.revRevScore>=4.0:
			isGood=True
	if isGood and isBad and isAvg:
		return 1
	return 0

def getF26(pdtDataObjs):
	return 0

def getF27(pdtDataObjs):
	return 0

def getF28(pdtDataObjs):
	mean=0.0
	for pdtDataObj in pdtDataObjs:
		mean+=float(pdtDataObj.pdtReviewScore)
	return float(mean)/float(len(pdtDataObjs))

def getF29(pdtDataObjs,mean):
	variance = 0.0
	for pdtDataObj in pdtDataObjs:
		variance += float((float(pdtDataObj.pdtReviewScore)-mean)*(float(pdtDataObj.pdtReviewScore)-mean))
	return math.sqrt(float(variance)/float(len(pdtDataObjs)))

def commitFeats(*args,**kwargs):
	k=''
	filename=''
	opinion=''
	suffix='f'
	ind=1
	for (K,V) in kwargs.iteritems():
		if K=='filename':
			k = K
			filename=V
		elif K=='opinion':
			k = K
			opinion = V
	fileData = open(filename,'w')
	fileData.write(str(opinion))
	fileData.write(' ')
	for a in args:
		fileData.write(suffix+str(ind)+':')
		fileData.write(str(a))
		fileData.write(' ')
		ind+=1
	fileData.write('\n')
	fileData.close()

def getCompleteListOfFilesAndLabels(trainingFile):
	listFiles = [f.rstrip('\n') for f in open(trainingFile)]
	files=[]
	spams={}
	hams={}
	for f in listFiles:
		f = f.split()
		files.append(f[0].strip())
		if f[1].strip().lower()=='spam':
			spams[f[0].strip()]=1
		else:
			hams[f[0].strip()]=1
	return (files,spams,hams)

def megamTest(testFilename,modelFile):
	ret=[]
	command = './megam/megam.opt -nc -predict %s multitron %s' %(modelFile,testFilename)
	#print command
	args=[command]
	pid = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
	out, err = pid.communicate()
	ret.append(out)
	return ret

def extractFeatures(files,featFilename,modelFilename):
	decisionPerFile={}
	for f in files:
		if not f.endswith('.txt'):
			print 'ERROR: File not ending in txt. ',f
			continue
		review = [r.rstrip('\n') for r in open(f.rstrip('\n'))]
		if len(review)==0:
			print 'ERROR: Empty review for file f: ',f
			continue
		product_productId = review[0].split(':')[1].strip()
		product_title = review[1].split(':')[1].strip()
		product_price = review[2].split(':')[1].strip()
		review_userId = review[3].split(':')[1].strip()
		review_profilename = review[4].split(':')[1].strip()
		review_helpfulness = review[5].split(':')[1].strip()
		review_score = review[6].split(':')[1].strip()
		review_time = review[7].split(':')[1].strip()
		review_summary = review[8].split(':')[1].strip()
		review_text = review[9].split(':')[1].strip()
		if review_userId == 'unknown' or product_productId=='unknown' or review_time == 'unknown':
			continue

		f1 = review_helpfulness.split('/')[0]
		f2 = float(f1)/float(max(int(review_helpfulness.split('/')[1]),1))
		f3 = len(review_summary)
		f4 = len(review_text)
		f9 = percentSentimentWords(review_text,posWords)
		f10 = percentSentimentWords(review_text,negWords)
		f11 = percentNumerals(review_text)
		f12 = percentCapitals(review_text)
		f13 = percentAllCapitalWord(review_text)
		f14 = review_score
		
		pdtDataObjs = readPdtData(product_productId)
		revDataObjs = readReviewerData(review_userId)
		
		#5. Position of the review in the reviews of a product sorted by date in ascending order(g)
		f5=getF5F6(pdtDataObjs,review_time,review_userId,False)
		#6. Position of the review in the reviews of a product sorted by date in descending order(g)
		f6 = getF5F6(pdtDataObjs,review_time,review_userId,True)
		#7. Is first review(g)
		f7 = getF7(pdtDataObjs,review_time,review_userId)
		#8. Is only review(g)
		f8 = getF8(pdtDataObjs,review_time,review_userId)
		#15. Binary feature indicating whether a bad review was written just after the first good review(g)
		f15 = getF15(pdtDataObjs,review_time,review_userId)
		#16. Binary feature indicating whether a good review was written just after the first bad review(g)
		f16 = getF16(pdtDataObjs,review_time,review_userId)
		#17. Ratio of the number of reviews reviewer wrote which were the first reviews of the products to the total number of reviews she wrote(g)
		f17 = getF17(revDataObjs,product_productId)
		#18. ratio of the number of cases is which she was the only reviewer(g)
		f18 = getF18(revDataObjs)
		#19. Average rating given by reviewer(g)
		f19 = getF19(revDataObjs)
		#20. Standard deviation in rating(g)
		f20 = getF20(revDataObjs,f19)
		#21. Feature indicating if the reviewer always gave only good average or bad rating(g)
		f21 = getF21(revDataObjs)
		#22. Binary feature whether reviewer gave both good and bad ratings(g)
		f22 = getF22(revDataObjs)
		#23. Binary feature whether reviewer gave both good and average ratings(g)
		f23 = getF23(revDataObjs)
		#24. Binary feature whether reviewer gave both average and bad ratings(g)
		f24 = getF24(revDataObjs)
		#25. Binary feature whether reviewer gave all three ratings(g)
		f25 = getF25(revDataObjs)
		#26. Percent of times that a reviewer wrote a review with binary features f15(g)
		f26 = getF26(pdtDataObjs) #TODO: To implement
		#27. Percent of times that a reviewer wrote a review with binary features f16(g)
		f27 = getF27(pdtDataObjs) #TODO: To implement
		#28. Average rating on the reviews of the product(g)
		f28 = getF28(pdtDataObjs)
		#29. Standard deviation in rating on the reviews of the product(g)
		f29 = getF29(pdtDataObjs,f28)
		label=''
		if f in spams:
			label='SPAM'
		else:
			label='HAM'
		commitFeats(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,filename=featFilename,opinion=label)
		decision = megamTest(featFilename,modelFilename)
		decision = decision[0].split('\t')
		decision = decision[0]
		decisionPerFile[f] = decision
		#print decision
	return decisionPerFile

def remove(f,spams,hams):
	if f in spams:
		spams.pop(f)
	if f in hams:
		hams.pop(f)
	return (spams,hams)

def calculateFScore(decisionPerFile,spams,hams):
	classified={}
	correctlyClassified={}
	
	classified['spam']=0
	classified['ham']=0
	
	correctlyClassified['spam']=0
	correctlyClassified['ham']=0
	
	belongs={}
	belongs['spam']=len(spams)
	belongs['ham']=len(hams)
	
	for f in decisionPerFile:
		if decisionPerFile[f]=='SPAM':
			classified['spam']+=1
			if f in spams:
				correctlyClassified['spam']+=1
		if decisionPerFile[f]=='HAM':
			classified['ham']+=1
			if f in hams:
				correctlyClassified['ham']+=1
	precision = {}
	recall = {}
	precision['spam'] = float(correctlyClassified['spam'])/float(classified['spam'])
	recall['spam'] = float(correctlyClassified['spam'])/float(belongs['spam'])
	precision['ham'] = float(correctlyClassified['ham'])/float(classified['ham'])
	recall['ham'] = float(correctlyClassified['ham'])/float(belongs['ham'])
	
	print 'fscore for spam is: ',2*precision['spam']*recall['spam']/(precision['spam']+recall['spam'])
	print 'fscore for ham is: ',2*precision['ham']*recall['ham']/(precision['ham']+recall['ham'])

if __name__=='__main__':
	if len(sys.argv)!=7:
		print 'Enter file containing positive words, file contaning negative words,file containing path to reviews, file to store features,file containing list of reviews for which I have to extract features and the model file'
	else:
		posWords = [f.rstrip('\n') for f in open(sys.argv[1])]
		negWords = [f.rstrip('\n') for f in open(sys.argv[2])]
		spams={}
		hams={}
		if os.path.exists(TEMP_FOLDER):
			shutil.rmtree(TEMP_FOLDER)
		os.makedirs(TEMP_FOLDER)
		if os.path.exists(sys.argv[4]):
			os.remove(sys.argv[4])
		[files,spams,hams] = getCompleteListOfFilesAndLabels(sys.argv[5])
		#files = os.listdir(sys.argv[3])
		#print files
		#for k in spams:
		#	print k,' ',spams[k]
		#print len(spams)
		#print len(hams)
		#raw_input()
		#print len(files)
		for f in files:
			if not f.endswith('.txt'):
				print 'ERROR: File not ending in txt. ',f
				spams,hams=remove(f,spams,hams)
				continue
			review = [r.rstrip('\n') for r in open(f.rstrip('\n'))]
			if len(review)==0:
				print 'ERROR: Empty review for file f: ',f
				spams,hams=remove(f,spams,hams)
				continue
			
			#print len(review)
			product_productId = review[0].split(':')[1].strip()
			product_title = review[1].split(':')[1].strip()
			product_price = review[2].split(':')[1].strip()
			review_userId = review[3].split(':')[1].strip()
			review_profilename = review[4].split(':')[1].strip()
			review_helpfulness = review[5].split(':')[1].strip()
			review_score = review[6].split(':')[1].strip()
			review_time = review[7].split(':')[1].strip()
			review_summary = review[8].split(':')[1].strip()
			review_text = review[9].split(':')[1].strip()
			if review_userId == 'unknown' or product_productId=='unknown' or review_time == 'unknown':
				continue
			'''
			print product_productId
			print product_title
			print priduct_price
			print review_userId
			print review_profilename
			print review_helpfulness
			print review_score
			print review_time
			print review_summary
			print review_text
			'''
			
			isFirstReview = 1-int(os.path.isfile(os.path.join(TEMP_FOLDER,product_productId+'.txt')))
			#print isFirstReview
			writePdtData(product_productId,review_time,review_userId,review_score)
			writeReviewerData(review_userId,review_time,isFirstReview,product_productId,review_score)
		#print len(files)
		decisionPerFile = extractFeatures(files,sys.argv[4],sys.argv[6])
		print len(files)
		print len(decisionPerFile)
		print len(spams)
		print len(hams)
		calculateFScore(decisionPerFile,spams,hams)
		#for f in spams:
		#	if f in decisionPerFile:
		#		print f,'SPAM',decisionPerFile[f]
		#for f in hams:
		#	if f in decisionPerFile:
		#		print f,'HAM',decisionPerFile[f]
