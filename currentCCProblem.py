import requests,json,time,threading
from bs4 import BeautifulSoup
from sys import stdout
import os

url = "https://www.codechef.com/problems/easy"
cc = "https://www.codechef.com"
probStack=[]
Done=False

pathTo = lambda relPath: os.path.join(os.getcwd()+relPath)

def dot():
	stdout.write('Loading problem')
	while not Done:
		time.sleep(1)
		stdout.write('.')
		stdout.flush()

def mainWork():
	with open(pathTo("/chefCookie.json"),'r') as cookie:
		c = cookie.read()
		with requests.Session() as session:
			r = session.get(url,cookies=json.loads(c))
			time.sleep(5)
			soup = BeautifulSoup(r.content,"html.parser")
			# print(soup.encode('utf8'))
			for row in soup.findAll('div',{'class':'problemname'}):
				children = row.findAll(recursive=False)
				aTag = row.next.next
				pName = aTag.next.next.text
				if len(children)==1:
					probStack.append(pName+' - '+cc+aTag['href'])
				elif len(children)>1 and children[1]['alt']!='Solved':
					probStack.append(pName+' - '+cc+aTag['href'])
	global Done
	Done=True
	probStack.append(0)
	i='y'
	while i in ('y','yes','Y',"YES"):
		probStack.pop()
		print("Total Remaining: ",len(probStack),"\nCurrent problem: ")
		print(probStack[-1])
		os.system('python -m webbrowser -t "{}"'.format(probStack[-1].split(' - ')[1]))
		i=input("Done?(yes/no) ")
	

dotter=threading.Thread(target=dot)
dotter.start()
thread=threading.Thread(target=mainWork)
thread.start()
