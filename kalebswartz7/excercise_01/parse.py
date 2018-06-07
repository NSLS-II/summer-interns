# Parse the data from the dat file -> Points vs Horizontal Position = how many rows per column in the 2D array 
#                                  -> Points vs Vertical Position = how many columns in the 2D array 

#       Create a dictionary and populate it with other dictionaries based on the data in the dat file 
#       Use this data to add to the graph

import numpy as np
import matplotlib.pyplot as plt

#Just default values, these are changed based on the dat file
horizontal = 1 
vertical = 1

#initialize the dictionary for storing parameters given in the dat file 
initial_data = {'photon': {}, 'horizontal': {}, 'vertical': {}}
matrix = [[]] 

""" 
Get data from the dat file with the parameters for the scan. Put this data into an organized Dictionary
"""
def get_parameters():
    with open('res_int_pr_se.dat') as file:
        line_num = 1
        for line in file:
            if "#" not in line:
                return
            else:
                if line_num == 1:
                    populate_dictionary(line, '[', ']', 'intensity')
                elif 'Initial Photon' in line:
                    populate_dictionary(line, '#', ' ', 'photon', 'Initial_Energy')
                elif 'Final Photon' in line:
                    populate_dictionary(line, '#', ' ', 'photon', 'Final_Energy')
                elif 'Initial Horizontal' in line:
                    populate_dictionary(line, '#', ' ', 'horizontal', 'Initial_Position')
                elif 'Final Horizontal' in line:
                    populate_dictionary(line, '#', ' ', 'horizontal', 'Final_Position')
                elif 'vs Horizontal' in line:
                    populate_dictionary(line, '#', ' ', 'horizontal', 'Points', 'float','horizontal')
                elif 'Initial Vertical' in line:
                    populate_dictionary(line, '#', ' ', 'vertical', 'Initial_Position')
                elif 'Final Vertical' in line:
                    populate_dictionary(line, '#', ' ', 'vertical', 'Final_Position')
                elif 'vs Vertical' in line:
                    populate_dictionary(line, '#', ' ', 'vertical', 'Points', 'float','vertical')

            line_num += 1

"""
Funciton that populates the dictionary based on what values from the line are needed, what type they should be, and if they need to change 
the values of any global varaiables 
"""

def populate_dictionary(line, starting_point, ending_point, d, d1=None, type1='string', v_to_change=0):
    change_h = False
    change_v = False

    if v_to_change is 'horizontal':
        change_h = True
    elif v_to_change is 'vertical':
        change_v = True

    start = line.find(starting_point) + 1
    end = line.find(ending_point)

    if type1 is 'string':
        v_to_change = (line[start:end])
    else:
        v_to_change = int(line[start:end])

    #Checks to see if d1 is actually necessary 
    if not d1:
        initial_data[d] = v_to_change
    else:
        initial_data[d][d1] = v_to_change

    #Checks to see if horizontal / vertical global values should be changed 
    if change_h:
        setHorizontal(v_to_change)
    elif change_v:
        setVertical(v_to_change)


def setHorizontal(value):
    global horizontal
    horizontal = value


def setVertical(value):
    global vertical
    vertical = value


def populate_matrix():
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


def populate_matrix_smart():
    d = np.loadtxt('res_int_pr_se.dat')
    d2 = d.reshape((294, 528))
    global matrix
    matrix = d2


def create_image(): 
   im = plt.imshow(matrix, cmap='gray', aspect="equal")
   plt.colorbar(im, orientation='vertical')
   plt.show()


# np.loadtxt()
# import pandas
if __name__ == '__main__':
    get_parameters()

    #populateMatrixSmart()

    populate_matrix()
    print(initial_data)
    create_image() 
