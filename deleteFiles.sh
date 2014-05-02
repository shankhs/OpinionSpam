count=1
while [ $count -lt 100000 ]
do
	echo $1/$count.txt
	rm $1/$count.txt;
	count=$[count+1];
done
