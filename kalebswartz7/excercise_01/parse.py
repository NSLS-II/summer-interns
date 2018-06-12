# Parse the data from the dat file -> Points vs Horizontal Position = how many rows per column in the 2D array 
#                                  -> Points vs Vertical Position = how many columns in the 2D array 

#       Create a dictionary and populate it with other dictionaries based on the data in the dat file 
#       Use this data to add to the graph

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.transforms as tf
from matplotlib import gridspec


def get_parameters(d):
    """
    Read in first 10 lines of input file to get parameters for data 

    Parameters
    ----------
    d : dictionary
        dictionary that is going to be populated by the parameter data

    """
    with open('res_int_pr_se.dat') as file:
        for i in range(10):
            line = file.readline()
            if '/' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='[', ending_point=']',
                d='intensity', type1='string')
            elif 'Initial Photon' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='#', ending_point=' ',
                d='photon', d1='initial_energy')
            elif 'Final Photon' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='#', ending_point=' ',
                d='photon', d1='final_energy')
                populate_dictionary(line, d_to_populate = d,
                starting_point='[', ending_point=']',
                d='photon', d1='units', type1='string')
            elif 'Initial Horizontal' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='#', ending_point=' ',
                d='horizontal', d1='initial_position')
            elif 'Final Horizontal' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='#', ending_point=' ',
                d='horizontal', d1='final_position')
                populate_dictionary(line, d_to_populate = d,
                starting_point='[', ending_point=']',
                d='horizontal', d1='units', type1='string')
            elif 'vs Horizontal' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='#', ending_point=' ',
                d='horizontal', d1='points', type1='int')
            elif 'Initial Vertical' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='#', ending_point=' ',
                d='vertical', d1='initial_position')
            elif 'Final Vertical' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='#', ending_point=' ',
                d='vertical', d1='final_position')
                populate_dictionary(line, d_to_populate = d,
                starting_point='[', ending_point=']',
                d='vertical', d1='units', type1='string')
            elif 'vs Vertical' in line:
                populate_dictionary(line, d_to_populate = d,
                starting_point='#', ending_point=' ',
                d='vertical', d1='points', type1='int')


