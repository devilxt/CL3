import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class RMIServer {
    public static void main(String[] args) {
        try {
           
            StringCombinerImpl combiner = new StringCombinerImpl();
            Registry registry = LocateRegistry.createRegistry(1099);
            
            registry.rebind("StringCombinerService", combiner);
            
            System.out.println("RMI Server is ready and waiting for requests...");
        } catch (Exception e) {
            System.out.println("Server Exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}