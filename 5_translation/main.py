# Import necessary libraries
import pygame as pg
from OpenGL.GL import *
import numpy as np
import time

import pyrr
import shaderLoader
from objLoaderV2 import ObjLoader
from guiV1 import SimpleGUI

# Initialize pygame
pg.init()

# Set up OpenGL context version
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)

# Create a window for graphics using OpenGL
width = 640
height = 480
pg.display.set_mode((width, height), pg.OPENGL | pg.DOUBLEBUF)


glClearColor(0.3, 0.4, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)



# Write our shaders. We will write our vertex shader and fragment shader in a different file
shader = shaderLoader.compile_shader("shaders/vert.glsl", "shaders/frag.glsl")
glUseProgram(shader)


# Lets setup our scene geometry.
obj = ObjLoader("objects/teapot.obj")
vertices = np.array(obj.vertices, dtype="float32")
center = obj.center
dia = obj.dia


# *********** Lets define some variables that we will use later ***********
size_position = 3       # x, y, z
size_texture = 2        # u, v
size_normal = 3          # r, g, b

stride = (size_position + size_texture + size_normal) * 4     # stride is the number of bytes between each vertex
offset_position = 0                           # offset of the position data
offset_texture = size_position * 4            # offset of the texture data.
                                              # Texture data starts after 3 floats (12 bytes) of position data
offset_normal = (size_position + size_texture) * 4     # offset of the normal data.
                                                       # Normal data starts after 5 floats (20 bytes) of position and texture data
n_vertices = len(obj.vertices) // (size_position + size_texture + size_normal)   # number of vertices

scale = 2/dia           # scale factor for the model
center = obj.center     # center of the model
aspect = width/height   # aspect ratio of the window


translate_mat1 = pyrr.matrix44.create_from_translation(-center)

# *************************************************************************



# Create a Vertex Array Object (VAO) to store the following
#   vertex attribute configurations
#   vertex buffer objects associated with vertex attributes
vao = glGenVertexArrays(1)
glBindVertexArray(vao)                 # Bind the VAO. That is, make it the active one.


# Create a Vertex Buffer Object (VBO) to store the vertex data
vbo = glGenBuffers(1)                  # Generate one buffer and store its ID.
glBindBuffer(GL_ARRAY_BUFFER, vbo)     # Bind the buffer. That is, make it the active one.
glBufferData(GL_ARRAY_BUFFER,
             size=obj.vertices.nbytes,
             data=obj.vertices,
             usage=GL_STATIC_DRAW)   # Upload the data to the GPU.


# *********** Define the vertex attribute configurations ***********
# This is where we specify how the data is stored in the VBO.
# For the position attribute
position_loc = 0
glVertexAttribPointer(index=position_loc,           # Now we specify how the data is stored in the VBO for the position attribute
                      size=size_position,           # Specify the number of components per attribute: 3 for position (x, y, z)
                      type=GL_FLOAT,                # Specify the type of the components
                      normalized=GL_FALSE,          # Specify if we want the data to be normalized
                      stride=stride,                # Specify the stride (number of bytes between each vertex)
                      pointer=ctypes.c_void_p(offset_position))   # Specify the starting point (in bytes) for the position data
# Enable the position attribute using its index
glEnableVertexAttribArray(position_loc)

# For the normal attribute
normal_loc = 1
glVertexAttribPointer(normal_loc,                    # Now we specify how the data is stored in the VBO for the normal attribute
                      size=size_normal,
                      type=GL_FLOAT,
                      normalized=GL_FALSE,
                      stride=stride,
                      pointer=ctypes.c_void_p(offset_normal))   # The starting point for the normal data (in bytes)
# Enable the vertex attribute (normal) using its index
glEnableVertexAttribArray(normal_loc)
# *****************************************************************



# *********** Configure uniform variables ***********
aspect_loc = glGetUniformLocation(shader, "aspect")  # Get the location of the uniform variable "aspect" in the shader
glUniform1f(aspect_loc, aspect)                       # Set the value of the uniform variable "aspect" in the shader

model_mat_loc = glGetUniformLocation(shader, "model_matrix")  # Get the location of the uniform variable "model_mat" in the shader

# **************************************************



# Create a slider using TKinter to change the scale and translate the model in the y direction

gui = SimpleGUI("Transformation")
scale_slider = gui.add_slider("Scale", min_value=0.5 * scale, max_value=2 * scale, initial_value=scale)
translateY_slider = gui.add_slider("TranslateY", min_value=-1.25, max_value=1.25, initial_value=0)





# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # scaling
    scale = scale_slider.get_value()
    # second translation
    tx = np.sin(time.time()) * 0.5
    ty = translateY_slider.get_value()
    tz = 0


    # Compute and set the model matrix
    scale_mat = pyrr.matrix44.create_from_scale([scale, scale, scale])
    translate_mat2 = pyrr.matrix44.create_from_translation([tx, ty, tz])

    model_mat = pyrr.matrix44.multiply(translate_mat1, scale_mat)   # Bring the model to the origin and scale it
    model_mat = pyrr.matrix44.multiply(model_mat, translate_mat2)   # Translate the model again to the desired position given by tx, ty, tz

    glUniformMatrix4fv(model_mat_loc, 1, GL_FALSE, model_mat)   # Set the value of the uniform variable "model_mat" in the shader


    # Draw the triangle
    glUseProgram(shader)                # Use the shader program
    glBindVertexArray(vao)              # Bind the VAO. That is, make it the active one.
    glDrawArrays(GL_TRIANGLES,
                 0,
                 n_vertices)      # Draw the triangle

    # Refresh the display to show what's been drawn
    pg.display.flip()


# Cleanup
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])
glDeleteProgram(shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program