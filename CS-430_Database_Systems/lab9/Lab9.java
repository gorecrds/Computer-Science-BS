import java.sql.*;

public class Lab9 {

    public static void main(String[] args) {
        try {
            String host = System.getenv("DBHOST");
            if (host == null || host.trim().isEmpty()) {
                host = "faure";
            }

            String port = System.getenv("DBPORT");
            if (port == null || port.trim().isEmpty()) {
                port = "3306";
            }
            String dbuser = System.getenv("DBUSER");
            String dbpass = System.getenv("DBPASS");
            String dbname = System.getenv("DBNAME");

            if (dbname == null || dbname.trim().isEmpty()) {
                dbname = dbuser;
            }

            if (dbuser == null || dbuser.trim().isEmpty() || dbpass == null) {
                throw new SQLException("DBUSER and DBPASS environment variables must be set.");
            }
            Class.forName("org.mariadb.jdbc.Driver");

            String url = "jdbc:mariadb://" + host + ":" + port + "/" + dbname + "?sslMode=trust";
            Connection con = DriverManager.getConnection(url, dbuser, dbpass);

            System.out.println("Connection Established.");

            con.close();
            
            System.out.println("Connection Closed");  
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}