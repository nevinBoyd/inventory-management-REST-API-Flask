# Inventory Management System – Flask REST API

This project is an inventory management system for a small retail environment.  
It provides a REST API for creating, viewing, updating, and deleting products.  
It also integrates real-time product lookup from the OpenFoodFacts API and includes a CLI tool for direct interaction from the terminal.

This system is designed for an admin workflow — the type used behind an e-commerce site to manage what products are available.

---

## Features

- Full CRUD API using Flask
- Fetch product details from an external API using product name
- Command-line interface for managing inventory without using a browser or Postman
- In-memory data store for simplified testing and demonstration
- Automated testing with pytest, including mocking external API calls

---

## File Structure

```
inventory-management-REST-API-Flask
├── inventory_api/
│   ├── app.py                # Flask API routes + logic
│   ├── external_api.py       # OpenFoodFacts integration
│   └── __init__.py
├── tests/
│   └── test_api.py           # Single clean test suite
├── cli.py                    # Click-based command-line tool
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation & Setup

Clone the repo and enter the project:

```
git clone <your-repo-url>
cd inventory-management-REST-API-Flask
```

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install required packages:

```
pip install -r requirements.txt
```

Run the API:

```
python3 -m flask --app inventory_api.app run --debug
```

The server starts at:
http://127.0.0.1:5000


## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /inventory | Get all items |
| GET | /inventory/\<id> | Get item by ID |
| POST | /inventory | Add inventory item |
| PATCH | /inventory/\<id> | Update fields |
| DELETE | /inventory/\<id> | Delete item |
| GET | /inventory/fetch/\<name> | Import item from OpenFoodFacts |

## CLI Tool

A Click-based CLI is included to interact with the API faster.

Run the CLI:

```
python cli.py --help
```

Example commands:

```
python cli.py list
python cli.py add "New Product" 5 12.99
python cli.py update 2 --quantity 20
python cli.py fetch "almond milk"
python cli.py delete 2
```


## Testing

Pytest suite includes:

- CRUD functionality
- Error handling
- Mocked external API calls
- Inventory reset between tests

Run tests:

```
pytest -q
```

Result example:

```
6 passed in 0.10s
```


### Screenshots

These screenshots demonstrate the API running, CLI usage via cURL, and the test suite passing:

- [Flask Server Running](./screenshots/server.png)
- [CRUD API Calls via cURL](./screenshots/CURL.png)
- [Unit Tests Passing (pytest)](./screenshots/pytest.png)

## Resources

These are the references that directly supported how this project was designed and executed:

### External API Used in This Project
- [OpenFoodFacts Official API Documentation](https://openfoodfacts.github.io/openfoodfacts-server/api/)

### Click & CLI Implementation
- [Build AWESOME CLIs With Click in Python – ArjanCodes](https://www.youtube.com/watch?v=FWacanslfFM)

### Python Code Organization & Project Structure
- [How to Organize Your Python Code: Splitting Files into Modules – ArjanCodes](https://www.youtube.com/watch?v=NtjiCkf1t2c)
- [What Does the Structure of a Modern Python Project Look Like? – ArjanCodes](https://www.youtube.com/watch?v=Lr1koR-YkMw)

### Language Specification
- [Python Official Documentation (3.12)](https://docs.python.org/3.12/)


## Reflection & Takeaways

After receiving feedback on my previous summative, I wanted to show that I could not only meet expectations — but exceed them with stronger structure, testing, and professional workflow.

Key improvements I focused on:

- Clear separation of concerns across dedicated modules instead of one large script
- A single, well-organized pytest suite with isolated test cases
- External API calls mocked to ensure fast and reliable testing
- A fully functional CLI built using Click to enhance real-world usability
- A structured Git workflow using branches and pull requests for every feature

Click was not part of the curriculum, but it allowed me to demonstrate practical command-line tooling using the Python fundamentals that *have* been taught — imports, APIs, environment setup, and data handling.

Overall, this project represents a direct response to previous feedback — applying it, leveling up, and delivering something intentionally built to be cleaner, more maintainable, and closer to professional standards.
