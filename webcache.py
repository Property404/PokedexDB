#########################################
#              webcache.py              #
#  Stores webpages on local drive when  #
#               accessed                #
#########################################
import urllib.request
import urllib.parse
import os


def get_page(url):
	# constants
	file_extension = ".cache"
	containing_folder = "./cache/"

	# Replace but remember protocol
	protocol = "http"
	for i in ["http", "https", "ftp", "file"]:
		if url[0:len(i)+3] == i+"://":
			url = url[len(i)+3::]
			protocol = i
			break

	# Make file path
	local_path = (containing_folder+url+file_extension).replace("?", "{_QMARK}")

	if os.path.exists(local_path):
		# Read and return file text
		return open(local_path, "rb").read().decode("utf16")
	else:
		# Get text
		print(url.encode("utf8"))
		text = urllib.request.urlopen(protocol+"://"+url)
		text = text.read().decode("utf8")

		# save text
		fp = open(local_path, 'wb')
		fp.write(text.encode("utf16"))
		fp.close()

		return text
