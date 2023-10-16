import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoaderV3  # Assuming you have a ShaderLoader module
from utils import load_image

# Initialize pygame and create a window.
pg.init()
pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
glClearColor(0.3, 0.4, 0.5, 1)
glEnable(GL_DEPTH_TEST)

# Load the shaders.
shaderProgram = shaderLoaderV3.ShaderProgram("shaders/vert.glsl", "shaders/frag.glsl")

triangle_vertices = (
            # Position          # texture       # Normal
            -0.8, -0.8, 0.0,    0.0, 0.0,       1.0, 0.0, 0.0,
             0.0, -0.8, 0.0,    1.0, 0.0,       0.0, 1.0, 0.0,
            -0.4,  0.0, 0.0,    0.5, 0.5,       0.0, 0.0, 1.0
            )
triangle_vertices = np.array(triangle_vertices, dtype=np.float32)

# Define the quad positions using two triangles
quad_vertices = (
    # Position          # texture       # Normal
    0.0, 0.0, 0.0,      0.0, 0.0,        0.0, 0.0, 1.0,
    0.8, 0.0, 0.0,      1.0, 0.0,        0.0, 0.0, 1.0,
    0.8, 0.8, 0.0,      1.0, 1.0,        0.0, 0.0, 1.0,

    0.0, 0.0, 0.0,      0.0, 0.0,        0.0, 0.0, 1.0,
    0.8, 0.8, 0.0,      1.0, 1.0,        0.0, 0.0, 1.0,
    0.0, 0.8, 0.0,      0.0, 1.0,        0.0, 0.0, 1.0
)

quad_vertices = np.array(quad_vertices, dtype=np.float32)


# Set up the Vertex Array Object (VAO) and Vertex Buffer Object (VBO) for the triangle.
triangle_vao = glGenVertexArrays(1)
glBindVertexArray(triangle_vao)                 # Bind the VAO. That is, make it the active one.
triangle_vbo = glGenBuffers(1)                  # Generate one buffer and store its ID.
glBindBuffer(GL_ARRAY_BUFFER, triangle_vbo)     # Bind the buffer. That is, make it the active one.
glBufferData(GL_ARRAY_BUFFER, triangle_vertices, GL_STATIC_DRAW)    # Upload the data to the GPU.


# Define the vertex attribute configurations
# we can either query the locations of the attributes in the shader like we did in our previous assignments
# or explicitly tell the shader that the attribute "position" corresponds to location 0.
# It is recommended to explicitly set the locations of the attributes in the shader than querying them.
# Notice the changes in the fragment shader.
# Position attribute
pos_loc = 0
texture_loc = 1
normal_loc = 2
glBindAttribLocation(shaderProgram.shader, pos_loc, "position")
glBindAttribLocation(shaderProgram.shader, texture_loc, "uv")
glBindAttribLocation(shaderProgram.shader, normal_loc, "normal")
glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
glVertexAttribPointer(texture_loc, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
glEnableVertexAttribArray(pos_loc)
glEnableVertexAttribArray(texture_loc)
glEnableVertexAttribArray(normal_loc)


# Set up the Vertex Array Object (VAO) and Vertex Buffer Object (VBO) for the quad.
quad_vao = glGenVertexArrays(1)
glBindVertexArray(quad_vao)
quad_vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, quad_vbo)
glBufferData(GL_ARRAY_BUFFER, quad_vertices, GL_STATIC_DRAW)

pos_loc = 0
texture_loc = 1
normal_loc = 2
glBindAttribLocation(shaderProgram.shader, pos_loc, "position")
glBindAttribLocation(shaderProgram.shader, texture_loc, "uv")
glBindAttribLocation(shaderProgram.shader, normal_loc, "normal")
glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
glVertexAttribPointer(texture_loc, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
glEnableVertexAttribArray(pos_loc)
glEnableVertexAttribArray(texture_loc)
glEnableVertexAttribArray(normal_loc)


# Load the textures
texture1 = glGenTextures(1)     # Generate one texture object and store its ID
glBindTexture(GL_TEXTURE_2D, texture1)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

img_data, img_width, img_height = load_image("images/img2.png", flip=True)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
glGenerateMipmap(GL_TEXTURE_2D)     # To Generate mipmaps. Mipmap property is set above using GL_LINEAR_MIPMAP_NEAREST


texture2 = glGenTextures(1)     # Generate one texture object and store its ID
glBindTexture(GL_TEXTURE_2D, texture2)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

img_data, img_width, img_height = load_image("images/img.png", flip=True)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
glGenerateMipmap(GL_TEXTURE_2D)       # To Generate mipmaps. Mipmap property is set above using GL_LINEAR_MIPMAP_NEAREST


# ***** Attach the uniform sampler variable "tex" in the shader to the texture unit 0.  *****
# We can explicitly tell the shader that the sampler "tex" corresponds to texture unit 0.
# This is optional since we are using only one texture unit. It is attached to texture unit 0 (GL_TEXTURE0) by default,
# but a wise man once said, "Explicit is better than implicit."
shaderProgram["tex"] = 0   # Okay this might be confusing. Here 0 indicates texture unit 0. Note that "tex" is a sampler variable in the fragment shader. It is not an integer.
# instead of the line above, we could have used the following lines:
# glUseProgram(shaderProgram.shader)
# tex_loc = glGetUniformLocation(shaderProgram.shader, "tex")
# glUniform1i(tex_loc, 0)


# Set up the game loop.
draw = True
while (draw):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    glUseProgram(shaderProgram.shader)

    # Activate texture unit 0. This is the default, but it is good practice to explicitly set it.
    # GPU's may have 16, 32, or even more texture units. Can be done only once outside the game loop since we are using only one texture unit.
    glActiveTexture(GL_TEXTURE0)

    # Bind the correct texture to the active texture unit, bind the correct VAO, and draw the triangle.
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBindVertexArray(triangle_vao)
    glDrawArrays(GL_TRIANGLES, 0, len(triangle_vertices) // 6)

    # Bind the correct texture to the active texture unit, bind the correct VAO, and draw the quad.
    glBindTexture(GL_TEXTURE_2D, texture2)
    glBindVertexArray(quad_vao)
    glDrawArrays(GL_TRIANGLE_FAN, 0, len(quad_vertices) // 6)

    pg.display.flip()


# Clean up
glDeleteVertexArrays(1, [triangle_vao])
glDeleteBuffers(1, [triangle_vbo])
glDeleteVertexArrays(1, [quad_vao])
glDeleteBuffers(1, [quad_vbo])
glDeleteProgram(shaderProgram.shader)
pg.quit()
quit()
