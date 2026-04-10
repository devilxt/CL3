import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Scanner;

public class RMIClient {
    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            
            StringCombiner stub = (StringCombiner) registry.lookup("StringCombinerService");
            
            Scanner scanner = new Scanner(System.in);
            System.out.print("Enter the first string: ");
            String str1 = scanner.nextLine();
            
            System.out.print("Enter the second string: ");
            String str2 = scanner.nextLine();
            
            String result = stub.concatenate(str1, str2);
            System.out.println("Response from server: " + result);
            
            scanner.close();
        } catch (Exception e) {
            System.out.println("Client Exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}