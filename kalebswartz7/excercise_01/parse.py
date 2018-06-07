# Parse the data from the dat file -> Points vs Horizontal Position = how many rows per column in the 2D array 
#                                  -> Points vs Vertical Position = how many columns in the 2D array 

#       Create a dictionary and populate it with other dictionaries based on the data in the dat file 
#       Use this data to add to the graph

import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

#Just default values, these are changed based on the dat file
horizontal = 1 
vertical = 1

#initialize the dictionary for storing parameters given in the dat file 
initialData = {}
initialData['photon'] = {}
initialData['horizontal'] = {}
initialData['vertical'] = {}
matrix = [[]] 

""" 
Get data from the dat file with the parameters for the scan. Put this data into an organized Dictionary

"""
def getCommentedData():
    with open('res_int_pr_se.dat') as file:
        lineNum = 1
        for line in file:
            if "#" not in line:
                return
            else:
                if (lineNum is 1):
                    populateDictionary(line, '[', ']', 'intensity')
                elif ('Initial Photon' in line):
                    populateDictionary(line, '#', ' ', 'photon', 'Initial_Energy')
                elif ('Final Photon' in line):
                    populateDictionary(line, '#', ' ', 'photon', 'Final_Energy')
                elif ('Initial Horizontal' in line):
                    populateDictionary(line, '#', ' ', 'horizontal', 'Initial_Position')
                elif ('Final Horizontal' in line):
                    populateDictionary(line, '#', ' ', 'horizontal', 'Final_Position')
                elif ('vs Horizontal' in line):
                    populateDictionary(line, '#', ' ', 'horizontal', 'Points', 'float','horizontal')
                elif ('Initial Vertical' in line):
                    populateDictionary(line, '#', ' ', 'vertical', 'Initial_Position')
                elif ('Final Vertical' in line):
                    populateDictionary(line, '#', ' ', 'vertical', 'Final_Position')
                elif ('vs Vertical' in line):
                    populateDictionary(line, '#', ' ', 'vertical', 'Points', 'float','vertical')


            lineNum += 1

"""
Funciton that populates the dictionary based on what values from the line are needed, what type they should be, and if they need to change 
the values of any global varaiables 

"""

def populateDictionary(line, startingPoint, endingPoint, d, d1 = {}, type1='string', vToChange = 0):
    changeH = False
    changeV = False

    if (vToChange is 'horizontal'):
        changeH = True
    elif (vToChange is 'vertical'):
        changeV = True

    start = line.find(startingPoint) + 1
    end = line.find(endingPoint)

    if (type1 is 'string'):
        vToChange = (line[start:end])
    else:
        vToChange = int(line[start:end])


    #Checks to see if d1 is actually necessary 
    if (not d1):
        initialData[d] = vToChange
    else:
        initialData[d][d1] = vToChange

    #Checks to see if horizontal / vertical global values should be changed 
    if (changeH):
        setHorizontal(vToChange)
    elif (changeV):
        setVertical(vToChange)

def setHorizontal(value):
    global horizontal
    horizontal = value

def setVertical(value):
    global vertical
    vertical = value


def populateMatrix():
    global matrix
    matrix = [[0 for i in range(horizontal)] for j in range(vertical)] 
    with open('res_int_pr_se.dat') as file:
        h, v = 0, 0
        for line in file:
            if "#" not in line:
                matrix[v][h] = float(line)
                if (h < horizontal - 1):
                    h += 1
                else:
                    h = 0
                    v += 1

def populateMatrixSmart():
    d = np.loadtxt('res_int_pr_se.dat')
    d2 = d.reshape((294, 528))
    global matrix
    matrix = d2

def createImage(): 
   im = plt.imshow(matrix, cmap='gray', aspect="equal")
   plt.colorbar(im, orientation='vertical')
   plt.show()


# np.loadtxt()
# import pandas

if __name__ == '__main__':
    getCommentedData()

    #populateMatrixSmart()

    populateMatrix()
    print(initialData)
    createImage() 
