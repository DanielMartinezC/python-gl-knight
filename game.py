import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import graphics
import conf
import os

class Ground(object):

    '''
    Func: - Init
    '''
    def __init__(self):
        self.ground_id = graphics.load_texture("images/ConcreteTriangles.png")
        self.ground = graphics.ObjLoader("plane.obj")

        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_zoom = 1.0
    
    '''
    Func: - GL Helpers
    '''
    def render_scene(self):

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.zoom_camera() 

        glTranslatef(0,-45,0)
        
        #Add ambient light:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[0.2,0.2,0.2,1.0])

        self.ground.ground_render_texture(self.ground_id,((0,0),(100,0),(100,100),(0,100)))

    def delete_texture(self):
        glDeleteTextures(self.ground_id)
    
    '''
    Func: - Update camera on mouse interaction
    '''
    def update(self):
        # Mouse action
        pos = pygame.mouse.get_pos()

        pressed = pygame.mouse.get_pressed()

        if not pressed[0]:
            if pos[1] < 5:
                self.zoom_in()
            elif pos[1] > 700:
                self.zoom_out()
        else:
            if pos[0] < 400:
                self.camera_x += 1.5
            else:
                self.camera_x -= 1.5

    '''
    MARK: - Zoom Helpers
    '''
    def zoom_in(self):
        # Zoom camera
        self.camera_zoom *= 1.2

    def zoom_out(self):
        # Zoom camera
        self.camera_zoom /= 1.2

    def zoom_camera(self):
        # Move to camera position
        glTranslatef(self.camera_x, self.camera_y, 0 )
        # Scale camera
        glScalef( self.camera_zoom, self.camera_zoom, 1 )
        # Move back from camera position
        glTranslatef( -self.camera_x, -self.camera_y, 0 )

class GenericObj(object):

    '''
    MARK: - Object properties
    '''
    left_key = False
    right_key = False
    up_key = False
    down_key = False
    q_key = False #Stand
    a_key = False #Attack
    c_key = False #Crouch Attack
    z_key = False #Crouch death
    p_key = False #Crouch pain
    s_key = False #Crouch stand
    x_key = False #Crouch walk
    f_key = False #Fallback death
    l_key = False #Fallback death slow
    k_key = False #Fallforward death
    i_key = False #Fallback
    t_key = False #Flip
    j_key = False #Jump
    one_key = False #Pain a
    two_key = False #Pain b
    three_key = False #Pain c
    r_key = False #Point
    t_key = False #Salute
    w_key = False #Wave
    
    action = "stand"
    angle = -85.0
    mouse_angle = 0.0
    current_position = 0

    '''
    Func: - Init
    '''
    def __init__(self, objs, soundChannel):
        #---Coordinates----[x,y,z]-----------------------------
        self.coordinates = [0,0,-70]
        self.pox_x = 0.0
        self.pos_y = 0.0
        self.objs = objs

        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_zoom = 1.0

        self.sound_channel = soundChannel

    '''
    Func: - Update object action based on pressed key or camera on mouse interaction
    '''
    def update(self, action = "stand", limit = "39"):
        if self.left_key:
            self.move_left()
        elif self.right_key:
            self.move_right()
        elif self.up_key:
            self.move_forward()
        elif self.down_key:
            self.move_back()
        elif self.a_key:
            self.do_action("attack", 7)
        elif self.q_key:
            self.do_action("stand", 39)
        elif self.c_key:
            self.do_action("crouch_attack", 7)
        elif self.z_key:
            self.do_action("crouch_death", 4)
        elif self.p_key:
            self.do_action("crouch_pain", 3)
        elif self.s_key:
            self.do_action("crouch_stand", 18)
        elif self.x_key:
            self.do_action("crouch_walk", 5)
        elif self.f_key:
            self.do_action("death_fallback", 5)
        elif self.t_key:
            self.do_action("flip", 11)
        elif self.j_key:
            self.do_action("jump", 5)
        else:
            self.stand()
            
        # Mouse action
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        if not pressed[0]:
            if pos[0] < 75:
                self.rotate(-5)
            elif pos[0] > 600:
                self.rotate(5)
            if pos[1] < 5:
                self.zoom_in()
            elif pos[1] > 700:
                self.zoom_out()
        else:
            if pos[0] < 400:
                self.camera_x += 1.5
            else:
                self.camera_x -= 1.5

    '''
    Func: - Reset pressed keys
    '''         
    def keyup(self):
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False
        self.q_key = False #Stand
        self.a_key = False #Attack
        self.c_key = False #Crouch Attack
        self.z_key = False #Crouch death
        self.p_key = False #Crouch pain
        self.s_key = False #Crouch stand
        self.x_key = False #Crouch walk
        self.f_key = False #Fallback death
        self.l_key = False #Fallback death slow
        self.k_key = False #Fallforward death
        self.i_key = False #Fallback
        self.t_key = False #Flip
        self.j_key = False #Jump
        self.one_key = False #Pain a
        self.two_key = False #Pain b
        self.three_key = False #Pain c
        self.r_key = False #Point
        self.t_key = False #Salute
        self.w_key = False #Wave
        self.sound_channel.stop()

    '''
    MARK: - Actions 
    '''
    def do_action(self, action, limit):
        if self.current_position < limit:
            self.current_position += 1
        else:
            self.current_position = 0
            if os.path.isfile('sounds/'+action+'.wav'):  
                sound1 = pygame.mixer.Sound('sounds/'+action+'.wav')
                self.sound_channel.play(sound1, loops = 0)
        self.action = action

    def stand(self):
        if self.current_position <= 38:
            self.current_position += 1
        else:
            self.current_position = 0
        self.action = "stand"

    def run(self):
        if self.current_position <= 4:
            self.current_position += 1
        else:
            self.current_position = 0
        sound1 = pygame.mixer.Sound("sounds/run.wav")
        self.sound_channel.play(sound1, loops = -1)
        self.action = "run"

    def move_right(self):
        self.coordinates[2] += 2.5 * math.cos(math.radians(self.angle))
        self.coordinates[0] -= 2.5 * math.sin(math.radians(self.angle))
        self.mouse_angle = 90.0
        self.run()
        
    def move_left(self):
        self.coordinates[2] -= 2.5 * math.cos(math.radians(self.angle))
        self.coordinates[0] += 2.5 * math.sin(math.radians(self.angle))
        self.mouse_angle = -90.0
        self.run()
            
    def move_forward(self):
        self.coordinates[0] += 2.5 * math.cos(math.radians(self.angle))
        self.coordinates[2] += 2.5 * math.sin(math.radians(self.angle))
        self.mouse_angle = -180.0
        self.run()
        
    def move_back(self):
        self.coordinates[0] -= 2.5 * math.cos(math.radians(self.angle))
        self.coordinates[2] -= 2.5 * math.sin(math.radians(self.angle))
        self.mouse_angle = 0.0
        self.run()
    
    '''
    Func: - Rotate and zoom 
    '''
    def rotate(self,n):
        if self.mouse_angle >= 360 or self.mouse_angle <= -360:
            self.mouse_angle = 0
        self.mouse_angle += n
    
    def zoom_in(self):
        # Zoom camera
        self.camera_zoom *= 1.2

    def zoom_out(self):
        # Zoom camera
        self.camera_zoom /= 1.2

    def zoom_camera(self):
        # Move to camera position
        glTranslatef(self.camera_x, self.camera_y, 0 )
        # Scale camera
        glScalef( self.camera_zoom, self.camera_zoom, 1 )
        # Move back from camera position
        glTranslatef( -self.camera_x, -self.camera_y, 0 )
    
    '''
    Func: - GL Helpers
    '''
    def delete_texture(self):
        for obj in self.objs:
            glDeleteTextures(obj.texture)

    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #Do camera config, before objects config
        self.zoom_camera()

        glTranslatef(self.coordinates[0],self.coordinates[1],self.coordinates[2])
        glRotatef(self.angle, 0, 1, 0)
        glRotatef(self.angle, 1, 0, 0)
        glRotatef(self.mouse_angle, 0, 0, 1)
        
        #Add ambient light:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[0.2,0.2,0.2,1.0])
        
        for obj in self.objs:
            textureID = graphics.load_texture(obj.texture)
            tempObj = graphics.ObjLoader(str(obj.path)+"/"+str(obj.name)+"_"+str(self.action)+"_"+str(self.current_position)+".obj")
            tempObj.render_texture(textureID)

