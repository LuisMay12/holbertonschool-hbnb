from flask_restx import Namespace, Resource, fields
from app.services.facade import hbnb_facade

api = Namespace('reviews', description='Review operations', path='/api/v1/reviews')

# Input model for validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Output model for display
review_output_model = api.inherit('ReviewOutput', review_model, {
    'id': fields.String(description='Review ID')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_output_model, code=201)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = api.payload
        try:
            review = hbnb_facade.create_review(data)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_list_with(review_output_model)
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return hbnb_facade.get_all_reviews()


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_output_model)
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = hbnb_facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_output_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload
        try:
            updated = hbnb_facade.update_review(review_id, data)
            return updated
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            hbnb_facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}
        except ValueError as e:
            api.abort(404, str(e))


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_output_model)
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            return hbnb_facade.get_reviews_by_place(place_id)
        except ValueError as e:
            api.abort(404, str(e))
