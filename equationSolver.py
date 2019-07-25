
S = "#7*7+5-1O"
n = len(S)
tp = []
i = 1
while(i < n) :
    if(S[i] == '+') : tp.append(-100001)
    elif(S[i] == '-') : tp.append(-100002)
    elif(S[i] == '*') : tp.append(-100003)
    elif(S[i] == '/') : tp.append(-100004)
    else :
        x = 0
        ix = i
        while(ix < n and (S[ix] >= '0' and S[ix] <= '9' or S[ix] == 'O' or S[ix] == 'o')) : ix += 1
        for j in range(i, ix) :
            y = S[j]
            if(S[j] == 'O' or S[j] == 'o') : y = '0'
            x = x * 10 + ord(y) - 48
        tp.append(x)
        #print(i)
        i = ix - 1
        #print(i)
    i += 1
#print (tp)
sv = []

i = 1
#print("done")
sv.append(tp[0])
#print(sv)

while(i < len(tp)) :
    if(tp[i] == -100004) :
        x = sv.pop()
        y = tp[i + 1]
        sv.append(x / y)

    else :
        sv.append(tp[i])
        sv.append(tp[i + 1])
    #print(sv)
    i += 2
#print("here")

if len(sv) > 0 : tp = sv
#print (tp)
sv = []

i = 1

sv.append(tp[0])

while(i < len(tp)) :
    if(tp[i] == -100003) :
        x = sv.pop()
        y = tp[i + 1]
        sv.append(x * y)

    else :
        sv.append(tp[i])
        sv.append(tp[i + 1])
    i += 2


if len(sv) > 0 : tp = sv
#print (tp)
sv = []
i = 1

sv.append(tp[0])

while(i < len(tp)) :
    if(tp[i] == -100002) :
        x = sv.pop()
        y = tp[i + 1]
        sv.append(x - y)

    else :
        sv.append(tp[i])
        sv.append(tp[i + 1])
    i += 2


if len(sv) > 0 : tp = sv
#print (tp)
sv = []
i = 1

sv.append(tp[0])

while(i < len(tp)) :
    if(tp[i] == -100001) :
        x = sv.pop()
        y = tp[i + 1]
        sv.append(x + y)

    else :
        sv.append(tp[i])
        sv.append(tp[i + 1])
    i += 2
if len(sv) > 0 : tp = sv
print (tp)
#print("end")

