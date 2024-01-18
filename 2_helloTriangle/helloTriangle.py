import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoader

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
shader = shaderLoader.compile_shader("shaders/vert.glsl", "shaders/frag.glsl")


# Lets setup our scene geometry. Our scene has just a single triangle for now.
# Define the vertices of the triangle.
vertices = (
            # Position        # color
            0.0, 0.0, 0.0,    1.0, 0.0, 0.0,        # vertex 1
            0.8, 0.0, 0.0,    0.0, 1.0, 0.0,        # vertex 2
            0.8, 0.8, 0.0,    0.0, 0.0, 1.0         # vertex 3
            )
vertices = np.array(vertices, dtype=np.float32)

size_position = 3       # x, y, z
size_color = 3          # r, g, b
stride = (size_position + size_color) * 4     # stride is the number of bytes between each vertex
offset_position = 0                           # offset of the position data
offset_color = size_position * 4              # offset of the color data. Color data starts after 3 floats (12 bytes) of position data
n_vertices = len(vertices) // (size_position + size_color)   # number of vertices


# Create a Vertex Array Object (VAO) to store the following
#   vertex attribute configurations
#   vertex buffer objects associated with vertex attributes
vao = glGenVertexArrays(1)
glBindVertexArray(vao)                 # Bind the VAO. That is, make it the active one.

# Create a Vertex Buffer Object (VBO) to store the vertex data
vbo = glGenBuffers(1)                  # Generate one buffer and store its ID.
glBindBuffer(GL_ARRAY_BUFFER, vbo)     # Bind the buffer. That is, make it the active one.
glBufferData(GL_ARRAY_BUFFER,
             size=vertices.nbytes,
             data=vertices,
             usage=GL_STATIC_DRAW)   # Upload the data to the GPU.


# Define the vertex attribute configurations
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

# For the color attribute
color_loc = 1
glVertexAttribPointer(color_loc,                    # Now we specify how the data is stored in the VBO for the color attribute
                      size=size_color,
                      type=GL_FLOAT,
                      normalized=GL_FALSE,
                      stride=stride,
                      pointer=ctypes.c_void_p(offset_color))   # The starting point for the color data (in bytes)

# Enable the vertex attribute (color) using its index
glEnableVertexAttribArray(color_loc)


# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear the screen (or clear the color buffer), and set it to the background color chosen earlier
    glClear(GL_COLOR_BUFFER_BIT)

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