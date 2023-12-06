from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino la tabla
class Cliente(db.Model):   # la clase Producto hereda de db.Model, esta clase representa la tabla "clientes" en la base de datos
    idclientes=db.Column(db.Integer, primary_key=True) #define los campos de la tabla
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    telefono=db.Column(db.Integer)
    localidad=db.Column(db.String(100))
    direccion=db.Column(db.String(400))
    bolson=db.Column(db.Integer)
    medio_de_pago=db.Column(db.String(45))
    dia_de_entrega=db.Column(db.String(45))    



    def __init__(self,nombre,apellido,telefono,localidad, direccion, bolson, medio_de_pago, dia_de_entrega):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.apellido=apellido
        self.telefono=telefono
        self.localidad=localidad
        self.direccion=direccion
        self.bolson=bolson
        self.medio_de_pago=medio_de_pago
        self.dia_de_entrega=dia_de_entrega

#  si hay que crear mas tablas , se hace aqui


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************

class ClienteSchema(ma.Schema):
    class Meta:
        fields=('idclientes','nombre','apellido','telefono','localidad', 'direccion', 'bolson', 'medio_de_pago', 'dia_de_entrega')


cliente_schema=ClienteSchema()            # El objeto producto_schema es para traer un producto
clientes_schema=ClienteSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto




# crea los endpoint o rutas (json)
@app.route('/cliente',methods=['GET'])
def get_Clientes():
    all_clientes=Cliente.query.all()  # el metodo query.all() lo hereda de db.Model
    result=clientes_schema.dump(all_clientes)  # el metodo dump() lo hereda de ma.schema y trae todos los registros de la tabla
    return jsonify(result)  # retorna un JSON de todos los registros de la tabla


#creo un endpoint para traer solo un cliente

@app.route('/cliente/<id>',methods=['GET'])
def get_cliente(id):
    cliente=Cliente.query.get(id)
    return cliente_schema.jsonify(cliente)   # retorna el JSON de un producto recibido como parametro


@app.route('/cliente/<id>',methods=['DELETE'])
def delete_cliente(id):
    cliente=Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return cliente_schema.jsonify(cliente)   # me devuelve un json con el registro eliminado


@app.route('/cliente', methods=['POST']) # crea ruta o endpoint
def create_cliente():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre = request.json['nombre']  
    apellido = request.json['apellido']  
    telefono = request.json['telefono']  
    localidad = request.json['localidad']  
    direccion = request.json['direccion'] 
    bolson = request.json['bolson'] 
    medio_de_pago = request.json['medio_de_pago'] 
    dia_de_entrega = request.json['dia_de_entrega'] 
    new_cliente = Cliente(nombre, apellido, telefono, localidad, direccion, bolson, medio_de_pago, dia_de_entrega )  # Crea un nuevo objeto Producto con los datos proporcionados
    db.session.add(new_cliente)  # Agrega el nuevo producto a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return clientes_schema.jsonify(new_cliente)


@app.route('/cliente/<id>' ,methods=['PUT'])
def update_cliente(id):
    cliente=Cliente.query.get(id)

# Actualiza los atributos del producto con los datos proporcionados en el JSON
    nombre = request.json['nombre']  
    apellido = request.json['apellido']  
    telefono = request.json['telefono']  
    localidad = request.json['localidad']  
    direccion = request.json['direccion'] 
    bolson = request.json['bolson'] 
    medio_de_pago = request.json['medio_de_pago'] 
    dia_de_entrega = request.json['dia_de_entrega'] 

    db.session.commit()  # Guarda los cambios en la base de datos
    return clientes_schema.jsonify(cliente)  # Retorna el JSON del cliente actualizado 

 


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
