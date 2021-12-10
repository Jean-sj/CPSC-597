package game;

import org.neo4j.driver.*;

import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;

import static com.mongodb.client.model.Filters.eq;
import static org.neo4j.driver.Values.parameters;

import org.bson.Document;


public class ImportGraphData {
	
	private static final String mongoUri = "mongodb://127.0.0.1:27017";
	
	private static void importGames(Session session) {				
		try (MongoClient mongoClient = MongoClients.create(mongoUri)) {
            MongoDatabase database = mongoClient.getDatabase("gamedb");
            MongoCollection<Document> collection = database.getCollection("games");
            
            FindIterable<Document> findIter = collection.find();
            MongoCursor<Document> mongoCursor = findIter.iterator();
            while (mongoCursor.hasNext()) {
            	Document doc = mongoCursor.next();
            	final String name = doc.getString("name");
            	final String game = session.writeTransaction(
        				new TransactionWork<String>() {
        					public String execute(Transaction tx) {
        						Result result = tx.run("CREATE (g:Game {name: $name}) " + 
        								"RETURN g.name", 
        								parameters("name", name));
        						return result.single().get(0).asString();
        					}
        				});
            	System.out.println(game);            	            	            	
//            	List<String> developers = doc.getList("developers", String.class);
			}                        
        } catch (Exception e) {
			// TODO: handle exception
        	System.out.println(e.getMessage());
		}				
	}
	
	private static void importDevelopers(Session session) {
		try (MongoClient mongoClient = MongoClients.create(mongoUri)) {
            MongoDatabase database = mongoClient.getDatabase("gamedb");
            MongoCollection<Document> collection = database.getCollection("developers");
            
            FindIterable<Document> findIter = collection.find();
            MongoCursor<Document> mongoCursor = findIter.iterator();
            while (mongoCursor.hasNext()) {
            	Document doc = mongoCursor.next();
            	final String name = doc.getString("name");
            	final String country = doc.getString("country");
            	final String city = doc.getString("city");
            	final String foundYear = doc.getString("est_year");
            	final String status = doc.getString("status");
            	final String game = session.writeTransaction(
        				new TransactionWork<String>() {
        					public String execute(Transaction tx) {
        						Result result = tx.run("CREATE (d:Developer {name: $name, country: $country, city: $city, foundYear: $foundYear, status: $status}) " + 
        								"RETURN d.name", 
        								parameters("name", name, "country", country, "city", city, "foundYear", foundYear, "status", status));
        						return result.single().get(0).asString();
        					}
        				});
            	System.out.println(game);            	            	            	
//            	List<String> developers = doc.getList("developers", String.class);
			}                        
        } catch (Exception e) {
			// TODO: handle exception
        	System.out.println(e.getMessage());
		}
	}
	
	private static void importPublishers(Session session) {
		try (MongoClient mongoClient = MongoClients.create(mongoUri)) {
            MongoDatabase database = mongoClient.getDatabase("gamedb");
            MongoCollection<Document> collection = database.getCollection("publishers");
            
            FindIterable<Document> findIter = collection.find();
            MongoCursor<Document> mongoCursor = findIter.iterator();
            while (mongoCursor.hasNext()) {
            	Document doc = mongoCursor.next();
            	final String name = doc.getString("name");
            	final String country = doc.getString("country");
            	final String city = doc.getString("city");
            	final String foundYear = doc.getString("est_year");
            	final String status = doc.getString("status");
            	final String game = session.writeTransaction(
        				new TransactionWork<String>() {
        					public String execute(Transaction tx) {
        						Result result = tx.run("CREATE (p:Publisher {name: $name, country: $country, city: $city, foundYear: $foundYear, status: $status}) " + 
        								"RETURN p.name", 
        								parameters("name", name, "country", country, "city", city, "foundYear", foundYear, "status", status));
        						return result.single().get(0).asString();
        					}
        				});
            	System.out.println(game);            	            	            	
//            	List<String> developers = doc.getList("developers", String.class);
			}                        
        } catch (Exception e) {
			// TODO: handle exception
        	System.out.println(e.getMessage());
		}
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Driver driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.basic("neo4j", "neo4j"));
		Session session = driver.session();
		
		
//		importGames(session);
//		importDevelopers(session);
		importPublishers(session);
		
		System.out.print("Success!");
		session.close();
		driver.close();
	}	

}
