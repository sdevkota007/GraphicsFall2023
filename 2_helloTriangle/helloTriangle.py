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
stride = (size_position + size_color) * 4           # stride is the number of bytes between each vertex
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
position_loc = glGetAttribLocation(shader, "position")      # Get the index of the position attribute in the shader
glVertexAttribPointer(index=position_loc,           # Now we specify how the data is stored in the VBO for the position attribute
                      size=3,                       # Specify the number of components per attribute: 3 for position (x, y, z)
                      type=GL_FLOAT,                # Specify the type of the components
                      normalized=GL_FALSE,          # Specify if we want the data to be normalized
                      stride=24,                    # Specify the stride (number of bytes between each vertex)
                      pointer=ctypes.c_void_p(0))   # Specify the starting point (in bytes) for the position data
# Enable the position attribute using its index
glEnableVertexAttribArray(position_loc)

# For the color attribute
color_loc = glGetAttribLocation(shader, "color")    # Get the index of the color attribute in the shader
glVertexAttribPointer(color_loc,                    # Now we specify how the data is stored in the VBO for the color attribute
                      3,
                      GL_FLOAT,
                      GL_FALSE,
                      24,
                      ctypes.c_void_p(12))          # The starting point for the color data is 12 bytes after the starting point for the position data

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
    glDrawArrays(GL_TRIANGLES, 0, 3)

    # Refresh the display to show what's been drawn
    pg.display.flip()


pg.quit()   # Close the graphics window
quit()      # Exit the program