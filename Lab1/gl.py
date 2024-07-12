import struct

def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    # 2 bytes
    return struct.pack("=h", w)

def dword(d):
    # 4 bytes
    return struct.pack("=l", d)

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()

    def glColor(self, r,g,b):
        r= min(1, max(0,r))
        g= min(1, max(0,g))
        b= min(1, max(0,b))
        
        self.currColor= [r,g,b]

    def glClearColor(self, r,g,b):
        r= min(1, max(0,r))
        g= min(1, max(0,g))
        b= min(1, max(0,b))
        
        self.clearColor = [r,g,b]
    
    def glClear(self):
        color = [int(i*255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                            for x in range(self.width)]
        

    def glPoint(self, x, y, color=None):
        if(0<=x<self.width) and (0<=y<self.height):
            color = [int(i*255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color

    def glLine(self,v0,v1,color=None):

        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0)
            return 
    
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx 

        if steep: 
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.75
        m = dy / dx
        y = y0


        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)

            offset += m
            
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1

    def glFillPolygon(self, points, color=None):
        color = color or self.currColor
        if not points:
            return

        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        edges = []

        
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            if p1[1] > p2[1]:
                p1, p2 = p2, p1
            if p1[1] != p2[1]:  
                slope = (p2[0] - p1[0]) / (p2[1] - p1[1])
                edges.append([p1[1], p2[1], p1[0], slope])

        edges = sorted(edges, key=lambda e: e[0])  

        
        active_edges = []
        current_y = min_y
        while current_y <= max_y:
            
            while edges and edges[0][0] == current_y:
                active_edges.append(edges.pop(0))

            
            active_edges = [e for e in active_edges if e[1] > current_y]

            
            active_edges.sort(key=lambda x: x[2])

            
            for i in range(0, len(active_edges), 2):
                start_x = int(active_edges[i][2])
                end_x = int(active_edges[i + 1][2])
                self.glLine((start_x, current_y), (end_x, current_y), color)

            
            for e in active_edges:
                e[2] += e[3]  

            current_y += 1


    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14+40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]

                    color = bytes([color[2], color[1], color[0]])

                    file.write(color)








        


