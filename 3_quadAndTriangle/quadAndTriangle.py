import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoader  # Assuming you have a ShaderLoader module

# Initialize pygame and create a window.
pg.init()
pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
glClearColor(0.3, 0.4, 0.5, 1)

# Load the shaders.
shader = shaderLoader.compile_shader("shaders/vert.glsl", "shaders/frag.glsl")
glUseProgram(shader)

triangle_vertices = (
            # Position            # Normal
            -0.8, -0.8, 0.0,    1.0, 0.0, 0.0,
             0.0,  0.0, 0.0,    0.0, 1.0, 0.0,
            -0.8,  0.0, 0.0,    0.0, 0.0, 1.0
            )
triangle_vertices = np.array(triangle_vertices, dtype=np.float32)

# Define the quad positions using two triangles
quad_vertices = (
    # Position            # Normal
    0.0, 0.0, 0.0,        0.0, 0.0, 1.0,
    0.8, 0.0, 0.0,        0.0, 0.0, 1.0,
    0.8, 0.8, 0.0,        0.0, 0.0, 1.0,

    0.0, 0.0, 0.0,        0.0, 0.0, 1.0,
    0.8, 0.8, 0.0,        0.0, 0.0, 1.0,
    0.0, 0.8, 0.0,        0.0, 0.0, 1.0,
)

quad_vertices = np.array(quad_vertices, dtype=np.float32)


# Set up the Vertex Array Object (VAO) and Vertex Buffer Object (VBO) for the triangle.
triangle_vao = glGenVertexArrays(1)
glBindVertexArray(triangle_vao)                 # Bind the VAO. That is, make it the active one.
triangle_vbo = glGenBuffers(1)                  # Generate one buffer and store its ID.
glBindBuffer(GL_ARRAY_BUFFER, triangle_vbo)     # Bind the buffer. That is, make it the active one.
glBufferData(GL_ARRAY_BUFFER, triangle_vertices, GL_STATIC_DRAW)    # Upload the data to the GPU.


pos_loc = glGetAttribLocation(shader, "position")
normal_loc = glGetAttribLocation(shader, "normal")
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(pos_loc)
glEnableVertexAttribArray(normal_loc)


# Set up the Vertex Array Object (VAO) and Vertex Buffer Object (VBO) for the quad.
quad_vao = glGenVertexArrays(1)
glBindVertexArray(quad_vao)
quad_vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, quad_vbo)
glBufferData(GL_ARRAY_BUFFER, quad_vertices, GL_STATIC_DRAW)

pos_loc = glGetAttribLocation(shader, "position")
normal_loc = glGetAttribLocation(shader, "normal")
glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(pos_loc)
glEnableVertexAttribArray(normal_loc)


# Set up the game loop.
draw = True
while (draw):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the cube but bind the VAO for the triangle first
    glBindVertexArray(triangle_vao)
    glDrawArrays(GL_TRIANGLES, 0, len(triangle_vertices) // 6)

    # Draw the sphere but bind the VAO for the quad first
    glBindVertexArray(quad_vao)
    glDrawArrays(GL_TRIANGLE_FAN, 0, len(quad_vertices) // 6)

    pg.display.flip()


# Clean up
glDeleteVertexArrays(1, [triangle_vao])
glDeleteBuffers(1, [triangle_vbo])
glDeleteVertexArrays(1, [quad_vao])
glDeleteBuffers(1, [quad_vbo])
glDeleteProgram(shader)
pg.quit()
quit()
