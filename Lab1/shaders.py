from MathLib import *
from texture import Texture
import math 

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


def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    # Sabiendo que las coordenadas de textura
    # están en la 4ta y 5ta posicion de cada
    # indice del vertice, los obtenemos y
    # guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    # Sabiendo que los valores de las normales 
    # están en la 6ta, 7ma y 8va posición 
    # de cada vértice, los obtenemos y guardamos

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1

    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # Se regresa el color
    return [r,g,b]

def flatShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [(nA[0] + nB[0] + nC[0]) / 3,
              (nA[1] + nB[1] + nC[1]) / 3,
              (nA[2] + nB[2] + nC[2]) / 3]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # intensity = normal DOT -dirlight
    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = (normal[0] * dirLight_neg[0] + 
                 normal[1] * dirLight_neg[1] + 
                 normal[2] * dirLight_neg[2])
    
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    # Se regresa el color
    return [r, g, b]

def toonShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # intensity = normal DOT -dirlight
    dirLight_neg = [-dirLight[0], -dirLight[1], -dirLight[2]]
    intensity = (normal[0] * dirLight_neg[0] + 
                 normal[1] * dirLight_neg[1] + 
                 normal[2] * dirLight_neg[2])
    
    intensity = max(0, intensity)
    
    if intensity < 0.33:
        intensity = 0.3
    elif intensity < 0.66:
        intensity = 0.6
    else:
        intensity = 1.0

    r *= intensity
    g *= intensity
    b *= intensity
    
    # Se regresa el color
    return [r, g, b]


def glowShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]
    modelMatrix = kwargs["modelMatrix"]
    camMatrix = kwargs["camMatrix"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    # GLOW
    yellowGlow = [1, 1, 0]
    
    camForward = [
        camMatrix[0][2],
        camMatrix[1][2],
        camMatrix[2][2]
    ]
    
    glowIntensity = 1 - (normal[0] * camForward[0] + normal[1] * camForward[1] + normal[2] * camForward[2])
    glowIntensity = min(1, max(0, glowIntensity))
    
    r = 0.2 
    g = 0.2
    b = 0.2

    r += yellowGlow[0] * glowIntensity
    g += yellowGlow[1] * glowIntensity
    b += yellowGlow[2] * glowIntensity

    # Se regresa el color
    return [min(1, r), min(1, g), min(1, b)]

def circularDistortionShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    # Calcular la posición interpolada en la textura
    vtP = [
        u * vtA[0] + v * vtB[0] + w * vtC[0],
        u * vtA[1] + v * vtB[1] + w * vtC[1]
    ]

    frequency = 20.0  # Aumentar la frecuencia para hacer las ondas más notorias
    amplitude = 0.2   # Aumentar la amplitud para que las distorsiones sean más fuertes

    # Generar un patrón circular usando las coordenadas u y v
    distance = math.sqrt(vtP[0]**2 + vtP[1]**2)
    wave = math.sin(frequency * distance)

    # Aplicar la distorsión en las coordenadas de textura
    distorted_u = vtP[0] + amplitude * wave
    distorted_v = vtP[1] + amplitude * wave

    # Mantener las coordenadas dentro del rango [0, 1]
    distorted_u = max(0, min(1, distorted_u))
    distorted_v = max(0, min(1, distorted_v))

    r, g, b = 1, 1, 1
    if texture:
        # Asegurarse de que siempre estamos usando la textura del objeto
        texColor = texture.getColor(distorted_u, distorted_v)
        if texColor:
            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]
        else:
            # Si no hay color válido, utilizar un fallback basado en la textura original
            texColor = texture.getColor(vtP[0], vtP[1])
            r, g, b = texColor[0], texColor[1], texColor[2]

    return [r, g, b]

def waveShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    # Calcular la posición interpolada en la textura
    vtP = [
        u * vtA[0] + v * vtB[0] + w * vtC[0],
        u * vtA[1] + v * vtB[1] + w * vtC[1]
    ]

    # Crear un patrón de ondas en el color
    wave_intensity = 0.5 * (math.sin(vtP[0] * 10 * math.pi) + 1)  # Rango de 0 a 1
    wave_color = [wave_intensity, wave_intensity, wave_intensity]

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        # Mezclar el color de la textura con el patrón de ondas
        finalColor = [texColor[i] * wave_color[i] for i in range(3)]
    else:
        finalColor = wave_color  # Si no hay textura, usar solo el patrón de ondas

    return finalColor


def smoothRainbowShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]

    # Generar un gradiente de arcoíris suave basado en la coordenada v
    r = (math.sin(v * math.pi) + 1) / 2  # Suave transición para rojo
    g = (math.sin((v + 0.33) * math.pi) + 1) / 2  # Desfase suave para verde
    b = (math.sin((v + 0.66) * math.pi) + 1) / 2  # Desfase suave para azul

    # Mantener la manipulación de color en la escala 0-1
    texColor = [r, g, b]

    return texColor


