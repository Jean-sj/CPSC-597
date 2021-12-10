package game;

import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;

import org.bson.Document;
import org.neo4j.driver.*;
import org.neo4j.driver.types.Node;

import static org.neo4j.driver.Values.parameters;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

public class BuildGraphLinks {
	
	private static final String MONGO_URI = "mongodb://127.0.0.1:27017";
	
	private static final String NEO4J_BOLT_URI = "bolt://localhost:7687";
	private static final String NEO4J_USERNAME = "neo4j";
	private static final String NEO4J_PASSWORD = "neo4j";
	
	private List<String> getDeveloperList(Session session) {
		List<Record> res = session.writeTransaction(
			new TransactionWork<List<Record>>() {
				public List<Record> execute(Transaction tx) {
					Result result = tx.run("MATCH (d:Developer) RETURN d.name");
					List<Record> list = result.list();
					
					return list;
				}				 
			}
		);
		
		List<String> developersList = new ArrayList<>();		
		for (Record record : res) {
			String developerName = record.get("d.name").asString();
			System.out.println(developerName);
			developersList.add(developerName);
		}
						
		return developersList;
	}
	
	private void buildDeveloperGameLinks(Session session) {
		try (MongoClient mongoClient = MongoClients.create(MONGO_URI)) {
            MongoDatabase database = mongoClient.getDatabase("gamedb");
            MongoCollection<Document> collection = database.getCollection("games");
            
            FindIterable<Document> findIter = collection.find();
            MongoCursor<Document> mongoCursor = findIter.iterator();
            while (mongoCursor.hasNext()) {
            	Document doc = mongoCursor.next();
            	final String game = doc.getString("name");
            	final List<String> developers = doc.getList("developers", String.class);
            	for (String developer : developers) {
            		List<Record> res = session.writeTransaction(
            				new TransactionWork<List<Record>>() {
            					public List<Record> execute(Transaction tx) {
            						Result result = tx.run("MATCH (d:Developer), (g:Game) " +
            								"WHERE d.name = $developer AND g.name = $game " +
            								"CREATE (d)-[r:DEVELOPS]->(g) " + 
            								"RETURN d.name + ' develops ' + g.name", 
            								parameters("developer", developer, "game", game));
            						return result.list();
            					}
            				});
                	System.out.println(game);  
            	}
            	            	
            	System.out.println(game);            	            	            	
//            	List<String> developers = doc.getList("developers", String.class);
			}                        
        } catch (Exception e) {
			// TODO: handle exception
        	System.out.println(e.getMessage());
		}
	}
	
	private void buildPublisherGameLinks(Session session) {
		try (MongoClient mongoClient = MongoClients.create(MONGO_URI)) {
            MongoDatabase database = mongoClient.getDatabase("gamedb");
            MongoCollection<Document> collection = database.getCollection("games");
            
            FindIterable<Document> findIter = collection.find();
            MongoCursor<Document> mongoCursor = findIter.iterator();
            while (mongoCursor.hasNext()) {
            	Document doc = mongoCursor.next();
            	final String game = doc.getString("name");
            	final List<String> publishers = doc.getList("publishers", String.class);
            	for (String publisher : publishers) {
            		List<Record> res = session.writeTransaction(
            				new TransactionWork<List<Record>>() {
            					public List<Record> execute(Transaction tx) {
            						Result result = tx.run("MATCH (p:Publisher), (g:Game) " +
            								"WHERE p.name = $publisher AND g.name = $game " +
            								"CREATE (p)-[r:PUBLISHES]->(g) " + 
            								"RETURN p.name + ' publishes ' + g.name", 
            								parameters("publisher", publisher, "game", game));
            						return result.list();
            					}
            				});
                	System.out.println(publisher);  
            	}
            	            	
            	System.out.println(game);            	            	            	
//            	List<String> developers = doc.getList("developers", String.class);
			}                        
        } catch (Exception e) {
			// TODO: handle exception
        	System.out.println(e.getMessage());
		}
	}
	
	
	private void buildGameLinks(Session session, LinkType linkType, String origin, String destination, String relation) {
		try (MongoClient mongoClient = MongoClients.create(MONGO_URI)) {
            MongoDatabase database = mongoClient.getDatabase("gamedb");
            MongoCollection<Document> collection = database.getCollection("games");
            
            FindIterable<Document> findIter = collection.find();
            MongoCursor<Document> mongoCursor = findIter.iterator();
            while (mongoCursor.hasNext()) {
            	Document doc = mongoCursor.next();
            	final String destVal = doc.getString(origin);
            	final List<String> originList = doc.getList(origin, String.class);
            	for (String originVal : originList) {
            		List<Record> res = session.writeTransaction(
            				new TransactionWork<List<Record>>() {
            					public List<Record> execute(Transaction tx) {
            						Result result = tx.run("MATCH (d:" + destination.substring(0, 1).toUpperCase() + destination.substring(1) + "), (o:" + origin.substring(0, 1).toUpperCase() + origin.substring(1) + ") " +
            								"WHERE d.name = $destination AND o.name = $origin " +
            								"CREATE (d)-[r:" + relation.toUpperCase() + "]->(o) " + 
            								"RETURN d.name + ' " + relation.toLowerCase() + " ' + g.name", 
            								parameters("origin", originVal, "destination", destVal));
            						return result.list();
            					}
            				});
            		if (res.size() > 0) {
            			System.out.println(res.get(0).toString());  
            		}                	
            	}            	            	            	
			}                        
        } catch (Exception e) {
			// TODO: handle exception
        	System.out.println(e.getMessage());
		}
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Driver driver = GraphDatabase.driver(NEO4J_BOLT_URI, AuthTokens.basic(NEO4J_USERNAME, NEO4J_PASSWORD));
		Session session = driver.session();
		
		BuildGraphLinks b = new BuildGraphLinks();				
//		b.buildDeveloperGameLinks(session);
		b.buildPublisherGameLinks(session);
		
		System.out.print("Finished!");
		
		session.close();
		driver.close();
	}
	
	public enum LinkType {
		Single,
		Multiple,
	}
	
}
