from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def verify():
    username = request.form['username']
    password = request.form['password']
    # Verify username and password
    if username == 'admin' and password == 'password':
        return 'Logged in successfully!'
    else:
        return 'Incorrect username or password'

if __name__ == '__main__':
    app.run(debug=True)
