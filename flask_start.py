from flask import Flask, render_template
#  引入form類別
from view_form import UserForm
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)


@app.route('/user', methods=['GET', 'POST'])
def user():
    form = UserForm()
    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if form.validate_on_submit():
        return 'Success Submit'
    #  如果不是提交過來的表單，就是GET，這時候就回傳user.html網頁
    return render_template('user.html', form=form)

if __name__ == '__main__':
    app.config['SECRET_KEY']='your key'
    app.debug = True
    app.run()
