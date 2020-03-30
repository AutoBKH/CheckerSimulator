import asyncio

from flask_restful import Resource, reqparse
from models.product import ProductModel

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
            delete_product = ProductModel(instanceid, data)
            return delete_product.get_response()

        except Exception as e:
            return {"message": str(e)}, 500

    def put(self, instanceid):
        try:
            data = Product.parser.parse_args()
            update_product = ProductModel(instanceid, data)
            return update_product.get_response()
        except:
            return {"message": "An error occurred when updating product."}, 500