def populate_dictionary(line, d_to_populate, starting_point,
    ending_point, d, d1=None, type1='float'):
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
    Reads in all non-commented data from file, parses into 2D array
    based on Horizontal and Vertical Points

    Parameters
    ----------
    matrix : 2D array 
        array that will be populated by the data parsed in the input file
    horizontal : int 
        # of horizontal rows in matrix
    vertical : int
        # of vertical rows in matrix
    
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
    Reads in all non-commented data from file, parses into 2D array based
    on Horizontal and Vertical Points (using numpy)

    Parameters
    ----------
    matrix : 2D array 
        array that will be populated by the data parsed in the input file
    horizontal : int 
        # of horizontal rows in matrix
    vertical : int
        # of vertical rows in matrix
    
    """
    d = np.loadtxt('res_int_pr_se.dat')
    d2 = d.reshape((vertical, horizontal))
    matrix = d2
    return matrix


def _display(matrix, initial_data):
    """
    Creates 2D image based on data points in matrix

    Parameters
    ----------
    matrix : 2D array 
        array that contains data for image
    initial_data : Dictionary
        contains paramter data from Dat file
    
    """
    fig = _create_figure()
    ax1 = fig.get_axes()[0]
    ax2 = fig.get_axes()[1]
    ax3 = fig.get_axes()[2]

    horizontal_initial = _unit_change(initial_data['horizontal']
                                      ['initial_position'], 'micro')
    horizontal_final = _unit_change(initial_data['horizontal']
                                    ['final_position'], 'micro')
    vertical_initial = _unit_change(initial_data['vertical']
                                    ['initial_position'], 'micro')
    vertical_final = _unit_change(initial_data['vertical']
                                  ['final_position'], 'micro')
    initial_array_horiz = 0
    initial_array_vert = 0

    # Subplot 1:
    ax1.imshow(matrix, aspect = 1.5,
                    extent=(
                         horizontal_initial, horizontal_final,
                         vertical_initial, vertical_final), cmap='gray'
                    )
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title(f'After Propagation (E= {initial_data["photon"]["final_energy"]}'
                  f' {initial_data["photon"]["units"]})', weight='extra bold')
    line_v = ax1.axvline(lw='1')
    line_h = ax1.axhline(lw='1')

    #Subplot 2:
    _create_horizontal_slice(ax2, initial_array_horiz)

    #Subplot 3:
    _create_vertical_slice(ax3, initial_array_vert)

    mouse = create_mouse(fig, line_h, line_v, initial_array_horiz)
    plt.show()

def _create_figure():
    """
    Creates 8x6 figure for subplots to be located

    """
    fig = plt.figure(1, figsize=(8, 6))
    ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid((3, 3), (2, 0), colspan=2)
    ax3 = plt.subplot2grid((3, 3), (0, 2), rowspan=2)
    return fig

def _create_horizontal_slice(axis, array_number):
    """
    Creates horizontal slice of 2D image

    Parameters
    ----------
    axis : subplot/axis
        axis / subplot for the slice plot to be located
    array_number : int
        location in 2D array for horizontal slice to occur

    """
    axis.plot(matrix[array_number])
    axis.set_aspect('auto')
    axis.set_xlabel('Horizontal Position [µm]', weight='semibold')
    _draw_lines(axis, 'x')

def _create_vertical_slice(axis, array_number):
    """
        Creates vertical slice of 2D image

        Parameters
        ----------
        axis : subplot/axis
            axis / subplot for the slice plot to be located
        array_number : int
            location in 2D array for vertical slice to occur

        """
    vertical = []
    for i in matrix:
        vertical.append(i[array_number])

    init_pos = plt.gca().transData
    new_pos = tf.Affine2D().rotate_deg(90)
    axis.plot(vertical, transform=new_pos + init_pos)

    axis.get_yaxis().set_ticks_position(position='right')
    axis.get_xaxis().set_ticks_position(position='bottom')
    axis.set_xlabel(f'Intensity [{initial_data["intensity"]}]',
                   weight='semibold', labelpad=20)
    axis.set_ylabel('Vertical Position [µm]', weight='semibold')
    axis.yaxis.set_label_position('right')
    _draw_lines(axis, 'y')



class create_mouse:
    def __init__(self, figure, horizontal_line, vertical_line, horiz_array):
        """
        Initialize mouse click class

        Parameters
        ----------
        figure : figure
            figure being clicked
        horizontal_line : axhline
            horizontal line being adjusted to slice based on click
        vertical_line : axvline
            vertical line being adjusted to slice based on click

        """
        self.figure = figure
        self.horizontal_line = horizontal_line
        self.vertical_line = vertical_line
        self.horiz_array = horiz_array
        self.cid = figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        """
        Called during a mouse click, displays location of point clicked and
        changes vertical/horizontal slice lines

        Parameters
        ----------
        event : event
            event that occurs on mouse click

        """
        if event.xdata != None and event.ydata != None:
            coordinates = f'x: {event.xdata:.4} y: {event.ydata:.4}'
            self.figure.suptitle(coordinates, x=0.18, y=0.95, fontsize = 12)
            if event.inaxes is self.figure.get_axes()[0]:
                self.horizontal_line.set_ydata(event.ydata)
                self.vertical_line.set_xdata(event.xdata)
                self.figure.get_axes()[1].clear()
                _create_horizontal_slice(self.figure.get_axes()[1],
                                         int(event.xdata))
                self.figure.get_axes()[2].clear()
                _create_vertical_slice(self.figure.get_axes()[2],
                                         int(event.ydata))
            self.figure.canvas.draw()


def _draw_lines(plot, x_or_y):
    """
    Draws lines for all points on specified axis

    Paramters
    ---------
    plot :  subplot
        subplot that the lines are added to
    x_or_y : string
        string that indicates which axis the lines are added to
    """
    if x_or_y is 'x':
        for i in plot.get_xticks():
            plot.axvline(i, lw='0.15', color='gray')
    else:
        for i in plot.get_yticks():
            plot.axhline(i, lw='0.15', color='gray')


def _unit_change(value_to_be_changed, unit):
    """
    Changes value based on given unit

    Parameters
    ----------
    value_to_be_changed : float
        value that is returned once it is changed
    unit : string
        unit the value should be converted to

    """
    if unit is 'micro':
        return value_to_be_changed * 1e6
    elif unit is 'nano':
        return value_to_be_changed * 1e9


if __name__ == '__main__':
    initial_data = {'photon': {}, 'horizontal': {}, 'vertical': {},}
    matrix = [[]] 

    get_parameters(initial_data)
    horizontal = initial_data['horizontal']['points']
    vertical = initial_data['vertical']['points']

    matrix = populate_matrix_smart(matrix, horizontal, vertical)
    matrix = populate_matrix(matrix, horizontal, vertical)
    print(initial_data)
    _display(matrix, initial_data)
