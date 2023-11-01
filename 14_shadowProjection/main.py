import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoaderV3
from objLoaderV4 import ObjLoader
from utils import load_image
from guiV3 import SimpleGUI
import pyrr
import os

def upload_and_configure_attributes(object, shader):
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
    glBindAttribLocation(shader, position_loc, "position")
    glBindAttribLocation(shader, tex_coord_loc, "uv")
    glBindAttribLocation(shader, normal_loc, "normal")

    glVertexAttribPointer(position_loc, object.size_position, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_position))
    glVertexAttribPointer(tex_coord_loc, object.size_texture, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_texture))
    glVertexAttribPointer(normal_loc, object.size_normal, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_normal))

    glEnableVertexAttribArray(tex_coord_loc)
    glEnableVertexAttribArray(position_loc)
    glEnableVertexAttribArray(normal_loc)

    return vao, vbo, object.n_vertices


def load_cubemap_texture(filenames):
    # Generate a texture ID
    texture_id = glGenTextures(1)

    # Bind the texture as a cubemap
    glBindTexture(GL_TEXTURE_CUBE_MAP, texture_id)

    # Define texture parameters
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


    # Define the faces of the cubemap
    faces = [GL_TEXTURE_CUBE_MAP_POSITIVE_X, GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
             GL_TEXTURE_CUBE_MAP_POSITIVE_Y, GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
             GL_TEXTURE_CUBE_MAP_POSITIVE_Z, GL_TEXTURE_CUBE_MAP_NEGATIVE_Z]

    # Load and bind images to the corresponding faces
    for i in range(6):
        img_data, img_w, img_h = load_image(filenames[i], format="RGB", flip=False)
        glTexImage2D(faces[i], 0, GL_RGB, img_w, img_h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Generate mipmaps
    glGenerateMipmap(GL_TEXTURE_CUBE_MAP)

    # Unbind the texture
    glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

    return texture_id



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
    shaderProgram_obj["modelMatrix"] = model_mat_obj
    shaderProgram_obj["viewMatrix"] = view_mat
    shaderProgram_obj["projectionMatrix"] = projection_mat

    shaderProgram_obj["lightPos"] = rotated_lightPos

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, obj_tex_id)

    # ***** Draw *****
    glBindVertexArray(vao_obj)
    glDrawArrays(GL_TRIANGLES,0, obj.n_vertices)      # Draw the triangle


def render_shadow():
    # ***** Set Uniforms *****
    glUseProgram(shaderProgram_shadow.shader)   # being explicit even though the line below will call this function
    shaderProgram_shadow["modelMatrix"] = model_mat_obj
    shaderProgram_shadow["viewMatrix"] = view_mat
    shaderProgram_shadow["projectionMatrix"] = projection_mat

    shaderProgram_shadow["planeNormal"] = receiver_normal
    shaderProgram_shadow["lightPos"] = rotated_lightPos
    shaderProgram_shadow["pointOnPlane"] = receiver_center
    shaderProgram_shadow["shadowFlag"] = shadow_checkbox.get_value()

    # ***** Draw *****
    glBindVertexArray(vao_obj)
    glDrawArrays(GL_TRIANGLES,0, obj.n_vertices)      # Draw the triangle


def render_skybox():
    glDepthFunc(GL_LEQUAL)  # Change depth function so depth test passes when values are equal to depth buffer's content

    # ***** Set Uniforms *****
    glUseProgram(shaderProgram_skybox.shader)   # being explicit even though the line below will call this function
    shaderProgram_skybox["invViewProjectionMatrix"] = inverseViewProjection_mat

    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cubemap_id)

    # ***** Draw *****
    glBindVertexArray(vao_skybox)
    glDrawArrays(GL_TRIANGLES,
                 0,
                 obj_skybox.n_vertices)  # Draw the triangle

    glDepthFunc(GL_LESS)    # Set depth function back to default


