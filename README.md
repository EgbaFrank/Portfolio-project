# GroceryHub Web Application

## Introducion
GroceryHub is a web-based application that enable users to plan and organize their grocery shopping efficiently. It provides a streamlined shopping experience, allowing users to create shopping lists, select products from various stores, compare prices, and track orders with ease. As such, GroceryHub aims to provide a convenient and user-friendly platform for grocery shopping.

## Features
GroceryHub offers the following features to streamline your grocery shopping experience:
- Create and manage personalized shopping lists
- Browse and Search products across multiple shops
- Compare prices from various local stores to get the best deals.
- Place orders directly to stores from shopping lists and track orders with real-time status updates.
- User-friendly interface for easy navigation and use

## Technology Stack
- Backend: Flask (Python) as the web framework
- Frontend: HTML, CSS, JavaScript
- Database: SQLAlchemy for database ORM (MySQL)
- API Documentation: Swagger for API documentation
- Testing: Unit tests using unittest framework
- Version Control: Git/GitHub for code management

## Installation
### Requirements
- Python 3.8+
- Flask 2.0+
- MySQL 8.0+
- SQLAlchemy
- pip
- python-dotenv
- Swagger
- flask_cors

### Steps
1. Clone the repository: `git clone (https://github.com/EgbaFrank/Portfolio-project.git)`
2. Create a MySQL database by running `cat setup_mysql_dev.sql | sudo mysql` as mysql root user
3. Ensure port 5000 and 5001 is open
4. Run the application: `GH_STORAGE_TYPE=db GH_API_PORT=5001` python -m web_flask.app` on a command window
5. Run the API server: `GH_STORAGE_TYPE=db python -m api.v1.app` on another command window

### Usage
1. Access the application at http://localhost:5001
2. Click try demo to use the application demo

## Wiki
For detailed documentation, please visit our wiki page
