# locustfile.py — Realistic Shopping User Journey + Breaking Point Test

from locust import HttpUser, task, between
import random

PRODUCT_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15]  # only active products (exclude ID 10, 16)


class ShoppingUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        """
        Called once per virtual user when they start.
        Register a unique user and login to get a JWT token.
        """
        # Create a unique user for this VU
        unique_id = random.randint(100000, 999999)
        self.user_email = f"loadtest_user_{unique_id}@example.com"
        self.user_password = "password123"

        # Register
        self.client.post("/users/register", json={
            "username": f"loadtest_{unique_id}",
            "email": self.user_email,
            "password_hash": self.user_password,
            "role": "user",
        }, name="/users/register")

        # Login to get token
        login_resp = self.client.post("/auth/login", json={
            "email": self.user_email,
            "password": self.user_password,
        }, name="/auth/login")

        if login_resp.status_code == 200:
            self.token = login_resp.json().get("access_token")

    @property
    def auth_headers(self):
        """Return Authorization header if token is available."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    @task
    def shopping_journey(self):
        """
        Simulate a realistic user journey:
        1. Browse all products
        2. Pick a specific product by ID
        3. Create an order for that product
        4. Fetch the order just created
        """
        # Step 1: GET all products
        self.client.get("/store/products", name="/store/products")

        # Step 2: GET a random product by ID
        product_id = random.choice(PRODUCT_IDS)
        self.client.get(
            f"/store/products/{product_id}",
            name="/store/products/<id>"
        )

        # Step 3: POST a new order for that product
        order_resp = self.client.post(
            "/orders",
            json={
                "items": [
                    {"product_id": product_id, "quantity": random.randint(1, 3)}
                ]
            },
            headers=self.auth_headers,
            name="/orders [POST]"
        )

        # Step 4: GET the order that was just created (only if POST succeeded)
        if order_resp.status_code == 201:
            order_data = order_resp.json()
            order_id = order_data.get("id")
            if order_id:
                self.client.get(
                    f"/orders/{order_id}",
                    headers=self.auth_headers,
                    name="/orders/<id>"
                )
