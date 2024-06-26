#una convolucion es mas eficiente ayudanto al computador al entender el contenido

#se utiliza un filtro para comparar un pixel segun sus vecinos
#se pueden aplicar filtros para distinguir lineas verticales u horizonaltales por ejemplo

#filtro lineas verticales
#[-1,0,1]
#[-2,0,2]
#[-1,0,1]

#filtro lineas horizontales
#[-1,-2,-1]
#[0,0,0]
#[1,2,1]

#pooling es el proceso de remover pixeles manteniendo info importante
#por ejemplo, un bloque de 16x16 se puede transformar en uno de 4x4

#esto ayuda a marcar aun mas las diferenicas mientras ayuda a comprimir la imagen

#con un filtro se pueden extraer distintos objetos de una imagen como maneos, pies, caras, etc
#por lo tanto, un modelo tambien puede aprender sobre filtros

#link a collab
#https://colab.research.google.com/github/tinyMLx/colabs/blob/master/2-3-3-ExploringConvolutions.ipynb

#una convolucion hace una copia de la imagen por cada filtro que aplica, por eso es importante reducir la calidad de 
#estas aplicando pooling

#Let's start by importing some python libraries.

import cv2
import numpy as np
from scipy import datasets
i = datasets.ascent()

#Next, we can use the pyplot library to draw the image so we know what it looks like.

import matplotlib.pyplot as plt
plt.grid(False)
plt.gray()
plt.axis('off')
plt.imshow(i)
plt.show()

#We can see that this is an image of a stairwell. There are lots of features in here that we can play
# with seeing if we can isolate them -- for example there are strong vertical lines.

#The image is stored as a numpy array, so we can create the transformed image by just copying that array. 
#Let's also get the dimensions of the image so we can loop over it later.

i_transformed = np.copy(i)
size_x = i_transformed.shape[0]
size_y = i_transformed.shape[1]

#Now we can create a filter as a 3x3 array.

# This filter detects edges nicely
# It creates a convolution that only passes through sharp edges and straight
# lines.

#Experiment with different values for fun effects.
#filter = [ [0, 1, 0], [1, -4, 1], [0, 1, 0]]

# A couple more filters to try for fun!
#filter = [ [-1, -2, -1], 
             #[0, 0, 0], 
             #[1, 2, 1]]
filter = [ [-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]

# If all the digits in the filter don't add up to 0 or 1, you 
# should probably do a weight to get it to do so
# so, for example, if your weights are 1,1,1 1,2,1 1,1,1
# They add up to 10, so you would set a weight of .1 if you want to normalize them
weight  = 1

#Now let's create a convolution. We will iterate over the image, leaving a 1 pixel margin, 
#and multiply out each of the neighbors of the current pixel by the value defined in the filter.

#i.e. the current pixel's neighbor above it and to the left will be multiplied by the top left item in the filter etc. etc. 
#We'll then multiply the result by the weight, and then ensure the result is in the range 0-255

#Finally we'll load the new value into the transformed image.

for x in range(1,size_x-1):
  for y in range(1,size_y-1):
      convolution = 0.0
      convolution = convolution + (i[x - 1, y-1] * filter[0][0])
      convolution = convolution + (i[x, y-1] * filter[1][0])
      convolution = convolution + (i[x + 1, y-1] * filter[2][0])
      convolution = convolution + (i[x-1, y] * filter[0][1])
      convolution = convolution + (i[x, y] * filter[1][1])
      convolution = convolution + (i[x+1, y] * filter[2][1])
      convolution = convolution + (i[x-1, y+1] * filter[0][2])
      convolution = convolution + (i[x, y+1] * filter[1][2])
      convolution = convolution + (i[x+1, y+1] * filter[2][2])
      convolution = convolution * weight
      if(convolution<0):
        convolution=0
      if(convolution>255):
        convolution=255
      i_transformed[x, y] = convolution

#Now we can plot the image to see the effect of the convolution!

# Plot the image. Note the size of the axes -- they are 512 by 512
plt.gray()
plt.grid(False)
plt.imshow(i_transformed)
#plt.axis('off')
plt.show() 

#This code will show (4, 4) pooling. Run it to see the output, and you'll see that while the image is 1/4 
#the size of the original in both length and width, the extracted features are maintained!

new_x = int(size_x/4)
new_y = int(size_y/4)
newImage = np.zeros((new_x, new_y))
for x in range(0, size_x, 4):
  for y in range(0, size_y, 4):
    pixels = []
    pixels.append(i_transformed[x, y])
    pixels.append(i_transformed[x+1, y])
    pixels.append(i_transformed[x+2, y])
    pixels.append(i_transformed[x+3, y])
    pixels.append(i_transformed[x, y+1])
    pixels.append(i_transformed[x+1, y+1])
    pixels.append(i_transformed[x+2, y+1])
    pixels.append(i_transformed[x+3, y+1])
    pixels.append(i_transformed[x, y+2])
    pixels.append(i_transformed[x+1, y+2])
    pixels.append(i_transformed[x+2, y+2])
    pixels.append(i_transformed[x+3, y+2])
    pixels.append(i_transformed[x, y+3])
    pixels.append(i_transformed[x+1, y+3])
    pixels.append(i_transformed[x+2, y+3])
    pixels.append(i_transformed[x+3, y+3])
    pixels.sort(reverse=True)
    newImage[int(x/4),int(y/4)] = pixels[0]

# Plot the image. Note the size of the axes -- now 128 pixels instead of 512
plt.gray()
plt.grid(False)
plt.imshow(newImage)
#plt.axis('off')
plt.show() 