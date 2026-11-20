"""Page Object de la boutique MiniShop (Atelier 8).

Tous les localisateurs de la page sont ici : si le HTML change, on ne corrige qu'un endroit.
Les méthodes d'action renvoient `self` pour pouvoir les enchaîner.
"""

from playwright.sync_api import Locator, Page, expect


class ShopPage:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url
        self.products = page.get_by_test_id("products").get_by_role("listitem")
        self.coupon = page.get_by_label("Code promo")
        self.quote_btn = page.get_by_role("button", name="Calculer le total")
        self.order_btn = page.get_by_role("button", name="Commander")
        self.error = page.get_by_role("alert")
        self.confirmation = page.get_by_test_id("confirmation")

    def open(self) -> "ShopPage":
        """Ouvre la boutique et attend que le catalogue soit chargé."""
        self.page.goto(self.url)
        expect(self.page.get_by_test_id("add-mug")).to_be_visible()
        return self

    def add(self, product: str, qty: int = 1) -> "ShopPage":
        """Ajoute `qty` fois le produit au panier."""
        for _ in range(qty):
            self.page.get_by_test_id(f"add-{product}").click()
        return self

    def cart_line(self, product: str) -> Locator:
        return self.page.get_by_test_id(f"cart-{product}")

    def apply_coupon(self, code: str) -> "ShopPage":
        """Saisit le coupon et calcule le total."""
        self.coupon.fill(code)
        self.quote_btn.click()
        return self

    def total(self) -> Locator:
        """Localisateur (et non texte) : les assertions restent web-first."""
        return self.page.get_by_test_id("total")

    def discount(self) -> Locator:
        return self.page.get_by_test_id("discount")

    def order(self) -> "ShopPage":
        self.order_btn.click()
        return self
