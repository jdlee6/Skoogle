from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=True)
# from app import routes