const { MongoClient } = require("mongodb");
const dotenv = require('dotenv');

dotenv.config();

const connectionString = process.env.MONGODB_URI || "";
const client = new MongoClient(connectionString);

let db;

async function connectDB() {
  try {
     // Await connection
    const conn = await client.connect();
    // Access the database
    db = conn.db("BFDISearch"); 
    console.log("Connected to MongoDB");
    return db;
  } catch (e) {
    console.error("Failed to connect to MongoDB", e);
    throw e;
  }
}

module.exports = connectDB;