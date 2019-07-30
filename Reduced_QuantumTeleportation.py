import strawberryfields as sf
from strawberryfields.ops import *
from strawberryfields.utils import scale
from numpy import pi, sqrt
#import matplotlib.pyplot as plt

eng, q = sf.Engine(3)

@sf.convert
def custom(x):
    return -x*sqrt(2)


x_ini = 1
p_ini = 0.5
with eng:
    # prepare the initial states
    Coherent(x_ini + p_ini * 1j) | q[0]  # This is the state we want to teleport
    Sgate(-2) | q[1] # momentum squeezed
    Sgate(2) | q[2] # position squeezed
    
    # apply the gates
    BSgate(pi/4, 0) | (q[1], q[2])  # a 50-50 beamsplitter
    BSgate(pi/4, 0) | (q[0], q[1])  # a 50-50 beamsplitter
    
    # perform the homodyne measurements
    MeasureX | q[0]
    MeasureP | q[1]    
    
    # displacement gates conditioned on the measurements
    Xgate(scale(q[0], sqrt(2))) | q[2]
    Zgate(scale(q[1], sqrt(2))) | q[2]
    #Zgate(custom(q[1])) | q[2]
    
state = eng.run('fock', cutoff_dim=15)
print('prepared state : ', x_ini, p_ini)
#print(q[0].val, q[1].val)

x = np.arange(-5, 5, 0.1)
p = np.arange(-5, 5, 0.1)
W = state.wigner(2, x, p)
X, P = np.meshgrid(x, p)
#plt.contourf(X, P, W)