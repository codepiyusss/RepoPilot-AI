from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """Homepage route"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
