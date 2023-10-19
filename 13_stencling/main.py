import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoaderV3
from objLoaderV4 import ObjLoader
from utils import load_image
from guiV3 import SimpleGUI
import pyrr
import os



def load_2d_texture(filename):
    img_data, img_w, img_h = load_image(filename, format="RGB", flip=True)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)  # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_w, img_h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, 0)

    return texture_id


def set_masking_parameters():
    # Enable stencil test
    glEnable(GL_STENCIL_TEST)

    # Set the stencil function to always pass
    glStencilFunc(GL_ALWAYS, 1, 0xFF)

    # Set the stencil operation to keep the current value
    glStencilOp(GL_REPLACE, GL_REPLACE, GL_REPLACE)

    # disable writing to the color buffer
    glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)

    # enable depth testing and disable writing to the depth buffer
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_FALSE)


def set_stenciling_parameters():
    # Enable stencil test
    glEnable(GL_STENCIL_TEST)

    # Set the stencil function to always pass
    glStencilFunc(GL_EQUAL, 1, 0xFF)

    # Set the stencil operation to keep the current value
    glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)

    # enable writing to the color buffer
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glDepthMask(GL_TRUE)


def set_default_parameters():
    # Disable stencil test
    glDisable(GL_STENCIL_TEST)

    glEnable(GL_DEPTH_TEST)
    # enable writing to the color buffer
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)

    glDepthMask(GL_TRUE)


def render_object():
    # ***** Set Uniforms *****
    glUseProgram(shaderProgram_obj.shader)   # being explicit even though the line below will call this function
    shaderProgram_obj["modelMatrix"] = model_mat
    shaderProgram_obj["viewMatrix"] = view_mat
    shaderProgram_obj["projectionMatrix"] = projection_mat

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, obj_tex_id)

    # ***** Draw *****
    glBindVertexArray(vao_obj)
    glDrawArrays(GL_TRIANGLES,0, obj.n_vertices)      # Draw the triangle


def render_stencil():
    # ***** Set Uniforms *****
    glUseProgram(shaderProgram_stencil.shader)   # being explicit even though the line below will call this function
    shaderProgram_stencil["modelMatrix"] = pyrr.matrix44.create_from_scale([1/obj_stencil.dia, 1/obj_stencil.dia, 1/obj_stencil.dia])
    shaderProgram_stencil["viewMatrix"] = pyrr.matrix44.create_identity()
    shaderProgram_stencil["projectionMatrix"] = pyrr.matrix44.create_identity()

    # ***** Draw *****
    glBindVertexArray(vao_stencil)
    glDrawArrays(GL_TRIANGLES,0, obj_stencil.n_vertices)      # Draw the triangle



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
# glClearStencil(0)
# glClearDepth(1.0)
glEnable(GL_DEPTH_TEST)


# Camera parameters
eye = (0,0,2)
target = (0,0,0)
up = (0,1,0)

fov = 45
aspect = width/height
near = 0.1
far = 10

view_mat = pyrr.matrix44.create_look_at(eye, target, up)
projection_mat = pyrr.matrix44.create_perspective_projection_matrix(fov, aspect, near, far)


# Write our shaders. We will write our vertex shader and fragment shader in a different file
shaderProgram_obj = shaderLoaderV3.ShaderProgram("shaders/obj/vert_obj.glsl", "shaders/obj/frag_obj.glsl")
shaderProgram_stencil = shaderLoaderV3.ShaderProgram("shaders/stencil/vert_stencil.glsl", "shaders/stencil/frag_stencil.glsl")



'''
# **************************************************************************************************************
# Setup vertices, VAO, VBO, and vertex attributes for the object
# **************************************************************************************************************
'''
obj = ObjLoader("objects/rayman/raymanModel.obj")

# *********** Lets define model matrix ***********
translation_mat = pyrr.matrix44.create_from_translation(-obj.center)
scaling_mat = pyrr.matrix44.create_from_scale([2 / obj.dia, 2 / obj.dia, 2 / obj.dia])
model_mat = pyrr.matrix44.multiply(translation_mat, scaling_mat)

# VAO and VBO
vao_obj = glGenVertexArrays(1)
glBindVertexArray(vao_obj)
vbo_obj = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_obj)
glBufferData(GL_ARRAY_BUFFER, obj.vertices.nbytes, obj.vertices, GL_STATIC_DRAW)

