import sys
import random
import os

if __name__ == '__main__':
	if len(sys.argv)!=4:
		print 'Please enter the directory path, spam file and ham file.'
	else:
		files = [os.path.join(sys.argv[1],f) for f in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1],f))]
		spamFiles = [f.rstrip('\n') for f in open(sys.argv[2])]
		hamFiles = [f.rstrip('\n') for f in open(sys.argv[3])]
		spams={}
		hams={}
		trainIndex=[]
		lookup={}
		#print spamFiles
		for s in spamFiles:
			spams[os.path.join(sys.argv[1],s)]=1
		for h in hams:
			hams[os.path.join(sys.argv[1],h)]=1
		for i in range(0,(int)(0.8*len(files))):
			isPresent=True
			while isPresent:
				newIndex = (int)(random.random()*len(files))
				flag=True
				'''
				for j in range(0,len(trainIndex)):
					if trainIndex[j]==newIndex:
						flag=False
						break
				'''
				if newIndex not in lookup:
					isPresent=False
					trainIndex.append(newIndex)
					lookup[newIndex] = len(trainIndex)
					#print len(trainIndex)
				'''
				if flag:
					isPresent=False
					trainIndex.append(newIndex)
					lookup[[newIndex] = len(trainIndex)
				'''
		fileTrainImageFilename = open("train.txt","wb")
		fileTestImageFilename = open("test.txt","wb")
		print 'Writing train files:'
		for i in range(0,len(trainIndex)):
			label=''
			if files[trainIndex[i]] in spams:
				label='spam'
			else:
				label = 'ham'
			fileTrainImageFilename.write(files[trainIndex[i]])
			fileTrainImageFilename.write(' ')
			fileTrainImageFilename.write(label)
			fileTrainImageFilename.write("\n")
		fileTrainImageFilename.close()
		print 'Writing test files:'
		for i in range(0,len(files)):
			if i not in lookup:
				label=''
				if files[i] in spams:
					label='spam'
				else:
					label = 'ham'
				fileTestImageFilename.write(files[i])
				fileTestImageFilename.write(' ')
				fileTestImageFilename.write(label)
				fileTestImageFilename.write('\n')
		fileTestImageFilename.close()
