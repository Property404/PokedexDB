#########################################
#              webcache.py              #
#  Stores webpages on local drive when  #
#               accessed                #
#########################################
import urllib.request
import os

def get_page(url):
	# constants
	FILE_EXTENSION = ".cache"
	CONTAINING_FOLDER = "./cache/"
	
	# Replace but remember protocol
	protocol = "http"
	for i in ["http","https","ftp","file"]:
		if url[0:len(i)+3]==i+"://":
			url=url[len(i)+3::]
			protocol = i
		
	# Make file path
	local_path = (CONTAINING_FOLDER+url+FILE_EXTENSION).replace("?","{_QMARK}")
		
	if os.path.exists(local_path):
		# Read and return file text
		return open(local_path).read()
	else:
		# Get text
		print(protocol+"://"+url)
		o_text = urllib.request.urlopen(protocol+"://"+url).read().decode("UTF-8")
		
		#Remove non-ascii characters
		text = ""
		for i in o_text:
			if ord(i)<=127:
				text+=i
		
		# save text
		fp = open(local_path, 'wb');
		fp.write(text.encode("UTF-8"))
		fp.close();
		
		return text