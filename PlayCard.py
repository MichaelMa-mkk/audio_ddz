from selenium import webdriver
import os
#引入chromedriver.exe
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

#设置浏览器需要打开的url
url = "http://localhost:8080/#/"
browser.get(url)

def PlayCard(cards):
	init = ['A','2','3','4','5','6','7','8','9','0','J','Q','K']
	play = []
	f = open('hand_cards.txt');
	hands = f.read()
	f.close()
	hands = hands.split(',')
	print(hands)
	for card in cards:
		for pid in hands:
			if (len(pid) == 0):
				continue
			if (int(pid) == 52):
				now = "W"
			elif (int(pid) == 53):
				now = "w"
			else:
				now = init[int(pid) % 13]

			if now == card:
				play.append(int(pid))

		else:
			print('You do not have card %s' % (card))
			break
	js = "window.PG.Game.prototype.send_message([37,%s])" % (str(play))
	browser.execute_script(js)
