# Import necessary libraries
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
pg.display.set_mode((width *2, height), pg.OPENGL | pg.DOUBLEBUF)


# glClearColor(0.3, 0.4, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_SCISSOR_TEST)



# Write our shaders. We will write our vertex shader and fragment shader in a different file
shader = shaderLoader.compile_shader("shaders/vert.glsl", "shaders/frag.glsl")



triangle_vertices = (
            # Position            # Normal
            -0.5, -0.5, 0.0,    1.0, 0.0, 0.0,
             0.5,  0.5, 0.0,    0.0, 1.0, 0.0,
            -0.5,  0.5, 0.0,    0.0, 0.0, 1.0
            )
triangle_vertices = np.array(triangle_vertices, dtype=np.float32)
triangle_n_vertices = len(triangle_vertices) // 6

# Define the quad positions using two triangles
quad_vertices = (
    # Position            # Normal
    0.0, 0.0, 0.0,        0.0, 0.0, 1.0,
    0.8, 0.0, 0.0,        0.0, 1.0, 1.0,
    0.8, 0.8, 0.0,        1.0, 0.0, 0.0,

    0.0, 0.0, 0.0,        1.0, 0.0, 0.0,
    0.8, 0.8, 0.0,        0.0, 1.0, 0.0,
    0.0, 0.8, 0.0,        0.0, 0.0, 1.0,
)

quad_vertices = np.array(quad_vertices, dtype=np.float32)
quad_n_vertices = len(quad_vertices) // 6

# Set up the Vertex Array Object (VAO) and Vertex Buffer Object (VBO) for the triangle.
triangle_vao = glGenVertexArrays(1)
glBindVertexArray(triangle_vao)                 # Bind the VAO. That is, make it the active one.
triangle_vbo = glGenBuffers(1)                  # Generate one buffer and store its ID.
glBindBuffer(GL_ARRAY_BUFFER, triangle_vbo)     # Bind the buffer. That is, make it the active one.
glBufferData(GL_ARRAY_BUFFER, triangle_vertices, GL_STATIC_DRAW)    # Upload the data to the GPU.


pos_loc = 0
normal_loc = 1
glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(pos_loc)
glEnableVertexAttribArray(normal_loc)


# Set up the Vertex Array Object (VAO) and Vertex Buffer Object (VBO) for the quad.
quad_vao = glGenVertexArrays(1)
glBindVertexArray(quad_vao)
quad_vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, quad_vbo)
glBufferData(GL_ARRAY_BUFFER, quad_vertices, GL_STATIC_DRAW)

pos_loc = 0
normal_loc = 1
glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(pos_loc)
glEnableVertexAttribArray(normal_loc)


# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    # ****************************************** Draw Triangle ******************************************
    glViewport(0, 0, width, height)
    glScissor(0, 0, width, height)
    glClearColor(0.3, 0.4, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Use the shader, bind the VAO for triangle and draw the triangle
    glUseProgram(shader)
    # configure your uniforms if necessary
    glBindVertexArray(triangle_vao)
    glDrawArrays(GL_TRIANGLES,0, triangle_n_vertices)
    # ****************************************************************************************************


    # ****************************************** Draw quad ******************************************
    glViewport(width, 0, width, height)
    glScissor(width, 0, width, height)
    glClearColor(0.2, 0.3, 0.4, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Use the shader, bind the VAO for object 2 and draw the object
    glUseProgram(shader)
    # configure your uniforms if necessary
    glBindVertexArray(quad_vao)
    glDrawArrays(GL_TRIANGLES,0, quad_n_vertices)
    # ****************************************************************************************************


    # Refresh the display to show what's been drawn
    pg.display.flip()


# Cleanup
glDeleteVertexArrays(1, [triangle_vao, quad_vao])
glDeleteBuffers(1, [quad_vbo, quad_vbo])
glDeleteProgram(shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program