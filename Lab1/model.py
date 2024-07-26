from obj import Obj
from MathLib import TrasnlationMatrix, ScaleMatrix, rotacionX, rotacionY, rotacionZ, multiplicarMatrices

class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename)

        self.vertices = objFile.vertices
        self.faces= objFile.faces

        self.translate = [0,0,0]
        self.rotate = [0,0,0]
        self.scale = [1,1,1]

    def GetModelMatrix(self):
        translateMat = TrasnlationMatrix(self.translate[0], self.translate[1], self.translate[2])

        rotatexMat = rotacionX(self.rotate[0])
        rotateyMat = rotacionY(self.rotate[1])
        rotatezMat = rotacionZ(self.rotate[2])

        rotatesemifinal = multiplicarMatrices(rotatexMat, rotateyMat)
        rotatefinal = multiplicarMatrices(rotatesemifinal, rotatezMat)

        scaleMat = ScaleMatrix(self.scale[0], self.scale[1], self.scale[2])

        # Primero escala, luego rotación, luego traslación
        ModeloObjeto = multiplicarMatrices(scaleMat, rotatefinal)
        ModeloObjetoFinal = multiplicarMatrices(translateMat, ModeloObjeto)

        return ModeloObjetoFinal
