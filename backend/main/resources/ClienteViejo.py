from flask_restful import Resource
from flask import jsonify, request




clientes = [
    {
        "id": 1,
        "nombre": "Diego",
        "apellido":"Córdoba"
    },
      {
        "id": 2,
        "nombre": "Juan",
        "apellido":"Perez"
    }
]

class Clientes(Resource):
    #obtener clientes
    def get(self):

        return jsonify( 
            {
                "clientes": clientes
            }
        )
    #agregar cliente
    def post(self):
        cliente = request.get_json()
        clientes.append(cliente)
        return cliente, 201


class Cliente(Resource):
    #obtener cliente requerido
    def get(self,id):

        return jsonify( 
            {
                "cliente": clientes[int(id)]
            }
        )
  
