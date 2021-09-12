import urllib.request
import shelve

string_url = "https://www.mit.edu/~ecprice/wordlist.10000"
response = urllib.request.urlopen(string_url)
long_txt = response.read().decode()
strings = long_txt.splitlines()
shelf_file = shelve.open('strings.txt')
shelf_file['strings'] = strings
shelf_file.close()
