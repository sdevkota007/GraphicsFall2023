import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoaderV3
from utils import load_image

# Initialize pygame
pg.init()

# Set up OpenGL context version
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)

# Create a window for graphics using OpenGL
width = 640
height = 480
pg.display.set_mode((width, height), pg.OPENGL | pg.DOUBLEBUF)


# Set the background color (clear color)
# glClearColor takes 4 arguments: red, green, blue, alpha. Each argument is a float between 0 and 1.
glClearColor(0.3, 0.4, 0.5, 1.0)


# Write our shaders. We will write our vertex shader and fragment shader in a different file
shaderProgram = shaderLoaderV3.ShaderProgram("shaders/vert.glsl", "shaders/frag.glsl")
glUseProgram(shaderProgram.shader)    # Use the shader program


# Define the vertices of the quad.
vertices = (
            # Position        # texture         # color
            -0.5, -0.5, 0.0,    0.0, 0.0,         1.0, 0.0, 0.0,      # vertex 1
             0.5, -0.5, 0.0,    1.0, 0.0,         0.0, 1.0, 0.0,      # vertex 2
             0.5,  0.5, 0.0,    1.0, 1.0,         0.0, 0.0, 1.0,       # vertex 3

            -0.5, -0.5, 0.0,    0.0, 0.0,         1.0, 0.0, 0.0,      # vertex 4
             0.5,  0.5, 0.0,    1.0, 1.0,         0.0, 0.0, 1.0,      # vertex 5
            -0.5,  0.5, 0.0,    0.0, 1.0,         0.0, 1.0, 0.0       # vertex 6
)
vertices = np.array(vertices, dtype=np.float32)

size_position = 3       # x, y, z
size_texture = 2        # s, t
size_color = 3          # r, g, b

stride = (size_position + size_texture + size_color) * 4   # size of a single vertex in bytes
offset_position = 0                                 # offset of the position data
offset_texture = size_position * 4                  # offset of the texture data. Texture data starts after 3 floats (12 bytes) of position data
offset_color = (size_position + size_texture) * 4   # offset of the color data. Color data starts after 5 floats (20 bytes) of position and texture data
n_vertices = len(vertices) // (size_position + size_texture + size_color)  # number of vertices


# Create VA0 and VBO
vao = glGenVertexArrays(1)
glBindVertexArray(vao)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)   # Upload the data to the GPU.


# Define the vertex attribute configurations
# we can either query the locations of the attributes in the shader like we did in our previous assignments
# or explicitly tell the shader that the attribute "position" corresponds to location 0.
# It is recommended to explicitly set the locations of the attributes in the shader than querying them.
# Notice the changes in the fragment shader.
# Position attribute
position_loc = 0
glBindAttribLocation(shaderProgram.shader, position_loc, "position")
glVertexAttribPointer(position_loc, size_position, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset_position))
glEnableVertexAttribArray(position_loc)

# texture attribute
texture_loc = 1
glBindAttribLocation(shaderProgram.shader, texture_loc, "uv")
glVertexAttribPointer(texture_loc, size_texture, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset_texture))
glEnableVertexAttribArray(texture_loc)

# color attribute
color_loc = 2
glBindAttribLocation(shaderProgram.shader, color_loc, "color")
glVertexAttribPointer(color_loc, size_color, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset_color))
glEnableVertexAttribArray(color_loc)


img_data, img_width, img_height = load_image("images/img.png", flip=True)
# Create a texture object
tex_id0 = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, tex_id0)        # Bind the texture object. That is, make it the active one.
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)    # Set the texture wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)    # Set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
# Upload the image data to the GPU
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)



img_data, img_width, img_height = load_image("images/img2.png", flip=True)
# Create a texture object
tex_id1 = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, tex_id1)        # Bind the texture object. That is, make it the active one.
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)    # Set the texture wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)    # Set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
# Upload the image data to the GPU
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)



# Set the texture units for the samplers in the fragment shader
shaderProgram["tex0"] = 0
shaderProgram["tex1"] = 1



# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear the screen (or clear the color buffer), and set it to the background color chosen earlier
    glClear(GL_COLOR_BUFFER_BIT)

    '''
    # ******************* Draw the object ************************
    '''
    # ***** Select shader and set uniforms if you have them *****
    glUseProgram(shaderProgram.shader)  # Use the shader program

    # Activate the texture units and bind the textures to them
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex_id0)

    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, tex_id1)

    # ***** Draw *****
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES,0,n_vertices)      # Draw the triangles
    '''
    # *************************************************************
    '''

    # Refresh the display to show what's been drawn
    pg.display.flip()


# Cleanup
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])
glDeleteProgram(shaderProgram.shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program