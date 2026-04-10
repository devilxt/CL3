import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

try:
    num = int(input("Enter an integer to find its factorial: "))
    
    result = proxy.factorial(num)
    print(f"The factorial of {num} is {result}")
    
except Exception as e:
    print(f"An error occurred: {e}")