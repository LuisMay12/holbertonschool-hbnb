#!/usr/bin/python3
"""
HBnB Entity Validator
Validates all core business logic constraints
"""

import uuid
from datetime import datetime

class EntityValidator:
    @staticmethod
    def validate_user(user):
        assert isinstance(user.id, uuid.UUID), "Invalid UUID"
        assert '@' in user.email, "Invalid email"
        assert len(user.password) >= 8, "Password too short"
        assert isinstance(user.is_admin, bool), "Admin flag must be boolean"

    @staticmethod
    def validate_place(place):
        assert place.price >= 10.0, "Price < $10 minimum"
        assert -90 <= place.latitude <= 90, "Invalid latitude"
        assert -180 <= place.longitude <= 180, "Invalid longitude"

    @staticmethod
    def validate_review(review):
        assert 1 <= review.rating <= 5, "Rating must be 1-5"
        assert 10 <= len(review.comment) <= 500, "Comment length invalid"

if __name__ == "__main__":
    print("Validation module ready for import")
