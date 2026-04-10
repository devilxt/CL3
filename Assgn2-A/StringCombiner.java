import java.rmi.Remote;
import java.rmi.RemoteException;

public interface StringCombiner extends Remote {
    // Method to concatenate two strings
    public String concatenate(String s1, String s2) throws RemoteException;
}