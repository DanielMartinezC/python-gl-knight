import pygame
import re
from sys import platform as _platform
from OpenGL.GL import *

def load_texture(filename):
    """ This fuctions will return the id for the texture"""
    textureSurface = pygame.image.load(filename)
    # Flip only for mac os
    if _platform == "darwin":
        textureSurface = pygame.transform.flip(textureSurface, False, True)
    textureData = pygame.image.tostring(textureSurface,"RGBA",1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,ID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_REPEAT)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    return ID

class ObjLoader(object):
    def __init__(self,filename):
        self.vertices = []
        self.normals = []
        self.textures = []
        self.faces = []
        self.quad_faces = []
        self.polygon_faces = []
        #-----------------------
        try:

            f = open(filename)
            n = 1
            for line in f:
                if line[:2] == "v ":
                    index1 = line.find(" ") +1 #first number index;
                    index2 = line.find(" ",index1+1)  # second number index;
                    index3 = line.find(" ",index2+1) # third number index;
                    
                    vertex = (float(line[index1:index2]),float(line[index2:index3]),float(line[index3:-1]))
                    self.vertices.append(vertex)
                    
                elif line[:2] == "vn":
                    index1 = line.find(" ") +1 #first number index;
                    index2 = line.find(" ",index1+1)  # second number index;
                    index3 = line.find(" ",index2+1) # third number index;
                    
                    normal = (float(line[index1:index2]),float(line[index2:index3]),float(line[index3:-1]))
                    self.normals.append(normal)
                
                elif line[:2] == "vt":
                    index1 = line.find(" ")+1 #first number index;
                    index2 = line.find(" ",index1+1)  # second number index;
                    
                    texture = (float(line[index1:index2]), float(line[index2:-1]))
                    self.textures.append(texture)
                    
                elif line[0] == "f":
                    #---------------------------------------------------
                    i = line.find(" ")+1
                    face  = []
                    for item in range(line.count(" ")):
                        if line.find(" ",i) == -1:
                            face.append(line[i:-1])
                            break
                        face.append(line[i:line.find(" ",i)])
                        i = line.find(" ",i) +1
                    #---------------------------------------------------
                    self.faces.append(tuple(face))
                    # First one is the first that is currently using: faces. 
                    if line.count("/") == 3:
                        self.faces.append(tuple(face))
                    elif line.count("/") == 4:
                        self.quad_faces.append(tuple(face))
                    else:
                        self.polygon_faces.append(tuple(face))

            f.close()
        except IOError:
            print("Could not open the .obj file...")
            
    # To render obj without texture
    def render_scene(self):
        glBegin(GL_TRIANGLES)
        for face in (self.faces):
            for i,f in enumerate(face):

                fValues = f.split("/")

                glNormal3fv(self.normals[int(fValues[1])-1])
                
                glVertex3fv(self.vertices[int(fValues[0])-1])

        glEnd()
        
    def ground_render_texture(self,textureID,texcoord):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,textureID)
        
        glBegin(GL_QUADS)
        for face in self.quad_faces:
            n = face[0]
            normal = self.normals[int(n[n.find("/")+1:])-1] 
            glNormal3fv(normal)
            for i,f in enumerate(face):
                glTexCoord2fv(texcoord[i])
                glVertex3fv(self.vertices[int(f[:f.find("/")])-1])
        glEnd()
    
        glDisable(GL_TEXTURE_2D)
    
    # To render obj with texture
    def render_texture(self,textureID):

        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        glBindTexture(GL_TEXTURE_2D,textureID)
        
        glBegin(GL_TRIANGLES)
        for face in (self.faces):
            for i,f in enumerate(face):

                fValues = f.split("/")

                glNormal3fv(self.normals[int(fValues[1])-1])
                
                glTexCoord2fv(self.textures[int(fValues[2])-1])
                
                glVertex3fv(self.vertices[int(fValues[0])-1])

        glEnd()
        
        glDisable(GL_TEXTURE_2D)