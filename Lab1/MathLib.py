import math

def TrasnlationMatrix(x,y,z):
    return [[1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]]
    
def ScaleMatrix(x,y,z):
    return [[x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]]

def rotacionX(angulo):
    cosA = math.cos(math.radians(angulo))
    sinA = math.sin(math.radians(angulo))
    return [[1, 0, 0, 0],
            [0, cosA, -sinA, 0],
            [0, sinA, cosA, 0],
            [0, 0, 0, 1]]

def rotacionY(angulo):
    cosA = math.cos(math.radians(angulo))
    sinA = math.sin(math.radians(angulo))
    return [[cosA, 0, sinA, 0],
            [0, 1, 0, 0],
            [-sinA, 0, cosA, 0],
            [0, 0, 0, 1]]

def rotacionZ(angulo):
    cosA = math.cos(math.radians(angulo))
    sinA = math.sin(math.radians(angulo))
    return [[cosA, -sinA, 0, 0],
            [sinA, cosA, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]

def multiplicarMatrices(A, B):
    resultado = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

    for i in range(4):
        for j in range(4):
            resultado[i][j] = A[i][0] * B[0][j] + A[i][1] * B[1][j] + A[i][2] * B[2][j] + A[i][3] * B[3][j]
    return resultado

def transformarVertice(v, m):
    x = v[0] * m[0][0] + v[1] * m[0][1] + v[2] * m[0][2] + v[3] * m[0][3]
    y = v[0] * m[1][0] + v[1] * m[1][1] + v[2] * m[1][2] + v[3] * m[1][3]
    z = v[0] * m[2][0] + v[1] * m[2][1] + v[2] * m[2][2] + v[3] * m[2][3]
    w = v[0] * m[3][0] + v[1] * m[3][1] + v[2] * m[3][2] + v[3] * m[3][3]
    return [x, y, z, w]


    


    
