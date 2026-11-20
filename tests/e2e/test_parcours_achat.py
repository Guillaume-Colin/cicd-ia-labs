"""Tests E2E Playwright — parcours d'achat MiniShop (Atelier 8).

Prérequis : application lancée (make run) ; BASE_URL=http://localhost:8000 par défaut.
Lancer :   pytest -m e2e --headed --slowmo 300
"""

import re

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.shop_page import ShopPage

pytestmark = pytest.mark.e2e


@pytest.fixture
def shop(page: Page, app_url) -> ShopPage:
    """Ouvre la boutique ; chaque test repart d'une page neuve (panier vide)."""
    return ShopPage(page, app_url).open()


def test_page_accueil(shop: ShopPage):
    """La page d'accueil affiche le titre et les 5 produits du catalogue."""
    expect(shop.page).to_have_title(re.compile("MiniShop"))
    expect(shop.products).to_have_count(5)


def test_parcours_achat_welcome10(shop: ShopPage):
    """2 mugs + WELCOME10 -> total 27.40 € -> commande confirmée."""
    shop.add("mug", qty=2)
    expect(shop.cart_line("mug")).to_have_text(re.compile(r"× 2"))

    shop.apply_coupon("WELCOME10")
    expect(shop.discount()).to_have_text("2.50")
    expect(shop.total()).to_have_text("27.40")

    shop.order()
    expect(shop.confirmation).to_have_text(re.compile(r"Commande .+ confirmée"))


def test_coupon_invalide_affiche_une_erreur(shop: ShopPage):
    """Un coupon inconnu affiche un message d'erreur accessible (role=alert)."""
    shop.add("mug").apply_coupon("NOEL2026")
    expect(shop.error).to_contain_text("Coupon inconnu")


def test_commander_desactive_si_panier_vide(shop: ShopPage):
    """« Commander » est désactivé tant que le panier est vide, actif ensuite."""
    expect(shop.order_btn).to_be_disabled()
    shop.add("mug")
    expect(shop.order_btn).to_be_enabled()
