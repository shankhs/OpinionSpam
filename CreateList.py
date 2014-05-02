import os,sys

if __name__=='__main__':
	if len(sys.argv)<3:
		print 'Enter folder containing reviews and folder containing spam reviews'
		exit()
	files={}
	dataset = sys.argv[1]
	spams = sys.argv[2]
	
	spamTxt = open('SPAM.txt','w')
	hamTxt = open('HAM.txt','w')
	
	datasetFiles = os.listdir(dataset)
	spams = os.listdir(spams)
	
	for f in spams:
		files[f] = 1
	
	for f in datasetFiles:
		if f in files:
			spamTxt.write(f)
			spamTxt.write('\n')
		else:
			hamTxt.write(f)
			hamTxt.write('\n')
	spamTxt.close()
	hamTxt.close()
