
import torch
import math
import threading
import sys

ll = []
ll.append([])
print(ll)


sys.exit()
lock =threading.Lock()
x = 512
def div_by_2():
    global x,lock
    lock.acquire()
    while(x > 1):
        x = x/2
        print(x)
    lock.release()

def mul_by_2():
    global x,lock
    lock.acquire()
    while(x < 512*2*2*2):
        x = x*2
        print(x)
    lock.release()

    


t1 = threading.Thread(target=div_by_2)
t2 = threading.Thread(target=mul_by_2)

t2.start()
t1.start()





sys.exit()
print(int(116850/4))
print(116850 % 4)
print(116850- int(116850/4)* 4)



sys.exit()
t1 = torch.tensor([[1,0],[0,1]])
t2 = torch.tensor([[1,0],[0,1]])
print(t1+t2)

sys.exit()






sys.exit()
def summer(A,B, index,result):
    result[index] = A+B


result =[0, 0]
x = []

for i in range(len(result)):
    x.append(threading.Thread(target=summer, args=((i+1),(i+2),i,result)))
for i in range(len(result)):
    x[i].start()
flag = False
while(not(flag)):
    if(result[0] != 0):
        print(result[0])
    if(result[1] != 0):
        print(result[1])
    if(result[0] != 0 and result[1] != 0):
        flag = True

sys.exit()
def ll(l):
    l[0] += 1

l=[0,0]
ll(l)
print(l)
print(len(l))

sys.exit()
h = 15
g = 4
print(int(h/g))
m = 16 
m = m -int(h/g)
print(m)

sys.exit()
l = []
A = torch.randn(4,4)
print(A)
B = A[0: 2, 1: 3]
C = A [1 :3, 0 : 2 ]
l.append((B,C))
print(l)
print(len(l))




sys.exit()
k = math.log2(3) % 1
print(k)

k = -1 % 1
print(k)


sys.exit()
#Zero padding test
x = torch.tensor([[5.0, 3.0 , 3.0], [2.0, 2.0, 2.0], [1.0, 1.0, 1.0]])
y = torch.tensor([[5.0, 3.0 , 3.0], [2.0, 2.0, 2.0], [1.0, 1.0, 1.0]])

p = torch.matmul(x, y)

print(p)

xx,xy = x.size()

xx += 1
xy += 1

yx, yy = y.size()
yx += 1
yy += 1
x_padded = torch.zeros(xx, xy)
y_padded = torch.zeros(yx, yy)

x_padded[0: (xx-1), 0 : (xy-1)] = x
print(x_padded)
y_padded[0 : (yx-1), 0 : (yy-1)] = y
print(y)
p_padded = torch.matmul(x_padded, y_padded)
print(p_padded)





sys.exit()
x = torch.randn(2,2)
print(x)
y = torch.ones(2,1)
print(y)
p = torch.matmul(x,y)
print(p)

x,y = p.size()
print(p.size())
print(x)
print(y)