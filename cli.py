# CLI tool for interacting with the Inventory API

import click
import requests

API_URL = "http://127.0.0.1:5000/inventory"

@click.group()
def cli():
    """Inventory Management CLI"""
    pass


# LIST all inventory items
@cli.command()
def list():
    """List all inventory items"""
    response = requests.get(API_URL)
    data = response.json()
    click.echo("📦 Inventory:")
    for item in data:
        click.echo(f"- ID: {item['id']} | {item['name']} | Qty: {item['quantity']} | ${item['price']}")


# ADD a new product to inventory
@cli.command()
@click.argument("name")
@click.argument("quantity", type=int)
@click.argument("price", type=float)
def add(name, quantity, price):
    """Add a new product"""
    new_item = {
        "name": name,
        "quantity": quantity,
        "price": price
    }
    response = requests.post(API_URL, json=new_item)
    click.echo(f"Added: {response.json()}")


# UPDATE an item’s price or quantity
@cli.command()
@click.argument("item_id", type=int)
@click.option("--quantity", type=int, help="New quantity")
@click.option("--price", type=float, help="New price")
def update(item_id, quantity, price):
    """Update an existing product"""
    update_data = {}
    if quantity is not None:
        update_data["quantity"] = quantity
    if price is not None:
        update_data["price"] = price

    response = requests.patch(f"{API_URL}/{item_id}", json=update_data)
    click.echo(f"Updated: {response.json()}")


# DELETE a product from inventory
@cli.command()
@click.argument("item_id", type=int)
def delete(item_id):
    """Delete a product from inventory"""
    response = requests.delete(f"{API_URL}/{item_id}")
    click.echo(response.json())


# FETCH external product data and add to inventory
@cli.command()
@click.argument("name")
def fetch(name):
    """Fetch product from external API and add to inventory"""
    response = requests.get(f"{API_URL}/fetch/{name}")
    click.echo(f"Fetched: {response.json()}")


if __name__ == "__main__":
    cli()
