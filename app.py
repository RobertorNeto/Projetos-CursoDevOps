from flask import Flask,jsonify,request,make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os   

load_dotenv(dotenv_path= 'C:\\Users\\rbcor\\OneDrive\\Desktop\\API_receitas\\variaveis.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Ingredientes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable = False)
    unidade_de_medida = db.Column(db.String(100), nullable = False)
    
    def __repr__(self):
        return f"Ingrediente {self.nome}"

class Receita(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    nome = db.Column(db.String(100),nullable = False)
    quantidade = db.Column(db.Integer,nullable = False)
    descricao = db.Column(db.Text)

    def __repr__(self):
        return f"Receita {self.nome}"
    


@app.route('/ingredientes',methods=['GET'])
def obter_ingredientes():
    ingredientes = Ingredientes.query.all()
    result = []
    for ingrediente in ingredientes:
        result.append({
            'id': ingrediente.id,
            'nome': ingrediente.nome,
            'unidade_de_medida': ingrediente.unidade_de_medida
        })
    return jsonify(result)


@app.route('/ingredientes',methods=['GET'])
def obter_ingrediente_por_nome(nome):
    ingredientes = Ingredientes.query.all()
    result = []
    for ingrediente in ingredientes:
        if ingrediente.get('nome') == nome:
            result.append({
            'id': ingrediente.id,
            'nome': ingrediente.nome,
            'unidade_de_medida': ingrediente.unidade_de_medida
            })
    return jsonify(result)


@app.route('/ingredientes/<string:nome>',methods= ['PUT'])
def editar_ingrediente_por_nome(nome):
    ingrediente_alterado = request.get_json()
    ingrediente = Ingredientes.query.filter_by(nome=nome).first()
    if ingrediente:
        ingrediente.id = ingrediente_alterado.get('id',ingrediente.id)
        ingrediente.nome = ingrediente_alterado.get('nome',ingrediente.nome)
        ingrediente.unidade_de_medida = ingrediente_alterado.get('unidade_de_medida',ingrediente.unidade_de_medida)

        db.session.commit()
        return jsonify({
            'id': ingrediente.id,
            'nome': ingrediente.nome,
            'unidade_de_medida': ingrediente.unidade_de_medida
        })
    else:
        return jsonify({'message': 'Ingrediente não encontrado'}), 404
    
@app.route('/ingredientes',methods=['POST'])
def adicionar_novo_ingrediente():
    novo_ingrediente = request.get_json()

    if 'nome' not in novo_ingrediente or 'unidade_de_medida' not in novo_ingrediente:
        return jsonify({'message' : 'Faltando dados obrigatórios'}), 400
    
    ingrediente = Ingredientes(
        id = novo_ingrediente.get('id'),
        nome= novo_ingrediente.get('nome'),
        unidade_de_medida = novo_ingrediente.get('unidade_de_medida')
                               )
    
    
    db.session.add(ingrediente)
    db.session.commit()

    return jsonify({
         'id': ingrediente.id,
        'nome': ingrediente.nome,
        'unidade_de_medida': ingrediente.unidade_de_medida
    }), 201

@app.route('/ingredientes/<string:nome>',methods=['DELETE'])
def excluir_ingrediente(nome):
    ingrediente = Ingredientes.query.filter_by(nome=nome).first()
    if ingrediente:
        db.session.delete(ingrediente)
        db.session.commit()
        return jsonify({'message': 'Ingrediente excluído com sucesso'}),200
    else:
        return jsonify({'message': 'Ingrediente não encontrado'}), 404
    

with app.app_context():
    db.create_all() 
    
if __name__ == "__main__":
    app.run(port=5000,host='localhost',debug=True)