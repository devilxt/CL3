import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;

public class StringCombinerImpl extends UnicastRemoteObject implements StringCombiner {
    
    // Constructor must throw RemoteException
    protected StringCombinerImpl() throws RemoteException {
        super();
    }

    // Implementing the remote method
    @Override
    public String concatenate(String s1, String s2) throws RemoteException {
        System.out.println("Server received: '" + s1 + "' and '" + s2 + "'");
        return s1 + " " + s2; 
    }
}