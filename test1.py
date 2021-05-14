from flask import Flask, render_template, redirect, url_for, request, flash
app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if login_check(request.form['test'],request.form['password']):
            flash('success')
            flash('ffffff')
            return redirect(url_for('hello',username=request.form.get('test')))
    return render_template('login.html')

def login_check(username,password):
    if username=='admin' and password == 'hello':
        return True
    else:
        return False

@app.route('/buy')
def index():
    return render_template('buy.html')

@app.route('/chinese')
def chinese():
    return render_template('chinesebook.html')

@app.route('/english')
def english():
    return render_template('engilshbook.html')

@app.route('/kid')
def kid():
    return render_template('kidbook.html')

@app.route('/magazine')
def magazine():
    return render_template('magazine.html')





















if __name__ == '__main__':
    app.debug = True
    app.secret_key = "Your Key"
    app.run()

















