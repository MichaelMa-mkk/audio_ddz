# -*- coding: utf-8 -*-

class pattern:

    def match(self,input):
        poker = ["尖", "二","三","四","五","六","七","八","九","十","勾","圈", "王"]
        trans = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "joker"]
        quantity = ["一个","两个","三个","四个"]
        key = input.replace(' ','')
        number = 0
        for i in range(4):
            if key[0:2] == quantity[i]:
                number = i + 1
        card = ""
        for i in range(13):
            # print(key[2:3],poker[i])
            if key[2:3] == poker[i]:
                card = trans[i]
        output = ""
        for i in range(number):
            output = output + card
        return output

def exract(saying):
    Pattern = pattern()
    for key in saying:
        if(saying[key] < 0.7):
            continue
        word = key
        output = Pattern.match(word)
        print(output)

test = {"三个尖":0.8}
exract(test)