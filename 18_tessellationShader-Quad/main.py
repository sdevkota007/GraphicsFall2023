import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoaderV4
from objLoaderV4 import ObjLoader
from guiV3 import SimpleGUI
import pyrr


def upload_and_configure_attributes(object, shader=None):
    # VAO and VBO
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, object.vertices.nbytes, object.vertices, GL_STATIC_DRAW)

    # Define the vertex attribute configurations
    # we can either query the locations of the attributes in the shader like we did in our previous assignments
    # or explicitly tell the shader that the attribute "position" corresponds to location 0.
    # It is recommended to explicitly set the locations of the attributes in the shader than querying them.
    # Position attribute
    position_loc = 0
    tex_coord_loc = 1
    normal_loc = 2
    glVertexAttribPointer(position_loc, object.size_position, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_position))
    glVertexAttribPointer(tex_coord_loc, object.size_texture, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_texture))
    glVertexAttribPointer(normal_loc, object.size_normal, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_normal))

    glEnableVertexAttribArray(tex_coord_loc)
    glEnableVertexAttribArray(position_loc)
    glEnableVertexAttribArray(normal_loc)

    return vao, vbo, object.n_vertices


'''
# Program starts here
'''


# Initialize pygame
pg.init()

# Set up OpenGL context version
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_STENCIL_SIZE, 8)

# Create a window for graphics using OpenGL
width = 1280
height = 720
pg.display.set_mode((width, height), pg.OPENGL | pg.DOUBLEBUF)



# Set the background color (clear color)
# glClearColor takes 4 arguments: red, green, blue, alpha. Each argument is a float between 0 and 1.
glClearColor(0.3, 0.4, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)


# Write our shaders.
shaderProgram = shaderLoaderV4.ShaderProgram(vs="shaders/vert.glsl",
                                             fs="shaders/frag.glsl",
                                             tcs="shaders/tcs.glsl",
                                             tes="shaders/tes.glsl")


# Obj and attributes
vertices = np.array([
    # positions        # texture coords    # normal
    -1.0, -1.0, 0.0,    0.0, 0.0,           0.0, 0.0, 1.0,
     1.0, -1.0, 0.0,    1.0, 0.0,           0.0, 0.0, 1.0,
     1.0,  1.0, 0.0,    1.0, 1.0,           0.0, 0.0, 1.0,
    -1.0,  1.0, 0.0,    0.0, 1.0,           0.0, 0.0, 1.0
], dtype=np.float32)
n_vertices = 4
size_position = 3
size_texture = 2
size_normal = 3
stride = (size_position + size_texture + size_normal) * vertices.itemsize
offset_position = 0
offset_texture = size_position * vertices.itemsize
offset_normal = (size_position + size_texture) * vertices.itemsize


vao = glGenVertexArrays(1)
glBindVertexArray(vao)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Define the vertex attribute configurations
# we can either query the locations of the attributes in the shader like we did in our previous assignments
# or explicitly tell the shader that the attribute "position" corresponds to location 0.
# It is recommended to explicitly set the locations of the attributes in the shader than querying them.
# Position attribute
position_loc = 0
tex_coord_loc = 1
normal_loc = 2
glVertexAttribPointer(position_loc, size_position, GL_FLOAT, GL_FALSE, stride,
                      ctypes.c_void_p(offset_position))
glVertexAttribPointer(tex_coord_loc, size_texture, GL_FLOAT, GL_FALSE, stride,
                      ctypes.c_void_p(offset_texture))
glVertexAttribPointer(normal_loc, size_normal, GL_FLOAT, GL_FALSE, stride,
                      ctypes.c_void_p(offset_normal))

glEnableVertexAttribArray(tex_coord_loc)
glEnableVertexAttribArray(position_loc)
glEnableVertexAttribArray(normal_loc)


# matrices
scaling_mat = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.5, 0.5, 0.5]))
model_mat = scaling_mat

# matrices
gui = SimpleGUI("GUI")
outerLevel0 = gui.add_slider("outerLevel0", 1, 20, 1, resolution=1)
outerLevel1 = gui.add_slider("outerLevel1", 1, 20, 1, resolution=1)
outerLevel2 = gui.add_slider("outerLevel2", 1, 20, 1, resolution=1)
outerLevel3 = gui.add_slider("outerLevel3", 1, 20, 1, resolution=1)

innerLevel0 = gui.add_slider("innerLevel0", 1, 20, 1, resolution=1)
innerLevel1 = gui.add_slider("innerLevel1", 1, 20, 1, resolution=1)

wireframe = gui.add_checkbox("wireframe", False)


# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set the uniform variables
    shaderProgram["modelMatrix"] = model_mat
    shaderProgram["modelMatrix"] = model_mat
    shaderProgram["outerLevel0"] = int(outerLevel0.get_value())
    shaderProgram["outerLevel1"] = int(outerLevel1.get_value())
    shaderProgram["outerLevel2"] = int(outerLevel2.get_value())
    shaderProgram["outerLevel3"] = int(outerLevel3.get_value())
    shaderProgram["innerLevel0"] = int(innerLevel0.get_value())
    shaderProgram["innerLevel1"] = int(innerLevel1.get_value())

    if wireframe.get_value():
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Use our shader program
    glUseProgram(shaderProgram.shader)
    glBindVertexArray(vao)
    # glDrawArrays(GL_TRIANGLES, 0, obj.n_vertices)

    glPatchParameteri(GL_PATCH_VERTICES, n_vertices)
    glDrawArrays(GL_PATCHES, 0, n_vertices)

    # Refresh the display to show what's been drawn
    pg.display.flip()



# Cleanup
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])

glDeleteProgram(shaderProgram.shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program