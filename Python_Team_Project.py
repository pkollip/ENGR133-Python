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
    [TEAM ] understand the assignment expectations without
        telling me how they will approach it.
    [TEAM ] understand different ways to think about a solution
        without helping me plan my solution.
    [TEAM] think through the meaning of a specific error or
        bug present in my code without looking at my code.
===============================================================================
"""
 
 
import numpy as np
import matplotlib.pyplot as plot
 
def file_check(file):
    file = input('Enter the name of the image file: ')
   
    # The program will accept an input from the user which must refer to an
    # actual .png file name or it will reprompt the user for an accurate input.
    # Two error messages are present: checking whether the file has a '.png'
    # file extension and checking that the file is reachable/exists.
    if file.lower().endswith(('.png')) == True:
        try:
            image = plot.imread(f'{file}')
            return image, 1, file
       
        except FileNotFoundError:
            print('The file you are looking for does not exist. '
                  'Please enter an actual .png file name.')
            return None, 0, 0
    else:
        print('The file input is not ".png". Please input only .png files.')
        return None, 0, 0
 
 
def grayscale(image):
    red = []
    green = []
    blue = []
    allRGB = []
  
    #Fetches every row and column in the 3D array. Separates the colors.
    red = image[:,:,0]
    green = image[:,:,1]
    blue = image[:,:,2]
  
    # The values below accentuate the brightness and the others
    # accentuate the shadows. Since you're trying to
    # define edges, brighter is probably better.
    R = red * .2126
    G = green * .7152
    B = blue * .0722
  
    allRGB = np.add(R, G, B)
    return allRGB
  
def edge_blur(gray):
    # Dimensions of the image are fetched.
    dimensions = gray.shape
    rows, columns = dimensions
   
    # Creates empty array of black.
    empty_arr = np.zeros(dimensions)
   
    # Gaussian array to weigh each value in the 5x5 matrix of pixels for smoothing.
    mul_arr = np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]])
   
    # Iterates through every row and column, taking 5x5 matrices around each
    # pixel before multiplying element by element the two matrices to smooth.
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
   
    # Artificially takes a partial derivative through matrix multiplication.
    x_arr = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    y_arr = np.array([[-1,-2,-1],[0,-0,0],[1,2,1]])
    for r in range(1, rows - 1):
        for c in range(1, columns - 1):
            values = blur[r-1:r+2, c-1:c+2]
           
            # Creates two images in the same way the blur function works, but
            # now multiplied by a different matrix. These images are then
            # combined.
            values_multx = np.sum(np.multiply(values, x_arr))
            values_multy = np.sum(np.multiply(values, y_arr))
            empty_arrx[r][c] = values_multx
            empty_arry[r][c] = values_multy
    combo = ((empty_arrx**2) + (empty_arry**2))**(1/2)
    return combo
 
def threshold(combo, threshold_value):
    dimensions = combo.shape
    rows, columns = dimensions
    empty_arr = np.zeros(dimensions)
    for r in range(1, rows-1):
        for c in range(1, columns - 1):
           
            # The thresholding checks the value of every pixel in the same
            # way other functions have done it. It decides whether the pixel
            # meets an established "threshold" value. Those which do are made
            # black, those which don't are made white. Reverses the coloring of
            # the prior image.
             inquiry = combo[r, c]
             if inquiry <= float(threshold_value):
                 value = 255
             else:
                 value = 0
             empty_arr[r][c] = value
    return empty_arr
   
def main():
    # This while loops keeps recalling the file_check function if the file
    # is not returned (the user does not input an acceptable file).
    file = 0
    x = 0
    while x == 0:
        image, x, file = file_check(file)
       
    # Each function is called and a file is saved with a name corresponding
    # to what stage of processing it is in. The colormap is grayscale.
    gray = grayscale(image)
    plot.imsave(f'Gray_{file}', gray, cmap = 'gray')
 
    blurred = edge_blur(gray)
    plot.imsave(f'Edge_{file}', blurred, cmap = 'gray')
   
    threshold_list = [.45]
    x = 0
    combo = sobel(blurred)
    plot.imsave(f'Sobel_{file}', combo, cmap = 'gray')
 
    final = threshold(combo, threshold_list[0])
    plot.imsave(f'Threshold_{file}', final, cmap = 'gray')
   
    #Prints all the file names that the program outputs to.
    print('\nPhoto manipulation completed and saved to these files:\n \n' 
          f'Gray_{file}\n' 
          f'Edge_{file}\n'
          f'Sobel_{file}\n'
          f'Threshold_{file} \n')
    
    # Creates a loop to tell the user what the last iteration of the program was
    # using for its threshold value and gives them the capacity to change it.
    finish = False
    while finish == False:
        change = input(f'The threshold for "Threshold_{file}" was {threshold_list[x]} (the'
                       ' baseline is .45). Would you like to adjust it? (Y/N): ')
       
        if change.lower() == 'y':
            threshold_value = input('Enter a value between 0 and 1 for the best results.'
                                    ' A higher value will make the image more white while' 
                                    ' a lower value will make the image more black.\n'
                                    'Input a new threshold value: ')
            try:
                float(threshold_value)
                skip = 0
            except ValueError:
                print('Only integers and floats are accepted inputs.')
                skip = 1
            
            if skip == 0:
                threshold_list.append(threshold_value)
                x += 1
                final = threshold(combo, threshold_list[x])
               
                try:
                    plot.imsave(f'Threshold_{file}', final, cmap = 'gray')
                   
                # Sometimes when the file is open, the OS can't write to it, so
                # we use an exception to tell the user to close the file and rewind
                # the counter as well as remove that threshold value from memory.
                except OSError:
                    print(f'Please close Threshold_{file} so it can save.')
                    threshold_list.pop(x)
                    x -= 1
               
        elif change.lower() == 'n':
            finish = True
            plot.imshow(final, cmap = 'gray')
 
        else:
            print('Error: Input either "Y" or "N".')
   
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
 
