try:
    import sympy
    collision = True
except ImportError:
    collision = False
    
from sympy import Poly
from sympy import abc
from sympy.solvers.inequalities import solve_rational_inequalities
from sympy import sets

    
#Creates an inequality give pts
#OBJECT MUST BE CONVEX
def createIneq(pts):
    sides = len(pts)
    
    side_slope_mask = []
    side_point_mask = []
    side_b_mask = []
    side_value_mask = []
    
    #Sypy Poly(shit)
    result = [(),()]
    # [0] less then [1] greater then
    
    #NOTE: This gives everything needed for point slope form
    for i in range(0, len(pts)):
        if i != len(pts)-1:
            i2 = i+1
        else:
            i2 = 0
            
        x = [pts[i][0], pts[i2][0]]
        y = [pts[i][1], pts[i2][1]]
        
        try:
            slope = ((y[0]-y[1])/(x[0]-x[1]))
        except ZeroDivisionError :
            slope = 'Undef'
            
        #print('y: %s x: %s m: %s' %(y,x,slope))
        
        side_slope_mask.append(slope)
        side_point_mask.append([x[0], y[0]])
    
    #solves for B
    for i in range(0 , sides):
        m = side_slope_mask[i]
        if m != 'Undef':
            #y - y[1] = m(x - x[1])
            #y = mx + b
            current_point = side_point_mask[i]
            x = current_point[0]
            y = current_point[1]
            
            b = ((m*x*-1)+y)
        else:
            b = 0
            #turns slope back to one
            side_slope_mask[i] = 1
                
        side_b_mask.append(b)
    
    center = averagePoints(pts)
    
    for i in range(0, sides):
        #mx+b=y
        m = side_slope_mask[i]
        b = side_b_mask[i]
        x = center[0]
        y = center[1]
        #print('m: %s x: %s y: %s b: %s' %(m,x,y,b))
        right = y
        left = ((m*x)+b)
        #print('l: %s r: %s' %(left,right))
        if left < right:
            result[0] += (Poly(m*abc.x + b + abc.y, abc.x, abc.y))
            #print('left')
        elif right > left:
            result[1] += (Poly(m*abc.x + b + abc.y, abc.x, abc.y))
            #print('right')
        #print(result)
    return result

def getCollision(inequality1, inequality2):
    format = [[]]
    
    #print('inq: %s inq2: %s' %(inequality1[0],inequality2[0]))
    foo = inequality1[0]
    bar = inequality2[0]
    inequality1[0] += inequality2[0]
    greater = inequality1[1]+inequality2[1]
    
    less = (less, '<=')
    greater = (greater, '>=')
    
    format[0].append(less)
    format[0].append(greater)
    
    print(format)
    
    solutions = solve_rational_inequalities(format)
    
    if(solutions != sets.EmptySet()):
        return solutions
    else:
        return None
        
def averagePoints(pts):
    sumX = 0
    sumY = 0
    
    for pt in pts:
        sumX += pt[0]
        sumY += pt[1]
    
    return ((sumX/len(pts)),(sumY/len(pts)))        
        