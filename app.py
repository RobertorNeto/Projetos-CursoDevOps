from flask import Flask,jsonify,request,make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
import os   

load_dotenv(dotenv_path= 'C:\\Users\\rbcor\\OneDrive\\Desktop\\API_receitas\\variaveis.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Ingredientes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable = False)
    unidade_de_medida = db.Column(db.String(100), nullable = False)

    receitas = db.relationship('IngredienteReceita', backref='ingredientes_relacionados', lazy=True)
    
    def __repr__(self):
        return f"Ingrediente {self.nome}"

class Receita(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100),nullable = False)
    metodo_de_preparo = db.Column(db.Text)

    ingredientes = db.relationship('IngredienteReceita', backref='receita_relacionada', lazy=True)



    def __repr__(self):
        return f"Receita {self.nome}"
    
class IngredienteReceita(db.Model):
    __tablename__ = 'ingrediente_receita'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    id_receita = db.Column(db.Integer, db.ForeignKey('receita.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)   
    unidade_de_medida = db.Column(db.String(100), nullable=False)

    ingrediente = db.relationship('Ingredientes', backref='receitas_relacionadas', lazy=True)
    receita = db.relationship('Receita', backref='ingredientes_relacionados', lazy=True)

    @property
    def unidade_de_medida(self):
        return self.ingrediente.unidade_de_medida
    

@app.route('/receitas',methods=['POST'])  
def adicionar_nova_receita():
    receita = request.get_json()

    if 'nome' not in receita or 'metodo_de_preparo' not in receita:
        return jsonify({'message' : 'Faltando dados obrigatórios'}),400

    nova_receita = Receita(
        nome = receita['nome'],
        metodo_de_preparo = receita['metodo_de_preparo']
    )

    db.session.add(nova_receita)
    db.session.commit()

    for ing in receita['ingredientes']:
        ingrediente =  Ingredientes.query.filter_by(nome = ing['nome']).first()
        if ingrediente:
            relacao = IngredienteReceita(
                id_ingrediente = ingrediente.id,
                id_receita = nova_receita.id,
                quantidade = ing['quantidade']
            )
            db.session.add(relacao)

    db.session.commit()

    return jsonify({'message': 'Receita criada com sucesso!'}), 201



@app.route('/receitas',methods=['GET'])
def obter_receitas():
    receitas = Receita.query.all()
    result = []
    for receita in receitas:
        ingredientes = []
        for ing in receita.ingredientes:
            ingrediente = {
                'id' : ing.id,
                'nome' : ing.ingrediente.nome,
                'quantidade' : ing.quantidade,
                'unidade_de_medida' : ing.ingrediente.unidade_de_medida
            }
            ingredientes.append(ingrediente)

        result.append({
            'id': receita.id,
            'nome': receita.nome,
            'metodo_de_preparo': receita.metodo_de_preparo,
            'ingredientes': ingredientes 
        })

    return jsonify(result)

@app.route('/receitas/<string:nome>', methods=['PUT'])
def editar_receitas_por_nome(nome):
    try:
        receita_alterada = request.get_json()  # Obter dados da requisição
        receita = Receita.query.filter_by(nome=nome).first()

        if receita:
            # Garantir que receita.id não seja None
            if not receita.id:
                return jsonify({'message': 'Receita não encontrada ou com ID inválido'}), 404

            # Limpa os ingredientes antigos da receita
            receita.ingredientes.clear()

            # Atualiza os ingredientes da receita com os novos dados
            for ing in receita_alterada['ingredientes']:
                ingrediente = Ingredientes.query.filter_by(nome=ing['nome']).first()

                if ingrediente:
                    # Cria a relação entre a receita e o ingrediente
                    relacao = IngredienteReceita(
                        id_ingrediente=ingrediente.id,
                        id_receita=receita.id,  # Aqui, `id_receita` é garantido
                        quantidade=ing['quantidade'],
                    )
                    db.session.add(relacao)  # Adiciona a relação ao banco de dados

            # Comita as alterações dos ingredientes
            db.session.commit()

            # Atualiza os dados da receita
            receita.nome = receita_alterada['nome']
            receita.metodo_de_preparo = receita_alterada['metodo_de_preparo']

            # Comita as alterações da receita
            db.session.commit()

            # Organiza os ingredientes para retornar
            ingredientes = []
            for relacao in receita.ingredientes:
                ingrediente_novo = {
                    'nome': relacao.ingrediente.nome,
                    'quantidade': relacao.quantidade,
                    'unidade_de_medida': relacao.ingrediente.unidade_de_medida
                }
                ingredientes.append(ingrediente_novo)

            # Retorna os dados da receita atualizada
            return jsonify({
                'id': receita.id,
                'nome': receita.nome,
                'metodo_de_preparo': receita_alterada['metodo_de_preparo'],
                'ingredientes': ingredientes
            }), 200

        else:
            return jsonify({'message': 'Receita não encontrada'}), 404

    except Exception as e:
        # Captura exceções e retorna a mensagem de erro
        return jsonify({'message': f'Ocorreu um erro ao atualizar a receita: {str(e)}'}), 500

    

@app.route('/receitas/<string:nome>',methods=['DELETE'])
def excluir_receitas(nome): 
    receita = Receita.query.filter_by(nome = nome).first()
    if receita:
        IngredienteReceita.query.filter_by(id_receita=receita.id).delete()

        db.session.delete(receita)
        db.session.commit()
        return jsonify({'message': 'Receita excluída com sucesso'}),200
    else:
        return jsonify({'message': 'Receita não encontrada'}), 404





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



@app.route('/ingredientes/<string:nome>',methods=['GET'])
def obter_ingrediente_por_nome(nome):
    ingrediente = Ingredientes.query.filter_by(nome=nome).first()
    if ingrediente:
        return jsonify({
            'id': ingrediente.id,
            'nome': ingrediente.nome,
            'unidade_de_medida': ingrediente.unidade_de_medida
        })
    else:
        return jsonify({'message': 'Ingrediente não encontrado'}), 404



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
        }), 200
    else:
        return jsonify({'message': 'Ingrediente não encontrado'}), 404
    


@app.route('/ingredientes',methods=['POST'])
def adicionar_novo_ingrediente():
    novo_ingrediente = request.get_json()

    if 'nome' not in novo_ingrediente or 'unidade_de_medida' not in novo_ingrediente:
        return jsonify({'message' : 'Faltando dados obrigatórios'}), 400
    
    ingrediente = Ingredientes(
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

        ingredientes_tabelarelacao = IngredienteReceita.query.filter_by(id_ingrediente = ingrediente.id).all()
        for ingrediente_relacao in  ingredientes_tabelarelacao:
            db.session.delete(ingrediente_relacao)  

        db.session.delete(ingrediente)
        db.session.commit() 

        return jsonify({'message': 'Ingrediente excluído com sucesso'}),200
    else:
        return jsonify({'message': 'Ingrediente não encontrado'}), 404
    


with app.app_context(): 
    db.create_all() 
    
if __name__ == "__main__":
    app.run(port=5000,host='localhost',debug=True)