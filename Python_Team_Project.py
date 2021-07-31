#!/usr/bin/env python3

"""
===============================================================================
ENGR 133 Summer 2021
 
Program Description:
    The program prompts the user until an input PNG image file is given.
    This image is then ran through a Gaussian noise removal/smoothing function.
    This de-noised image is saved and ran through a Sobel function to define the
    edges of the image, outputting a file with edges in white and everything else
    black. Then, the edge-detected image is inverted in color with thresholds defined
    for turning to black or white. A final white-background and black-edge image is
    saved.
 
 
Assignment Information
    Assignment:     Python Project
    Author:         Garrett Lail, glail@purdue.edu
    Team ID:        #3
                   
Contributor:    Isaak Solochek, isolochek@purdue.edu
                Praval Sai Kollipara, pkollipa@purdue.edu
    My contributor(s) helped me:
    [TEAM] understand the assignment expectations without
        telling me how they will approach it.
    [TEAM] understand different ways to think about a solution
        without helping me plan my solution.
    [TEAM] think through the meaning of a specific error or
        bug present in my code without looking at my code.
 
No contributors.
===============================================================================
"""
 
 
import numpy as np
import matplotlib.pyplot as plot
 
def file_check(file):
    file = input('Enter the name of the image file: ')
    try:
        image = plot.imread(f'{file}')
        return image, 1, file
   
    except AttributeError:
        print('Please enter an actual .png file name.')
        return None, 0, 0
   
    except FileNotFoundError:
        print('Please enter an actual .png file name.')
        return None, 0, 0
 
 
def grayscale(image):
    red = []
    green = []
    blue = []
    allRGB = []
  
    red = image[:,:,0]#colons are to reference all of the rows and columns
    green = image[:,:,1]
    blue = image[:,:,2]
  
    #The values below accentuate the brigthness and the others
    #accentuate the shadows. Since you're trying to
    #define edges, brighter is probably better.
    R = red * .2126
    G = green * .7152
    B = blue * .0722
  
    allRGB = np.add(R, G, B)
    return allRGB
  
def edge_blur(gray):
    dimensions = gray.shape
    rows, columns = dimensions
    empty_arr = np.zeros(dimensions)
    mul_arr = np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]])
    for r in range(2, rows - 2):
        for c in range(2, columns - 2):
             temp_sum = gray[r-2:r+3, c-2:c+3]
             temp_mul_sum = np.sum(np.multiply(mul_arr, temp_sum))
             empty_arr[r][c] = temp_mul_sum/256
    return empty_arr
 
 
def sobel(blur):
    dimensions = blur.shape
    rows, columns = dimensions
    empty_arrx = np.zeros(dimensions)
    empty_arry = np.zeros(dimensions)
    x_arr = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    y_arr = np.array([[-1,-2,-1],[0,-0,0],[1,2,1]])
    for r in range(1, rows - 1):
        for c in range(1, columns - 1):
            values = blur[r-1:r+2, c-1:c+2]
            values_multx = np.sum(np.multiply(values, x_arr))
            values_multy = np.sum(np.multiply(values, y_arr))
            empty_arrx[r][c] = values_multx
            empty_arry[r][c] = values_multy
    combo = ((empty_arrx**2) + (empty_arry**2))**(1/2)
    return combo
 
def threshold(combo):
    dimensions = combo.shape
    rows, columns = dimensions
    empty_arr = np.zeros(dimensions)
    for r in range(1, rows-1):
        for c in range(1, columns - 1):
             inquiry = combo[r, c]
             if inquiry <=  .45:
                 value = 255
             else:
                 value = 0
             empty_arr[r][c] = value
    return empty_arr
   
def main():
    file = 0
    x = 0
    while x == 0:
        image, x, file = file_check(file)
    gray = grayscale(image)
    plot.imsave(f'Gray_{file}', gray, cmap = 'gray')
 
    blurred = edge_blur(gray)
    plot.imsave(f'Edge_{file}', blurred, cmap = 'gray')
   
    combo = sobel(blurred)
    plot.imsave(f'Sobel_{file}', combo, cmap = 'gray')
 
    final = threshold(combo)
    plot.imsave(f'Threshold_{file}', final, cmap = 'gray')
   
if __name__ == '__main__':
    main()
      
 
"""
===============================================================================
ACADEMIC INTEGRITY STATEMENT
    I have not used source code obtained from any other unauthorized
    source, either modified or unmodified. Neither have I provided
    access to my code to another. The project I am submitting
    is my own original work.
===============================================================================
"""
 