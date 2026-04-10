from xmlrpc.server import SimpleXMLRPCServer
import math

def calculate_factorial(n):
    print(f"Received request to calculate factorial for: {n}")
    return math.factorial(n)

server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC Server is listening on port 8000...")

server.register_function(calculate_factorial, "factorial")

server.serve_forever()