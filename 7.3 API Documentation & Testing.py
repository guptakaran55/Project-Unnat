from flask_restx import Api, Resource, fields
from flask_restx import reqparse

# API Documentation with Swagger
api = Api(app, doc='/docs/', title='Building Design Optimizer API')

building_model = api.model('Building', {
    'orientation': fields.Float(required=True, description='Building orientation in degrees'),
    'window_wall_ratio': fields.Float(required=True, description='Window to wall ratio'),
    'height': fields.Float(required=True, description='Building height in meters'),
    'length': fields.Float(required=True, description='Building length in meters'),
    'width': fields.Float(required=True, description='Building width in meters')
})

@api.route('/api/optimize')
class OptimizeBuilding(Resource):
    @api.expect(building_model)
    def post(self):
        """Optimize building design for given parameters"""
        pass