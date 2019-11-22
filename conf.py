
import graphics
import json

# Carga de la escena desde un archivo de configuración. 
# El archivo debe indicar los objetos a cargar, con sus texturas asociadas y sus transformaciones correspondientes. 
# También debe indicar las diferentes luces y sus parámetros de configuración.

class JsonObjs(object):
    def __init__(self):
        self.id = 0
        self.name = ""
        self.path = ""
        self.texture = ""

class Light(object):
    def __init__(self):
        self.material = ""
        self.vector = []

class InputFile(object):
    def __init__(self,filename):
        self.objects = []
        self.lights = []

        try:
            f = open(filename)
            with f as json_file:
                data = json.load(json_file)
                for p in data['objects']:
                    objFromJSON = JsonObjs()
                    objFromJSON.id = p['id']
                    objFromJSON.name = p['name']
                    objFromJSON.name = p['name']
                    objFromJSON.path = p['path']
                    objFromJSON.texture = p['texture']
                    self.objects.append(objFromJSON)
                for l in data['lights']:
                    light = Light()
                    light.material = l['material']
                    light.vector = l['vector']
                    self.lights.append(light)

            f.close()
        except IOError:
            print("Could not open the .obj file...")
        