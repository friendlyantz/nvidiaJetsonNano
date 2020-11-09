import matplotlib.pyplot as plt
import numpy as np
# x=np.arange(-4,4,.1)
x=np.linspace(0,2*np.pi,50)
# y=np.square(x)
y=np.sin(x-np.pi/2)
# y=x*x                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

# y2=np.square(x+2)
y2=np.cos(x)
# y3=x*(x-4)+3
plt.grid(True)
plt.xlabel('My X Values')
plt.ylabel('My Y Values')
plt.title('My Graph Values')
# plt.axis([0,5,0,10])
plt.plot(x,y,'b-*',linewidth=3,markersize=9, label='blue')
plt.plot(x,y2,'r-.o',linewidth=3,markersize=7, label='red')
# plt.plot(x,y3,'g:^',linewidth=3,markersize=7, label='green')

plt.legend(loc='lower left')
plt.show()