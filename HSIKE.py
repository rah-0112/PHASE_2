import random
import hashlib
import sympy as sp
import time

def returnImage(x_var1, x_var2, a, b, c):
    x, y = sp.symbols('x y')

    # Define the equation of the hyperelliptic curve
    # curve_eq = y**2 - (x**5 - 4*x**4 - 11*x**3 + 3*x**2 + 10*x) 108306943611133
    # curve_eq = y**2 - (x**5 - 3*x**4 - 11*x**3 + 4*x**2 + 12*x) 108306943611133
    # curve_eq = y**2 - (x**5 - 4*x**4 - 11*x**3 + 4*x**2 + 10*x) 108306943611133
    # curve_eq = y**2 - (x**5 - 6*x**4 - 11*x**3 + 6*x**2 + 6*x) 10830694361113356
    curve_eq = y**2 - (x**5 - 6*x**4 - 11*x**3 + 16*x**2 + 6*x) 
    # curve_eq = y**2 - (x**5 - 4*x**4 - 11*x**3 + 12*x**2 + 4*x) 108306943611133
    # curve_eq = y**2 - (x**5 - 4*x**4 - 11*x**3 + 12*x**2 + 18*x) 108306943611133
    # curve_eq = y**2 - (x**5 - 2*x**4 - 11*x**3 + 6*x**2 + 2*x) 1083069436783356
    # curve_eq = y**2 - (x**5 - 1*x**4 - 11*x**3 + 4*x**2 + 2*x) 108306943611133
    # curve_eq = y**2 - (x**5 - 8*x**4 - 11*x**3 + 4*x**2 + 2*x) 10830694361113356
    # curve_eq = y**2 - (x**5 - a*x**4 - 11*x**3 + b*x**2 + c*x)
    # Define the x-coordinates of the points where you want to find intersections
    
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Hyper Elliptic curve equation")
    print("y**2 - (x**5 - 6*x**4 - 11*x**3 + 16*x**2 + 6*x)")
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("View the graph in DESMOS")
    print("https://www.desmos.com/calculator/c46mh2fhe4")
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Or see the HEC grpah in image in hec.png")

    x_values = [x_var1, x_var2]

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
    # print("Intersection HEC Point in Curve - ")
    for point in intersection_points:
        # print(point)
        x_val = point[0]
        y_val = point[1].evalf(subs={x: x_val})
        maxX = max(abs(int(x_val)), maxX)
        maxImageListener = max(abs(int(y_val)), maxImageListener)
    # print(maxX, maxImageListener)
    return [maxX, maxImageListener]

def add_points(P, Q, a, d, p):
    # twisted edwards curve: (a*x^2 + y^2) mod p = (1 + d*x^2*y^2) mod p
    
    x1, y1 = P
    x2, y2 = Q
    
    x3 = ( ( (x1*y2 + y1*x2) % p) * pow(1 + d*x1*x2*y1*y2, -1, p) ) % p
    y3 = ( ( (y1*y2 - a*x1*x2) % p ) * pow(1 - d*x1*x2*y1*y2, -1, p) ) % p
    
    assert (a*x3*x3 + y3*y3) % p == (1 + d*x3*x3*y3*y3) % p
    
    return x3, y3

def apply_double_and_add_method(Q, k, a, d, p):
    """
    kQ = k x Q
    """
    addition_point = Q
    
    k_binary = bin(k)[2:] #1111111001
    
    for i in range(1, len(k_binary)):
        current_bit = k_binary[i:i+1]
        
        # always doubling
        addition_point = add_points(addition_point, addition_point, a, d, p)
        
        if current_bit == "1":
            addition_point = add_points(addition_point, Q, a, d, p)
    
    return addition_point

def text_to_int(text):
    encoded_text = text.encode("utf-8")
    hex_text = encoded_text.hex()
    return int(hex_text, 16)

def hashing(message_int):
    return int(hashlib.sha256(str(message_int).encode("utf-8")).hexdigest(), 16)

class HECCurveDSA(object):
    def __init__(self, a, b, c):
       self.a = a
       self.b = b
       self.c = c

    p = pow(2, 255) - 19
    a = -1

    d = -121665/121666
    d = (-121665 * pow(121666, -1, p)) % p

    # base point G
    u = 9
    # Gy = (u-1)/(u+1)
    Gy = ( (u-1) * pow(u+1, -1, p) ) % p
    Gx = 15112221349535400772501151409588531511454012693041857206046113283949847762202

    G = (Gx, Gy)
    GpointX = 1233
    sk = 0
    pk = 0

    message = text_to_int("No one knows the reason for all this, but it is probably quantum. - Pyramids, Terry Pratchett (1989)")

    def KeyGen(self):
      # generation
      private_key = random.getrandbits(256)

      self.sk = private_key
      # 108306943611133934620933874520787151991909626954932499000953049343871188807392
      public_key = returnImage(12333, 10830694361113356, self.a, self.b, self.c)

      pub_key = str(public_key[0]) + str(public_key[1])

      # print("Secret Key Size: ", len(str(private_key).encode('utf-8')))
      # print("Public Key Size: ", len(pub_key.encode('utf-8')))  

      return public_key, private_key

    def Encaps(self, sk, pk):
      # signing
      r = hashing(hashing(self.message) + self.message) % self.p

      R = apply_double_and_add_method(self.G, r, self.a, self.d, self.p)

      h = (R[0] + pk[0] + self.message) % self.p
      s = (r + h * sk)

      P1 = apply_double_and_add_method(self.G, s, self.a, self.d, self.p)

      return R, P1
    
    def Decaps(self, R, pk):
      # verify
      h = (R[0] + pk[0] + self.message) % self.p

      P2 = add_points(R, apply_double_and_add_method(pk, h, self.a, self.d, self.p), self.a, self.d, self.p)

      return P2

    def sign(self, pk, sk):
      r = hashing(hashing(self.message) + self.message) % self.p

      R = returnImage(self.GpointX, r, self.a, self.b, self.c)

      h = (R[0] + pk[0] + self.message) % self.p

      s = (r + h * sk)

      return R, s

    def verify(self, R, s, pk):
      h = (R[0] + pk[0] + self.message) % self.p

      r = s - h * self.sk

      Rnew = returnImage(self.GpointX, r, self.a, self.b, self.c)

      return R[0] == Rnew[0] and R[1] == Rnew[1]