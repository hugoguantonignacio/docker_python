from flask import Flask

app = Flask(__name__)

try:
    with open("volume/data.txt", "r") as file:
        data = file.read()
        file.close()
except:
    data = "failed to open data"

@app.route("/")
def myapp():
    return rf"<h1>Načtená data:</h1><p>{data}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0")