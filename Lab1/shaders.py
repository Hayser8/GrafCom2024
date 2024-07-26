from MathLib import transformarVertice,multiplicarMatrices
def vertexShader(vertex, **kwargs):
    # se lleva a cabo por cada vertice 

    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    vt = [vertex[0], vertex[1], vertex[2], 1]

    vtsss = multiplicarMatrices(viewportMatrix, projectionMatrix)
    vtss = multiplicarMatrices(vtsss, viewMatrix)
    vts = multiplicarMatrices(vtss, modelMatrix)



    vt = transformarVertice(vt, vts)

    vt = [vt[0] / vt[3], vt[1] / vt[3] , vt[2] / vt[3]]

    return vt