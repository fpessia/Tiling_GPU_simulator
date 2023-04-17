
import torch
import math
import sys


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