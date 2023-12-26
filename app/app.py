from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', name='Huraira')

@app.route('/greet', methods=['POST'])
def greet():
    user_name = request.form['name']
    return render_template('index.html', name=user_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
