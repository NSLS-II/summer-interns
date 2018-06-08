# Parse the data from the dat file -> Points vs Horizontal Position = how many rows per column in the 2D array 
#                                  -> Points vs Vertical Position = how many columns in the 2D array 

#       Create a dictionary and populate it with other dictionaries based on the data in the dat file 
#       Use this data to add to the graph

import numpy as np
import matplotlib.pyplot as plt


def get_parameters(d):
    """
    Read in first 10 lines of input file to get parameters for data 

    Parameters
    ----------
    d : dictionary
        dictionary that is going to be populated by the parameter data
    
    Notes
    -----

    """
    with open('res_int_pr_se.dat') as file:
        for i in range(10):
            line = file.readline()
            if '/' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='[', ending_point=']', d='intensity', type1='string')
            elif 'Initial Photon' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='#', ending_point=' ', d='photon', d1='initial_energy')
            elif 'Final Photon' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='#', ending_point=' ', d='photon', d1='final_energy')
            elif 'Initial Horizontal' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='#', ending_point=' ', d='horizontal', d1='initial_position')
            elif 'Final Horizontal' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='#', ending_point=' ', d='horizontal', d1='final_position')
            elif 'vs Horizontal' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='#', ending_point=' ', d='horizontal', d1='points', type1='int')
            elif 'Initial Vertical' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='#', ending_point=' ', d='vertical', d1='initial_position')
            elif 'Final Vertical' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='#', ending_point=' ', d='vertical', d1='final_position')
            elif 'vs Vertical' in line:
                populate_dictionary(line, d_to_populate = d, starting_point='#', ending_point=' ', d='vertical', d1='points', type1='int')


def populate_dictionary(line, d_to_populate, starting_point, ending_point, d, d1=None, type1='float'):
    """
    Populate dictionary based on wanting a certain portion of a string 

    Parameters
    ----------
    line : string
        string that contains 'substring'
    d_to_populate : dictionary
        first level dictionary to store 'substring'
    starting_point : string
        string character that comes right before 'substring'
    ending_point : string
        string character that comes right after 'substring'
    d : dictionary
        second level dictionary to store 'substring' 
    d1 : dictionary
        third level dictionary to store 'substring', optional
    type1 : string
        what type 'substring' is when stored in dictionary
    
    Notes
    -----

    """
    start = line.find(starting_point) + 1
    end = line.find(ending_point)

    if type1 is 'string':
        substring_value = (line[start:end])
    elif type1 is 'int':
        substring_value = int(line[start:end])
    else:
        substring_value = float(line[start:end])

    #Checks to see if d1 is actually necessary 
    if not d1:
        d_to_populate[d] = substring_value
    else:
        d_to_populate[d][d1] = substring_value


def populate_matrix(matrix, horizontal, vertical):
    """
    Reads in all non-commented data from file, parses into 2D array based on Horizontal and Vertical Points 

    Parameters
    ----------
    matrix : 2D array 
        array that will be populated by the data parsed in the input file
    horizontal : int 
        # of horizontal rows in matrix
    vertical : int
        # of vertical rows in matrix
    
    Notes
    -----
    
    """
    matrix = [[0 for i in range(horizontal)] for j in range(vertical)] 
    with open('res_int_pr_se.dat') as file:
        h, v = 0, 0
        for line in file:
            if '#' not in line:
                matrix[v][h] = float(line)
                if (h < horizontal - 1):
                    h += 1
                else:
                    h = 0
                    v += 1
    return matrix


def populate_matrix_smart(matrix, horizontal, vertical):
    """
    Reads in all non-commented data from file, parses into 2D array based on Horizontal and Vertical Points (using numpy) 

    Parameters
    ----------
    matrix : 2D array 
        array that will be populated by the data parsed in the input file
    horizontal : int 
        # of horizontal rows in matrix
    vertical : int
        # of vertical rows in matrix
    
    Notes
    -----
    
    """
    d = np.loadtxt('res_int_pr_se.dat')
    d2 = d.reshape((vertical, horizontal))
    matrix = d2
    return matrix


def create_image(matrix, initial_data):
    """
    Creates 2D image based on data points in matrix
    Parameters
    ----------
    matrix : 2D array 
        array that contains data for image
    
    Notes
    -----
    
    """
    plt.figure(1)
    plt.subplot(211)
    im = plt.imshow(matrix, aspect=2,
                    extent=(
                        initial_data['horizontal']['initial_position']*1e6, initial_data['horizontal']['final_position']*1e6,
                        initial_data['vertical']['initial_position']*1e6, initial_data['vertical']['final_position']*1e6
                    ))
    # plt.colorbar(im, orientation='vertical')
    plt.xlabel('Horizontal Position [µm]')
    plt.ylabel('Vertical Position [µm]')
    plt.title(f'Photon energy: {initial_data["photon"]["final_energy"]} eV')
    plt.show()


if __name__ == '__main__':
    initial_data = {'photon': {}, 'horizontal': {}, 'vertical': {},}
    matrix = [[]] 

    get_parameters(initial_data)
    horizontal = initial_data['horizontal']['points']
    vertical = initial_data['vertical']['points']

    #matrix = populate_matrix_smart(matrix, horizontal, vertical)
    matrix = populate_matrix(matrix, horizontal, vertical)
    print(initial_data)
    create_image(matrix, initial_data)
