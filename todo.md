# Analysis
- [x] Documentation of requirements

# Design
- [x] Decide Stack
- [x] Database design
- [] Architecture design
- [] Architecture scaled proposal

# Overall implementation steps
- Setup environment
    - [x] Setup UV
    - [x] Setup docker dev container 
        - [x] Setup Django and postgresql connection in container
- Implementation of solution
    - [x] 1. As an Admin, I want to manage other admins, so that I can assess who has admin permissions  to change the catalog system
        a. Use cases:
            i. 1.1 - Create users
                - Acceptance Criteria:
                    - [x] Only admins should be able to perform this
                    - [x] After execution, a new user with the specified username and encrypted password should be created in the database
                    - [x] If a user already exists, it should not create a user in the database and throw an error
            ii. 1.2 - Update users
                - Acceptance Criteria:
                    - [x] Only admins should be able to perform this
                    - [x] After execution, the user should be updated with new data
                    - [x] After execution, if user is superuser, it should fail
            iii. 1.3 - Delete users
                - Acceptance Criteria:
                    - [x] Only admins should be able to perform this
                    - [x] After execution, the user should be deactivated in the database
                    - [x] After execution, if user is superuser, it should fail
    - [x] 2. As an Admin, I want to manage the products, so that I can adapt the product to current market and tendencies
        a. Use cases:
            i. 2.1 - Create products
                - Acceptance Criteria:
                    - [x] Only admins should be able to perform this
                    - [x] After execution, a new product should be created in the database with the specified parameters
            ii. 2.2 - Update products
                - Acceptance Criteria:
                    - [x] Only admins should be able to perform this
                    - [x] After execution, the product should be updated with the new data
            iii. 2.3 - Delete products
                - Acceptance Criteria:
                    - [x] Only admins should be able to perform this
                    - [x] After execution, the product should not exist in the database
    - [x] 3. As an Admin, I want to receive notifications on any change of products, so that I can track the history of the products
        a. Use cases:
            i. 3.1 - Send email notification on change of products
                - Acceptance Criteria:
                    - [x] After an execution of update or delete on products, an email should be sent to all the admins
    - [x] 4. As an Anonymous user, I want to view the products so that I can know if what I want is available for purchase
        a. Use cases:
            i. 4.1 - Read products
                - Acceptance Criteria:
                    - [x] After execution, users will get all the products in the database
                    - [x] Users should be able to see one product
                        - [x] For every individual product seen, the views counter should increase
    - [x] 5. As an Anonymouse user with admin account, I want to sign in to the catalog system, so that I can perform admin actions
        a. User cases:
            i. 5.1 - Login
                - Acceptance Criteria
                    - [x] After execution, it should create a new refresh token and store it with the user
                    - [x] After execution, it should create a new access token
                    - [x] After execution, it should return the new refresh token and access token
            ii. 5.2 - Refresh token
                - Acceptance Criteria
                    - [x] After execution, it should revoke the previous refresh token and return a new access token
                    - [x] After execution, if refresh token does not match with user or was not found, it should throw an error
- [x] Swagger documentation
- [x] Unit testing
- [x] Github workflows for automated unit tests on pull request
- [x] Deployment
    - [x] Deployment of service
    - [x] Deployment of DB
- [] Research about reporting