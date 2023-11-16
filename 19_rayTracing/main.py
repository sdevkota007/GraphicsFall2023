import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoaderV4
from objLoaderV4 import ObjLoader
from guiV3 import SimpleGUI
import pyrr
import os

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
                                             fs="shaders/frag.glsl")

# Camera parameters
eye = (0,0,2)
target = (0,0,0)
up = (0,1,0)

fov = 45
aspect = width/height
near = 0.1
far = 10


# Obj and attributes
obj = ObjLoader("objects/square.obj")
vao_obj, vbo_obj, n_vertices_obj = upload_and_configure_attributes(obj)

# matrices
scaling_mat = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.5, 0.5, 0.5]))
model_mat = scaling_mat

# matrices
gui = SimpleGUI("GUI")

# Create a slider for the rotation angle around the Z axis
camera_rotY_slider = gui.add_slider("camera Y angle", -180, 180, 0, resolution=1)
camera_rotX_slider = gui.add_slider("camera X angle", -90, 90, 0, resolution=1)
fov_slider = gui.add_slider("fov", 25, 120, 60, resolution=1)

background_color = gui.add_color_picker("Background Color", initial_color=(0.3, 0.4, 0.5))


# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    rotateY_mat = pyrr.matrix44.create_from_y_rotation(np.deg2rad(camera_rotY_slider.get_value()))
    rotateX_mat = pyrr.matrix44.create_from_x_rotation(np.deg2rad(camera_rotX_slider.get_value()))
    rotation_mat = pyrr.matrix44.multiply(rotateX_mat, rotateY_mat)
    rotated_eye = pyrr.matrix44.apply_to_vector(rotation_mat, eye)

    view_mat = pyrr.matrix44.create_look_at(rotated_eye, target, up)
    projection_mat = pyrr.matrix44.create_perspective_projection_matrix(fov_slider.get_value(), aspect, near,  far)

    # Set the uniform variables
    shaderProgram["modelMatrix"] = model_mat
    shaderProgram["Background"] = background_color.get_color()
    shaderProgram["cameraEye"] = rotated_eye
    shaderProgram["fov"] = np.deg2rad(fov_slider.get_value())

    shaderProgram["minBound"] = (-0.5, -0.5, -0.5)
    shaderProgram["maxBound"] = (0.5, 0.5, 0.5)

    shaderProgram["cameraU"] = pyrr.Vector3([view_mat[0][0], view_mat[1][0], view_mat[2][0]])
    shaderProgram["cameraV"] = pyrr.Vector3([view_mat[0][1], view_mat[1][1], view_mat[2][1]])
    shaderProgram["cameraW"] = pyrr.Vector3([view_mat[0][2], view_mat[1][2], view_mat[2][2]])

    shaderProgram["resolution"] = np.array([width, height], dtype=np.float32)

    # Use our shader program
    glUseProgram(shaderProgram.shader)
    glBindVertexArray(vao_obj)
    glDrawArrays(GL_TRIANGLES, 0, obj.n_vertices)

    # Refresh the display to show what's been drawn
    pg.display.flip()



# Cleanup
glDeleteVertexArrays(1, [vao_obj])
glDeleteBuffers(1, [vbo_obj])

glDeleteProgram(shaderProgram.shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program