def render_receiver():
    # ***** Set Uniforms *****
    glUseProgram(shaderProgram_receiver.shader)   # being explicit even though the line below will call this function

    shaderProgram_receiver["modelMatrix"] = model_mat_receiver
    shaderProgram_receiver["viewMatrix"] = view_mat
    shaderProgram_receiver["projectionMatrix"] = projection_mat

    shaderProgram_receiver["lightPos"] = rotated_lightPos

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, receiver_tex_id)

    # ***** Draw *****
    glBindVertexArray(vao_receiver)
    glDrawArrays(GL_TRIANGLES, 0, obj_receiver.n_vertices)   # Draw the triangle


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
glClearStencil(0)
glEnable(GL_DEPTH_TEST)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


# Write our shaders. We will write our vertex shader and fragment shader in a different file
shaderProgram_obj = shaderLoaderV3.ShaderProgram("shaders/obj/vert_obj.glsl", "shaders/obj/frag_obj.glsl")
shaderProgram_skybox = shaderLoaderV3.ShaderProgram("shaders/skybox/vert_skybox.glsl", "shaders/skybox/frag_skybox.glsl")
shaderProgram_receiver = shaderProgram_obj
shaderProgram_shadow = shaderLoaderV3.ShaderProgram("shaders/shadow/vert_shadow.glsl","shaders/shadow/frag_shadow.glsl")


'''
# **************************************************************************************************************
# Load our objects and configure their attributes
# **************************************************************************************************************
'''
obj = ObjLoader("objects/rayman/raymanModel.obj")
vao_obj, vbo_obj, n_vertices_obj = upload_and_configure_attributes(obj, shaderProgram_obj.shader)

obj_receiver = ObjLoader("objects/square.obj")
vao_receiver, vbo_receiver, n_vertices_receiver = upload_and_configure_attributes(obj_receiver, shaderProgram_receiver.shader)

obj_skybox = ObjLoader("objects/square.obj")
vao_skybox, vbo_skybox, n_vertices_skybox = upload_and_configure_attributes(obj_skybox, shaderProgram_skybox.shader)

# **************************************************************************************************************
# **************************************************************************************************************


'''
# **************************************************************************************************************
# Define camera attributes
# **************************************************************************************************************
'''
eye = (0,0,4)
target = (0,0,0)
up = (0,1,0)

fov = 45
aspect = width/height
near = 0.1
far = 100

lightPos = [0, 2, 2]
# **************************************************************************************************************
# **************************************************************************************************************



'''
# **************************************************************************************************************
# Configure model matrices
# **************************************************************************************************************
'''
translation_mat = pyrr.matrix44.create_from_translation(-obj.center)
scaling_mat = pyrr.matrix44.create_from_scale([2 / obj.dia, 2 / obj.dia, 2 / obj.dia])
model_mat_obj = pyrr.matrix44.multiply(translation_mat, scaling_mat)

model_mat_receiver = pyrr.matrix44.create_from_translation([0, 0, -1])
receiver_center = pyrr.matrix44.apply_to_vector(model_mat_receiver, obj_receiver.center)

transpose_inverse_model_mat_receiver = pyrr.matrix44.inverse(model_mat_receiver).T
receiver_normal = pyrr.matrix44.apply_to_vector(transpose_inverse_model_mat_receiver, obj_receiver.vn[0])

# **************************************************************************************************************
# **************************************************************************************************************


'''
# **************************************************************************************************************
# Load the 2D texture and attach the sampler variable "tex" in the object shader to texture unit 0.
# **************************************************************************************************************
'''
obj_tex_id = load_2d_texture("objects/rayman/raymanModel.png")
receiver_tex_id = load_2d_texture("images/img.png")

shaderProgram_obj["tex2D"] = 0   # Okay this might be confusing. Here 0 indicates texture unit 0. Note that "tex" is a sampler variable in the fragment shader. It is not an integer.
# **************************************************************************************************************
# **************************************************************************************************************



