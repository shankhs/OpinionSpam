import os,sys
from itertools import islice

MAX_FILES=100000

def writeToFile(data,filename):
	fileData = open(filename,'w')
	for d in data:
	    fileData.write(str(d))
	    fileData.write('\n')
	fileData.close()

if __name__=='__main__':
	if len(sys.argv)<3:
	    print 'Enter the text file and destination folder'
	else:
	    n=1
	    folder = sys.argv[2]
	    indiData=[]
	    ind=0
	    for f in open(sys.argv[1]):
                f = f.rstrip('\n')
	    	if f=='':
	    	    if len(indiData)!=0:
                        product_id = indiData[0].split(":")[1]
                        user_id = indiData[3].split(":")[1]
                        timestamp = indiData[7].split(":")[1]
                        if not(product_id == "unknown" or user_id == "unknown" or product_id == "" or user_id ==""):
                            if long(timestamp) > long("1104537600"):
                                writeToFile(indiData,os.path.join(folder,str(ind)+'.txt'))
                                ind+=1
                    else:
                        print 'ERROR: Empty data!'
                    indiData=[]
	    	    if ind>MAX_FILES:
                        break
	    	else:
                    indiData.append(f)
            	writeToFile(indiData,os.path.join(folder,str(ind)+'.txt'))
