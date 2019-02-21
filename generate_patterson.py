import math
import numpy as np
import sys

elements = ["", "H", "He", "Li", "Be", "B", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As"]

print(elements[25])

class vec3d(np.ndarray):
    """ 3d vector class. Takes arguments eg vec3d((0, 0, 0)) """
    def __new__(cls, lst=(0,0,0)):
        ar = np.array(lst, dtype=float)
        x=np.ndarray.__new__(cls, shape=(3,), dtype=float, buffer=ar)
        return x
   
    def length(self):
        """ Returns the magnitude of the vector """
        # sqrt((x-x')^2 + (y-y')^2 + (z-z')^2)
        return np.sqrt(np.sum(self * self))
    def string(self, separator):
        """ Returns the vector as x, y, z (for separator = ',')"""
        return str("%f%s%f%s%f" % (self[0],
                                separator,
                                self[1],
                                separator,
                                self[2]))

def read_xyz(filename):
    p = []
    ma = []
    with open(filename, "r") as ins:
        array = []
        c = 0
        for line in ins:
            if (c > 1):
                loc = line.split()
                if (len(loc) < 4):
                    exit()
                p.append(vec3d((float(loc[1]),
                                float(loc[2]),
                                float(loc[3]))))
                ma.append(float(loc[0]))
            c = c + 1
    return [p, ma]

def output(filename, pos, weight, symbols):
    with open(filename, "w") as f:
        f.write("%d\nOutput file\n" % (len(pos)))
        for i in range(0, len(pos)):
            if (symbols == 0):
                f.write("%d\t%f\t%f\t%f\n" % (weight[i], pos[i][0], pos[i][1], pos[i][2]))
            else:
                f.write("%s\t%f\t%f\t%f\n" % (elements[int(weight[i])], pos[i][0], pos[i][1], pos[i][2]))

filename = ""
symbols = 0
for i in sys.argv[1:]:
    if (i == "c"):
        symbols = 1 
    elif (i[0] == "i"):
        filename = i[1:]
    elif (i[0] == "o"):
        outputfilename = i[1:]

if (filename == "" or outputfilename == ""):
    exit()

[p, ma] = read_xyz(filename)

patterson_pos = []
patterson_weight = []

for x in range(0, len(p)):
    for y in range(0, len(p)):
        new_pos = (p[x] - p[y])
        new_mass = ma[x] * ma[y]
        ck = 0
        for i in range(0, len(patterson_pos)):
            if ((new_pos - patterson_pos[i]).length() < 0.00001):
                ck = 1
                patterson_weight[i] = patterson_weight[i] + new_mass
        if (ck == 0):
            patterson_pos.append(new_pos)
            patterson_weight.append(new_mass)  

print(patterson_weight)

output(outputfilename, patterson_pos, patterson_weight, symbols)

print(read_xyz("ex.xyz"))
