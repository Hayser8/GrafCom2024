from MathLib import transformarVertice
def vertexShader(vertex, **kwargs):
    # se lleva a cabo por cada vertice 

    modelMatrix = kwargs["modelMatrix"]

    vt = [vertex[0], vertex[1], vertex[2], 1]

    vt = transformarVertice(vt, modelMatrix)

    vt = [vt[0] / vt[3], vt[1] / vt[3] , vt[2] / vt[3]]

    return vt