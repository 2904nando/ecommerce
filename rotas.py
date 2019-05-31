from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

from test_products import dict_produtos

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

users = [User(id) for id in range(1, 21)]

@app.route("/")
def home():
    return render_template("home.html", dict_produtos=dict_produtos)

@app.route("/produto/<codigo>", methods=['GET'])
def produto(codigo):
    return render_template("produto.html", produto = dict_produtos[str(codigo)])

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username
            user = User(id)
            login_user(user)
            return redirect("/")
        else:
            return abort(401)
    else:
        return render_template("login.html")

@app.route("/registro")
def register():
    return render_template("registro.html")

@app.route("/esqueciSenha")
def esqueciSenha():
    return render_template("esquecisenha.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/carrinho")
@login_required
def carrinho():
    return render_template("carrinho.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@login_manager.user_loader
def load_user(userid):
    return User(userid)

if __name__ == "__main__":
    app.run(debug=True)