position_loc = 0
glBindAttribLocation(shaderProgram_obj.shader, position_loc, "position")
glVertexAttribPointer(position_loc, obj.size_position, GL_FLOAT, GL_FALSE, obj.stride, ctypes.c_void_p(obj.offset_position))
glEnableVertexAttribArray(position_loc)

tex_coord_loc = 1
glBindAttribLocation(shaderProgram_obj.shader, tex_coord_loc, "uv")
glVertexAttribPointer(tex_coord_loc, obj.size_texture, GL_FLOAT, GL_FALSE, obj.stride, ctypes.c_void_p(obj.offset_texture))
glEnableVertexAttribArray(tex_coord_loc)

normal_loc = 2
glBindAttribLocation(shaderProgram_obj.shader, normal_loc, "normal")
glVertexAttribPointer(normal_loc, obj.size_normal, GL_FLOAT, GL_FALSE, obj.stride, ctypes.c_void_p(obj.offset_normal))
glEnableVertexAttribArray(normal_loc)
# **************************************************************************************************************
# **************************************************************************************************************


'''
# **************************************************************************************************************
# Set up vertices, VAO, VBO, and vertex attributes for stencil
# **************************************************************************************************************
'''
# Define the vertices of the stencil
obj_stencil = ObjLoader("objects/teapot.obj")

# Create VA0 and VBO
vao_stencil = glGenVertexArrays(1)
glBindVertexArray(vao_stencil)
vbo_stencil = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_stencil)
glBufferData(GL_ARRAY_BUFFER, obj_stencil.vertices.nbytes, obj_stencil.vertices, GL_STATIC_DRAW)

# Define the vertex attribute configurations
position_loc = 0
glBindAttribLocation(shaderProgram_stencil.shader, position_loc, "position")
glVertexAttribPointer(position_loc, obj_stencil.size_position, GL_FLOAT, GL_FALSE, obj_stencil.stride, ctypes.c_void_p(obj_stencil.offset_position))
glEnableVertexAttribArray(position_loc)

# **************************************************************************************************************
# **************************************************************************************************************



'''
# **************************************************************************************************************
# Load the 2D texture and attach the sampler variable "tex" in the object shader to texture unit 0.
# **************************************************************************************************************
'''

obj_tex_id = load_2d_texture("objects/rayman/raymanModel.png")

shaderProgram_obj["tex2D"] = 0
# **************************************************************************************************************
# **************************************************************************************************************




gui = SimpleGUI("Stencil")

# Create a slider for the rotation angle around the Z axis
camera_rotY_slider = gui.add_slider("camera Y angle", -180, 180, 0, resolution=1)
camera_rotX_slider = gui.add_slider("camera X angle", -90, 90, 0, resolution=1)
fov_slider = gui.add_slider("fov", 25, 120, 45, resolution=1)

render_option_radio = gui.add_radio_buttons("Choose render option",
                                          options_dict={"Show stencil pattern": "stencil",
                                                        "Show textured object": "object",
                                                        "Draw object over the stencil": "objOverStencil"},
                                          initial_option="Draw object over the stencil")



# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    rotateY_mat = pyrr.matrix44.create_from_y_rotation(np.deg2rad(camera_rotY_slider.get_value()))
    rotateX_mat = pyrr.matrix44.create_from_x_rotation(np.deg2rad(camera_rotX_slider.get_value()))
    rotation_mat = pyrr.matrix44.multiply(rotateX_mat, rotateY_mat)
    rotated_eye = pyrr.matrix44.apply_to_vector(rotation_mat, eye)

    view_mat = pyrr.matrix44.create_look_at(rotated_eye, target, up)
    projection_mat = pyrr.matrix44.create_perspective_projection_matrix(fov_slider.get_value(),
                                                                        aspect, near,  far)


    if render_option_radio.get_value() == "stencil":
        render_stencil()
    elif render_option_radio.get_value() == "object":
        render_object()
    else:

        set_masking_parameters()
        render_stencil()
        set_stenciling_parameters()
        render_object()
        set_default_parameters()


    # Refresh the display to show what's been drawn
    pg.display.flip()




# Cleanup
glDeleteVertexArrays(1, [vao_obj, vao_stencil])
glDeleteBuffers(1, [vbo_obj, vbo_stencil])

glDeleteProgram(shaderProgram_obj.shader)
glDeleteProgram(shaderProgram_stencil.shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program