def main():
    
    pygame.init()
    pygame.display.set_mode((900,900),pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.display.set_caption("Obligatorio Computación Gráfica")

    # initialize pygame.mixer
    pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12) 
    # init() channels refers to mono vs stereo, not playback Channel object

    channel1 = pygame.mixer.Channel(0) # main sound
    channel2 = pygame.mixer.Channel(1)

    # Play backtrack on channel 1
    sound1 = pygame.mixer.Sound("sounds/medieval-introduction.wav")
    channel1.play(sound1, loops = -1)

    # Read input file (objs and lights)
    input_file = conf.InputFile("inputfile.txt")
    
    # glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,0,0,1])
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [1,0,0,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 16)

    # Load lights from input file
    for light in input_file.lights:
        glLight(GL_LIGHT0, eval(light.material), light.vector)

    glEnable(GL_DEPTH_TEST)

    # Set antialiasing
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    # Set alpha blending
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    glViewport(0,0,900,900)
    glFrustum(-1,1,-1,1,1,1000)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Ground obj (harcoded obj and texture)
    ground = Ground()
    
    # Objs from input file, assigned channel2 for sounds
    objs = GenericObj(input_file.objects, channel2)

    done = False

    # Main Program Loop
    while not done:
        # Main event loop
        for event in pygame.event.get(): # User did something
            
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    objs.move_left()
                    objs.left_key = True
                elif event.key == pygame.K_RIGHT:
                    objs.move_right()
                    objs.right_key = True
                elif event.key == pygame.K_UP:
                    objs.move_forward()
                    objs.up_key = True
                elif event.key == pygame.K_DOWN:
                    objs.move_back()
                    objs.down_key = True
                elif event.key == pygame.K_a:
                    objs.a_key = True
                elif event.key == pygame.K_c:
                    objs.c_key = True
                elif event.key == pygame.K_q:
                    objs.q_key = True
                elif event.key == pygame.K_z:
                    objs.z_key = True
                elif event.key == pygame.K_p:
                    objs.p_key = True
                elif event.key == pygame.K_s:
                    objs.s_key = True
                elif event.key == pygame.K_x:
                    objs.x_key = True
                elif event.key == pygame.K_f:
                    objs.f_key = True
                elif event.key == pygame.K_t:
                    objs.t_key = True
                elif event.key == pygame.K_j:
                    objs.j_key = True

            if event.type == pygame.KEYUP:
                objs.keyup()
        
        objs.update()
        objs.render_scene()
        ground.update()
        ground.render_scene()

        pygame.display.flip()
    
    objs.delete_texture()
    ground.delete_texture()
    pygame.quit()

if __name__ == '__main__':
	main()