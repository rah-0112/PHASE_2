dump = False
import sympy as sp

#---------------------------------------------

# def findModularInverse(a, mod):
			
# 	while(a < 0):
# 		a = a + mod

# 	a = a % mod
	
# 	x1 = 1; x2 = 0; x3 = mod
# 	y1 = 0; y2 = 1; y3 = a

# 	print(int(x3/y3))
	
# 	q = int(x3 / y3)
# 	t1 = x1 - q*y1
# 	t2 = x2 - q*y2
# 	t3 = x3 - (q*y3)
	
# 	if dump == True:
# 		print("q\tx1\tx2\tx3\ty1\ty2\ty3\tt1\tt2\tt3")
# 		print("----------------------------------------------------------------------------")
# 		print(q,"\t",x1,"\t",x2,"\t",x3,"\t",y1,"\t",y2,"\t",y3,"\t",t1,"\t",t2,"\t",t3)
	
# 	while(y3 != 1):
# 		x1 = y1; x2 = y2; x3 = y3
		
# 		y1 = t1; y2 = t2; y3 = t3
		
# 		q = int(x3 / y3)
# 		t1 = x1 - q*y1
# 		t2 = x2 - q*y2
# 		t3 = x3 - (q*y3)
		
# 		if dump == True:
# 			print(q,"\t",x1,"\t",x2,"\t",x3,"\t",y1,"\t",y2,"\t",y3,"\t",t1,"\t",t2,"\t",t3)
# 			print("----------------------------------------------------------------------------")
# 			print("")
	
# 	while(y2 < 0):
# 		y2 = y2 + mod
	
# 	return y2

# def pointAddition(x1, y1, x2, y2, a, b, mod):
	
# 	if x1 == x2 and y1 == y2:
# 		#doubling
# 		beta = (3*x1*x1 + a) * (findModularInverse(2*y1, mod))
	
# 	else:
# 		#point addition
# 		beta = (y2 - y1)*(findModularInverse((x2 - x1), mod))
	
# 	x3 = beta*beta - x1 - x2
# 	y3 = beta*(x1 - x3) - y1
	
# 	x3 = x3 % mod
# 	y3 = y3 % mod
	
# 	while(x3 < 0):
# 		x3 = x3 + mod
	
# 	while(y3 < 0):
# 		y3 = y3 + mod
	
# 	return x3, y3
def findModularInverse(a, m):
    """
    Compute the modular inverse of 'a' modulo 'm' using the Extended Euclidean Algorithm.
    
    Parameters:
        a (int): The number whose modular inverse is to be found.
        m (int): The modulus.
    
    Returns:
        int: The modular inverse of 'a' modulo 'm'.
    
    Raises:
        ValueError: If 'a' is not invertible modulo 'm' (i.e., gcd(a, m) != 1).
    """
    t, t_prev = 0, 1
    r, r_prev = m, a
    
    while r_prev != 0:
        quotient = r // r_prev
        t, t_prev = t_prev, t - quotient * t_prev
        r, r_prev = r_prev, r - quotient * r_prev
    
    if r > 1:
        raise ValueError("The number 'a' is not invertible modulo 'm'")
    if t < 0:
        t += m
    
    return t % m

def pointAddition(x1, y1, x2, y2, a, d, mod):
    x3 = ((x1 * y2 + y1 * x2) * findModularInverse(1 + d * x1 * x2 * y1 * y2, mod)) % mod
    
    y3 = ((y1 * y2 - a * x1 * x2) * findModularInverse(1 - d * x1 * x2 * y1 * y2, mod)) % mod
    
    return x3, y3


def applyDoubleAndAddMethod(x0, y0, k, a, b, mod):
	
	x_temp = x0
	y_temp = y0
	
	kAsBinary = bin(k) #0b1111111001
	kAsBinary = kAsBinary[2:len(kAsBinary)] #1111111001
	#print(kAsBinary)
	
	for i in range(1, len(kAsBinary)):
		currentBit = kAsBinary[i: i+1]
		#always apply doubling
		x_temp, y_temp = pointAddition(x_temp, y_temp, x_temp, y_temp, a, b, mod)
		
		if currentBit == '1':
			#add base point
			x_temp, y_temp = pointAddition(x_temp, y_temp, x0, y0, a, b, mod)
	
	return x_temp, y_temp

# Define the symbols
def returnImage():
    x, y = sp.symbols('x y')

    # Define the equation of the hyperelliptic curve
    curve_eq = y**2 - (x**5 - 4*x**4 - 11*x**3 + 3*x**2 + 10*x)

    # Define the x-coordinates of the points where you want to find intersections
    x_values = [1233, 10]

    # Define a list to store the intersection points
    intersection_points = []

    # Iterate over the x-values
    for x_val in x_values:
        # Compute the first derivative of the curve equation
        first_derivative = sp.diff(curve_eq, x)

        # Evaluate the first derivative at the current x-value to get the slope (m)
        slope = first_derivative.subs(x, x_val)

        # Define the y-coordinate of the point using the curve equation
        y_val = sp.sqrt(curve_eq.subs(x, x_val))

        # Define the equation of the tangent line in slope-intercept form
        tangent_line_eq = slope * (x - x_val) + y_val

        # Find the intersection points of the tangent line with the curve
        intersections = sp.solve(curve_eq - tangent_line_eq, y)

        # Append the intersection points to the list
        intersection_points.extend([(x_val, intersection.evalf()) for intersection in intersections])

    # Print the intersection points
    maxX = -1
    maxImageListener = -1
    print("Intersection points:")
    for point in intersection_points:
        x_val = point[0]
        y_val = point[1].evalf(subs={x: x_val})
        maxX = max(abs(int(x_val)), maxX)
        maxImageListener = max(abs(int(y_val)), maxImageListener)

    return maxX, maxImageListener