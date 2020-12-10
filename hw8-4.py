L = []
with open('D://submission_complete.csv', 'r', encoding = 'utf-8') as f:
    for sentence in f:
        sentence = sentence.split(',')
        if sentence[6] == 'score':
            continue
        word = sentence[5]
        aword = word[2] + word[5]
        if sentence[2] == 'Accepted':
            if len(L) == 0:
                L.append([aword, 1])
            else:
                for i in range(len(L)):
                    if L[i][0] == aword:
                        L[i][1] += 1
                        break
                    if i == len(L) - 1:
                        L.append([aword, 2])
L.sort()        
print(L)
import matplotlib.pyplot as py
xlist = []
ylist = []
for i in range(len(L)):
    xlist.append(L[i][0])
    ylist.append(L[i][1])

py.plot(xlist,ylist)
py.show()