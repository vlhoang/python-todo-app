from flask import Flask, render_template
import os
from flask import jsonify
import socket

app = Flask(__name__)

@app.route("/quote")
def quote():
    return jsonify({
        "quote": "Life is what happens when you're busy making other plans.",
        "author": "John Lennon"
    })


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