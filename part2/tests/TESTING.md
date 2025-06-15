# HBnB API Testing Report

## User Endpoints Testing

| Test Case | Request | Expected Result | Actual Result | Status |
|-----------|---------|-----------------|---------------|--------|
| Create valid user | POST /users/ | 201 Created | 201 Created | ✅ |
| Create user with invalid email | POST /users/ | 400 Bad Request | 400 Bad Request | ✅ |
| List users | GET /users/ | 200 OK with list | 200 OK with list | ✅ |

## Place Endpoints Testing

| Test Case | Request | Expected Result | Actual Result | Status |
|-----------|---------|-----------------|---------------|--------|
| Create place with valid data | POST /places/ | 201 Created | 201 Created | ✅ |
| Create place with negative price | POST /places/ | 400 Bad Request | 400 Bad Request | ✅ |

## Edge Cases Tested

1. Attempt to create review with non-existent user_id
2. Attempt to update place with invalid coordinates
3. Delete non-existent review
4. Get list of reviews for non-existent place
