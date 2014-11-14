from flask import Flask, render_template, request, redirect, session,  url_for, escape
import MySQLdb

#from datetime import datetime
#from momentjs import momentjs

app = Flask(__name__)#, static_path = '/static', static_url_path = '/static')
#app.jinja_env.globals['momentjs'] = momentjs
db = MySQLdb.connect(host="localhost", user="root", passwd="13051992", db="clientes")


@app.route("/")
def index():
	return render_template("index.html")	
    

@app.route("/cadastro")
def cadastro():
	return render_template("cadastro.html")	


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        cur = db.cursor()
        cur.execute("SELECT * FROM usuarios WHERE nome = '%s' and senha= '%s';" %  (nome, senha))
        informacao = cur.fetchall()
        cur.execute("SELECT * FROM usuarios WHERE nome = '%s' and senha= '%s';" %  (nome, senha))
        tecno = cur.fetchall()
        cur.close()

        if len(informacao) > 0:
            session['user_id'] = tecno[0][0]
            session['user_nome'] = tecno[0][1]    

        else:
            return render_template("erro.html")    

        #return redirect(url_for('cliente'))
        return render_template("cliente.html", informacao=informacao)
    return render_template("index.html")     
     

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))  

@app.route("/cliente")
def cliente():
    cur = db.cursor()
    if 'user_id' in session:
        cur.execute("SELECT produto,data FROM lista3 WHERE usuario_id = %i;" % session['user_id'])
        mensagem = cur.fetchall()
        cur.execute("SELECT nome FROM usuarios WHERE nome= '%s';" %  session['user_nome'])
        informacao = cur.fetchall()
        cur.close()
        return render_template("cliente.html", informacao=informacao ,mensagem=mensagem )
    return render_template("index.html")    

@app.route("/visualizar")   
def visualizar():
    cur = db.cursor()
    if 'user_id' in session:
        cur.execute("SELECT produto,data FROM lista3 WHERE usuario_id = %i;" % session['user_id'])
        mensagem = cur.fetchall()
        cur.execute("SELECT nome FROM usuarios WHERE nome= '%s';" %  session['user_nome'])
        informacao = cur.fetchall()
        cur.execute("SELECT id FROM lista3 WHERE usuario_id = %i;" % session['user_id'])
        id_id = cur.fetchall()
        dados = id_id[0][0]
        cur.execute("SELECT data FROM lista3 WHERE id= '%s';" %  (dados))
        data = cur.fetchall()
        cur.close()
        return render_template("visualizar.html", informacao=informacao ,mensagem=mensagem , data=data)
    return render_template("index.html")      

@app.route("/postarmensagem", methods=["POST"])
def postarmensagem():
    if 'user_id' in session:
        mensagem = request.form['produto']
        cur = db.cursor()
        cur.execute("INSERT INTO lista3(produto,usuario_id) VALUES('%s', %i);" % (mensagem,session['user_id']))
        db.commit()
        cur.close()
        return redirect("/cliente") # Apos cadastrar a lista, redirecionar para a rota clientes     
    return render_template("index.html")  


@app.route("/deletar", methods=["GET"])
def deletar():
    if request.method == "GET":
        if 'user_id' in session:
            produto = request.form['produto']
            cur = db.cursor()
            cur.execute("DELETE FROM lista3 WHERE produto = '%s';" % (produto))
            db.commit()
            cur.close()
            return redirect("/visalizar") # Apos deletar, redirecionar para a roto clientes       
    return render_template("/index.html")
		
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form['nome']
    senha = request.form['senha']
    email = request.form['email'] 
    cur = db.cursor()
    cur.execute("INSERT INTO usuarios(nome, senha, email) VALUES('%s', '%s', '%s');" % (nome, senha, email) )
    db.commit()
    cur.close()
    return redirect("/") # Apos cadastrar, redirecionar para a rota visualizar		

@app.route('/<nome>', methods=["POST","GET"])
def user(nome):
    
    if request.method == "GET":
        cur = db.cursor()
        username = nome
        cur.execute("SELECT id FROM usuarios WHERE nome= '%s';" %  (username))
        informacao = cur.fetchall()
        dados = informacao[0][0]
        cur.execute("SELECT produto,data FROM lista3 WHERE usuario_id = %i;" % (dados))
        mensagem = cur.fetchall()
            
        cur.close()
        return render_template("visualizar.html" ,mensagem=mensagem)#, informacao=informacao
    else:
        return "erro" 
	
app.secret_key = 'Sq\xdb\xfb\x12\xb5\x08\xf4tS\xc2w\x06\x9e\x14hrOq>$o\xd0\x94'
		
if __name__ == "__main__":
	app.run(debug = True)
