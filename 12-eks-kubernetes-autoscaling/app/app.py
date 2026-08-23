from flask import Flask
import os
import socket
import time

app = Flask(__name__)


@app.route("/")
def home():
    hostname = socket.gethostname()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>EKS Kubernetes Demo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}

            .container {{
                max-width: 700px;
                margin: auto;
            }}

            .card {{
                border: 1px solid #ddd;
                padding: 25px;
                border-radius: 10px;
            }}

            code {{
                background: #f4f4f4;
                padding: 4px;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <h1>EKS Kubernetes Demo</h1>

            <div class="card">

                <h2>Application Information</h2>

                <p>
                    <strong>Pod:</strong>
                    {hostname}
                </p>

                <p>
                    <strong>Application:</strong>
                    Kubernetes Demo Application
                </p>

                <p>
                    <strong>Platform:</strong>
                    Amazon EKS
                </p>

                <hr>

                <p>
                    This application is running inside a Kubernetes pod.
                </p>

                <p>
                    Visit <code>/health</code> for the health check.
                </p>

                <p>
                    Visit <code>/load</code> to generate CPU load.
                </p>

            </div>

        </div>

    </body>
    </html>
    """


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "pod": socket.gethostname()
    }


@app.route("/load")
def load():
    start = time.time()

    while time.time() - start < 5:
        pass

    return {
        "message": "CPU load generated",
        "pod": socket.gethostname()
    }


@app.route("/ready")
def ready():
    return {
        "status": "ready"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
