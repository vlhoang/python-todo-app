from flask import Flask, render_template
import os
from flask import jsonify
import socket
from azure.cosmos import CosmosClient
import random

app = Flask(__name__)

# Cosmos DB config (use environment variables for production)
COSMOS_URI = os.environ.get("COSMOS_URI")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
DATABASE_NAME = "quotesDB"
CONTAINER_NAME = "quotes"


if not COSMOS_URI or not COSMOS_KEY:
    raise ValueError("COSMOS_URI and COSMOS_KEY must be set as environment variables.")

# Connect to Cosmos DB
client = CosmosClient(COSMOS_URI, COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

@app.route("/quote")
def get_random_quote():
    pivot = random.random()  # Random float between 0 and 1

    # First try: random >= pivot
    query = f"SELECT TOP 1 c.text, c.author FROM c WHERE c.random >= {pivot} ORDER BY c.random ASC"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    if not items:
        # If none found, wrap around to smallest random values
        query = f"SELECT TOP 1 c.text, c.author FROM c WHERE c.random < {pivot} ORDER BY c.random ASC"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))

    if items:
        return jsonify(items[0])
    else:
        return jsonify({"text": "No quote found", "author": ""})


@app.route('/')
def index():
    return render_template('index.html')

def find_free_port(default_port=5000):
    """Find a free port starting from default_port."""
    port = default_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('0.0.0.0', port)) != 0:
                return port
            port += 1

if __name__ == '__main__':
    # Use PORT from environment if set, else auto-find one
    env_port = os.environ.get('PORT')
    if env_port:
        port = int(env_port)
    else:
        port = find_free_port(5000)
    
    print(f"Running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port)