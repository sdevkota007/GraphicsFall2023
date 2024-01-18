import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import shaderLoaderV3
from objLoaderV4 import ObjLoader
from utils import load_image
from guiV3 import SimpleGUI
import pyrr
import os


def upload_and_configure_attributes(object):
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

    glVertexAttribPointer(position_loc, object.size_position, GL_FLOAT, GL_FALSE, object.stride,
                          ctypes.c_void_p(object.offset_position))
    glVertexAttribPointer(tex_coord_loc, object.size_texture, GL_FLOAT, GL_FALSE, object.stride,
                          ctypes.c_void_p(object.offset_texture))
    glVertexAttribPointer(normal_loc, object.size_normal, GL_FLOAT, GL_FALSE, object.stride,
                          ctypes.c_void_p(object.offset_normal))

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



def render_object(object_translation_vec):
    # ***** Set Uniforms *****
    glUseProgram(shaderProgram_obj.shader)  # being explicit even though the line below will call this function

    object_translation_mat = pyrr.matrix44.create_from_translation(object_translation_vec)
    model_mat_obj = pyrr.matrix44.multiply(translation_mat, object_translation_mat)

    # Set the model, view and projection matrices
    shaderProgram_obj["modelMatrix"] = model_mat_obj
    shaderProgram_obj["viewMatrix"] = view_mat
    shaderProgram_obj["projectionMatrix"] = projection_mat

    # Activate texture unit 0 and bind the texture to it
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, obj_tex_id)

    # ***** Draw *****
    glBindVertexArray(vao_obj)
    glDrawArrays(GL_TRIANGLES, 0, obj.n_vertices)  # Draw the triangle


def render_skybox():
    glDepthFunc(GL_LEQUAL)  # Change depth function so depth test passes when values are equal to depth buffer's content

    # ***** Set Uniforms *****
    glUseProgram(shaderProgram_skybox.shader)  # being explicit even though the line below will call this function
    shaderProgram_skybox["invViewProjectionMatrix"] = inverseViewProjection_mat

    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cubemap_id)

    # ***** Draw *****
    glBindVertexArray(vao_skybox)
    glDrawArrays(GL_TRIANGLES,
                 0,
                 obj_skybox.n_vertices)  # Draw the triangle

    glDepthFunc(GL_LESS)  # Set depth function back to default



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
clock = pg.time.Clock()

# Set the background color (clear color)
# glClearColor takes 4 arguments: red, green, blue, alpha. Each argument is a float between 0 and 1.
glClearColor(0.3, 0.4, 0.5, 1.0)
glClearStencil(0)
glEnable(GL_DEPTH_TEST)

# Write our shaders. We will write our vertex shader and fragment shader in a different file
shaderProgram_obj = shaderLoaderV3.ShaderProgram("shaders/obj/vert_obj.glsl", "shaders/obj/frag_obj.glsl")
shaderProgram_skybox = shaderLoaderV3.ShaderProgram("shaders/skybox/vert_skybox.glsl",
                                                    "shaders/skybox/frag_skybox.glsl")

'''
# **************************************************************************************************************
# Load our objects and configure their attributes
# **************************************************************************************************************
'''
obj = ObjLoader("objects/rayman/raymanModel.obj")
vao_obj, vbo_obj, n_vertices_obj = upload_and_configure_attributes(obj)

obj_skybox = ObjLoader("objects/square.obj")
vao_skybox, vbo_skybox, n_vertices_skybox = upload_and_configure_attributes(obj_skybox)

# **************************************************************************************************************
# **************************************************************************************************************


'''
# **************************************************************************************************************
# Define camera attributes
# **************************************************************************************************************
'''
eye = (0, 0, 4)
target = (0, 0, 0)
up = (0, 1, 0)

fov = 45
aspect = width / height
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

# **************************************************************************************************************
# **************************************************************************************************************


'''
# **************************************************************************************************************
# Load the 2D texture and attach the sampler variable "tex" in the object shader to texture unit 0.
# **************************************************************************************************************
'''
obj_tex_id = load_2d_texture("objects/rayman/raymanModel.png")
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

# **************************************************************************************************************
# **************************************************************************************************************


'''
# **************************************************************************************************************
# Setup gui
# **************************************************************************************************************
'''
gui = SimpleGUI("Skybox")

camera_rotY_slider = gui.add_slider("camera Y angle", -180, 180, 0, resolution=1)
camera_rotX_slider = gui.add_slider("camera X angle", -90, 90, 0, resolution=1)
fov_slider = gui.add_slider("fov", 25, 120, 45, resolution=1)

skybox_checkbox = gui.add_checkbox("Render skybox", True)

# **************************************************************************************************************
# **************************************************************************************************************


# Run a loop to keep the program running
object_translation_vec = np.array([0.0, 0.0, 0.0], dtype=np.float32)
move_speed = 0.1
draw = True
while draw:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False
        if event.type == pg.KEYDOWN:
            print(pg.key.name(event.key))

    keys = pg.key.get_pressed()

    # Handle key events for object movement
    if keys[K_LEFT]:
        object_translation_vec[0] -= move_speed
    if keys[K_RIGHT]:
        object_translation_vec[0] += move_speed
    if keys[K_UP]:
        object_translation_vec[1] += move_speed
    if keys[K_DOWN]:
        object_translation_vec[1] -= move_speed



    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    # # Matrices for camera
    cam_rotY_mat = pyrr.matrix44.create_from_y_rotation(np.deg2rad(camera_rotY_slider.get_value()))
    cam_rotX_mat = pyrr.matrix44.create_from_x_rotation(np.deg2rad(camera_rotX_slider.get_value()))
    cam_rot_mat = pyrr.matrix44.multiply(cam_rotX_mat, cam_rotY_mat)
    rotated_eye = pyrr.matrix44.apply_to_vector(cam_rot_mat, eye)

    view_mat = pyrr.matrix44.create_look_at(rotated_eye, target, up)
    projection_mat = pyrr.matrix44.create_perspective_projection_matrix(fov_slider.get_value(), aspect, near, far)


    # compute inverse of view projection for skybox (after removing the translation
    view_mat_without_translation = view_mat.copy()
    view_mat_without_translation[3][:3] = [0,0,0]
    inverseViewProjection_mat = pyrr.matrix44.inverse(pyrr.matrix44.multiply(view_mat_without_translation,projection_mat))


    # ******************* Draw the object ************************
    render_object(object_translation_vec)

    # ******************* Draw the skybox ************************
    render_skybox()

    # Refresh the display to show what's been drawn
    pg.display.flip()

# Cleanup
glDeleteVertexArrays(2, [vao_obj, vao_skybox])
glDeleteBuffers(2, [vbo_obj, vbo_skybox])

glDeleteProgram(shaderProgram_obj.shader)
glDeleteProgram(shaderProgram_skybox.shader)

pg.quit()  # Close the graphics window
quit()  # Exit the program