'''
# **************************************************************************************************************
# Load the cubemap texture and attach the sampler variable "cubeMapTex" in both shaders to texture unit 0.
# **************************************************************************************************************
'''
dir = "images/skybox"
cubemap_images = ["right.png", "left.png", "top.png", "bottom.png", "front.png", "back.png"]
cubemap_images = [os.path.join(dir, img) for img in cubemap_images]
cubemap_id = load_cubemap_texture(cubemap_images)

shaderProgram_skybox["cubeMapTex"] = 1

# **************************************************************************************************************
# **************************************************************************************************************



'''
# **************************************************************************************************************
# Setup gui
# **************************************************************************************************************
'''
gui = SimpleGUI("Skybox")

# Create a slider for the rotation angle around the Z axis
light_rotY_slider = gui.add_slider("light Y angle", -89, 89, 0, resolution=1)

camera_rotY_slider = gui.add_slider("camera Y angle", -180, 180, 0, resolution=1)
camera_rotX_slider = gui.add_slider("camera X angle", -90, 90, 0, resolution=1)
fov_slider = gui.add_slider("fov", 25, 120, 45, resolution=1)

texture_type_radio = gui.add_radio_buttons("Texture type:",
                      options_dict={"Environment mapping": 0, "2D texture": 1, "Mix": 2},
                      initial_option="Environment mapping")

skybox_checkbox = gui.add_checkbox("Render skybox", True)
receiver_checkbox = gui.add_checkbox("Render receiver", True)
shadow_checkbox = gui.add_checkbox("Render Shadow", True)
stencil_checkbox = gui.add_checkbox("Use Stencil", True)

# **************************************************************************************************************
# **************************************************************************************************************



# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    cam_rotY_mat = pyrr.matrix44.create_from_y_rotation(np.deg2rad(camera_rotY_slider.get_value()))
    cam_rotX_mat = pyrr.matrix44.create_from_x_rotation(np.deg2rad(camera_rotX_slider.get_value()))
    cam_rot_mat = pyrr.matrix44.multiply(cam_rotX_mat, cam_rotY_mat)
    rotated_eye = pyrr.matrix44.apply_to_vector(cam_rot_mat, eye)

    view_mat = pyrr.matrix44.create_look_at(rotated_eye, target, up)
    projection_mat = pyrr.matrix44.create_perspective_projection_matrix(fov_slider.get_value(), aspect, near,  far)

    # compute inverse of view projection for skybox (after removing the translation
    view_mat_without_translation = view_mat.copy()
    view_mat_without_translation[3][:3] = [0,0,0]
    inverseViewProjection_mat = pyrr.matrix44.inverse(pyrr.matrix44.multiply(view_mat_without_translation,projection_mat))

    # rotate the light around the Y axis
    light_rotY_mat = pyrr.matrix44.create_from_y_rotation(np.deg2rad(light_rotY_slider.get_value()))
    rotated_lightPos = pyrr.matrix44.apply_to_vector(light_rotY_mat, lightPos)


    # ******************* Draw the receiver ************************
    if receiver_checkbox.get_value():
        render_receiver()


    # ******************* Draw the shadow ************************
    if shadow_checkbox.get_value():
        if stencil_checkbox.get_value():
            set_masking_parameters()
            render_receiver()
            set_stenciling_parameters()
            render_shadow()
        else:
            render_shadow()

    # Set the default parameters before drawing anything else
    set_default_parameters()


    # ******************* Draw the object ************************
    render_object()

    # ******************* Draw the skybox ************************
    if skybox_checkbox.get_value():
        render_skybox()



    # Refresh the display to show what's been drawn
    pg.display.flip()






# Cleanup
glDeleteVertexArrays(1, [vao_obj, vao_skybox, vao_receiver])
glDeleteBuffers(1, [vbo_obj, vbo_skybox, vao_receiver])

glDeleteProgram(shaderProgram_obj.shader)
glDeleteProgram(shaderProgram_skybox.shader)
# glDeleteProgram(shaderProgram_receiver.shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program