import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    step_3d = 20
    edges = []
    polygons = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
    script = (commands,symbols)[0]
    for command in script:
        line = command[0]
        args = command[1:]
        print [line]+list(args)
        if line == 'push':
            stack.append([x[:] for x in stack[-1]])
        elif line == 'pop':
            stack.pop()
        elif line == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif line == 'rotate':
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif line == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif line == 'box':
            i = 0
            if not isinstance(args[0],float):
                i += 1
            add_box(polygons,
                    float(args[0+i]), float(args[1+i]), float(args[2+i]),
                    float(args[3+i]), float(args[4+i]), float(args[5+i]))
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []
        elif line == 'sphere':
            i = 0
            if not isinstance(args[0],float):
                i += 1
            add_sphere(polygons,
                       float(args[0+i]), float(args[1+i]), float(args[2+i]),
                       float(args[3+i]), step_3d)
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []
        elif line == 'torus':
            i = 0
            if not isinstance(args[0],float):
                i += 1
            add_torus(polygons,
                      float(args[0+i]), float(args[1+i]), float(args[2+i]),
                      float(args[3+i]), float(args[4+i]), step_3d)
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []
        elif line == 'line':
            i = 0
            if not isinstance(args[0],float):
                i += 1
            j = 0
            if not isinstance(args[3+i],float):
                j += 1
            add_edge( edges,
                      float(args[0+i]), float(args[1+i]), float(args[2+i]),
                      float(args[3+i+j]), float(args[4+i+j]), float(args[5+i+j]))
            matrix_mult( stack[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []
        elif line == 'save':
            save_extension(screen, args[0]+args[1])
        elif line == 'display':
            display(screen)
        
            
        
    
