import time
import threading
import random

# 1. SERVER CLASS
class Server:
    def __init__(self, name):
        self.name = name
        self.active_connections = 0
        self.lock = threading.Lock()

    def handle_request(self, request_id, duration):
        """Simulates processing a request for a specific duration."""
       
        with self.lock:
            self.active_connections += 1
            
        print(f"[{self.name}] Started Request {request_id} (Duration: {duration}s) | Active: {self.active_connections}")
        
        time.sleep(duration)
        with self.lock:
            self.active_connections -= 1
            
        print(f"[{self.name}] Finished Request {request_id} | Active: {self.active_connections}")


# 2. LOAD BALANCER CLASS
class LoadBalancer:
    def __init__(self, servers, algorithm="round_robin"):
        self.servers = servers
        self.algorithm = algorithm
        self.round_robin_index = 0

    def route_request(self, request_id, duration):
        """Routes the request based on the selected algorithm."""
        selected_server = None

        if self.algorithm == "round_robin":
            selected_server = self.servers[self.round_robin_index]
            self.round_robin_index = (self.round_robin_index + 1) % len(self.servers)
            
        elif self.algorithm == "least_connections":
            # Pick the server with the absolute minimum active connections
            selected_server = min(self.servers, key=lambda s: s.active_connections)

        print(f"[Load Balancer] Routing Request {request_id} to {selected_server.name} using {self.algorithm}")
        
        threading.Thread(target=selected_server.handle_request, args=(request_id, duration)).start()

# 3. SIMULATION RUNNER
def run_simulation(algorithm_name):
    print(f"\n{'='*50}\nStarting {algorithm_name.upper()} Simulation\n{'='*50}")
    
    servers = [Server("Server_A"), Server("Server_B"), Server("Server_C")]
    
    lb = LoadBalancer(servers, algorithm=algorithm_name)
    
    for i in range(1, 11):
        process_time = random.randint(1, 5)
        lb.route_request(request_id=i, duration=process_time)
        
        time.sleep(0.5)

    time.sleep(6)


if __name__ == "__main__":
    run_simulation("round_robin")
    
    run_simulation("least_connections")