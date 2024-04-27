import random
import hashlib

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

class TwistedEdwardCurve:
    # Ed25519, Curve25519
    p = pow(2, 255) - 19
    a = -1

    d = -121665/1216662
    d = (-121665 * pow(121666, -1, p)) % p

    # base point G
    u = 9
    # Gy = (u-1)/(u+1)
    Gy = ( (u-1) * pow(u+1, -1, p) ) % p
    Gx = 15112221349535400772501151409588531511454012693041857206046113283949847762202

    G = (Gx, Gy)

    message = text_to_int("No one knows the reason for all this, but it is probably quantum. - Pyramids, Terry Pratchett (1989)")

    def KeyGen(self):
      # generation
      private_key = random.getrandbits(256)
      public_key = apply_double_and_add_method(self.G, private_key, self.a, self.d, self.p)

      return public_key, private_key

    def Encaps(self, msg, sk, pk):
      # signing
      r = hashing(hashing(msg) + msg) % self.p

      R = apply_double_and_add_method(self.G, r, self.a, self.d, self.p)

      h = (R[0] + pk[0] + msg) % self.p
      s = (r + h * sk)

      P1 = apply_double_and_add_method(self.G, s, self.a, self.d, self.p)

      return R, P1
    
    def Decaps(self, R, pk, msg):
      # verify
      h = (R[0] + pk[0] + msg) % self.p

      P2 = add_points(R, apply_double_and_add_method(pk, h, self.a, self.d, self.p), self.a, self.d, self.p)

      return P2

    def sign(self, pk, sk):
      r = hashing(hashing(self.message) + self.message) % self.p

      R = apply_double_and_add_method(self.G, r, self.a, self.d, self.p)

      h = (R[0] + pk[0] + self.message) % self.p

      s = (r + h * sk)

      return R, s

    def verify(self, R, s, pk):
      h = (R[0] + pk[0] + self.message) % self.p

      P1 = apply_double_and_add_method(self.G, s, self.a, self.d, self.p)
        
      P2 = add_points(R, apply_double_and_add_method(pk, h, self.a, self.d, self.p), self.a, self.d, self.p)

      return P1 == P2