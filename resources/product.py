import asyncio

from flask_restful import Resource, reqparse
from models.product import ProductModel
from config.confing import UPDATE_RESPONSE, DELETE_RESPONSE
from event_loop import event_loop

class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('instance_id',
                        type=str,
                        required=False,
                        help="product instance id"
                        )
    parser.add_argument('name',
                        type=str,
                        required=False,
                        help="product name"
                        )

    def get(self, instanceid):
        return {'message': 'Bad request'}, 404

    def post(self, instanceid):
        return {'message': 'Bad request'}, 404

    def delete(self, instanceid):
        try:
            data = Product.parser.parse_args()
            if data['name'] is None:
                delete_product = ProductModel(instanceid, DELETE_RESPONSE)
            else:
                delete_product = ProductModel(instanceid, DELETE_RESPONSE, data['name'])
            if DELETE_RESPONSE == 'ACCEPTED':
                asyncio.run_coroutine_threadsafe(delete_product.delay_time(),event_loop)
            return {'message': delete_product.json()}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def put(self, instanceid):
        try:
            data = Product.parser.parse_args()
            if data['name'] is None:
                update_product = ProductModel(instanceid, UPDATE_RESPONSE)
            else:
                update_product = ProductModel(instanceid, UPDATE_RESPONSE, data['name'])
            if UPDATE_RESPONSE == 'ACCEPTED':
                asyncio.run_coroutine_threadsafe(update_product.delay_time(),event_loop)
            return {'message': update_product.json()}, 200
        except:
            return {"message": "An error occurred when updating product."}, 500
