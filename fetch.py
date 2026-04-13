#!/usr/bin/env python3
"""
Recuperation des codes promo Zooplus depuis shopilo.fr
Sursa: https://shopilo.fr/reductions/zooplus.fr
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

SHOPILO_URL = "https://shopilo.fr/reductions/zooplus.fr"
STORE_NAME = "Zooplus"


def fetch_coupons(url=SHOPILO_URL):
    """Renvoie la liste des coupons actifs pour Zooplus depuis shopilo.fr"""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; coupon-fetcher/1.0; +https://github.com/shopilo-fr/code-promo-zooplus)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la recuperation : {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    coupons = []

    for item in soup.select(".coupon-item, [data-coupon], .offer-card"):
        code_el     = item.select_one("[data-code], .coupon-code, .code")
        discount_el = item.select_one(".discount, .percent, .amount")
        desc_el     = item.select_one(".title, .description, h3")
        expires_el  = item.select_one(".expires, .expiry, [data-expires]")

        coupon = {
            "store":      STORE_NAME,
            "code":       code_el.get_text(strip=True)     if code_el     else None,
            "discount":   discount_el.get_text(strip=True) if discount_el else None,
            "description":desc_el.get_text(strip=True)     if desc_el     else None,
            "expires":    expires_el.get_text(strip=True)  if expires_el  else None,
            "source":     SHOPILO_URL,
            "fetched_at": datetime.now().isoformat()
        }

        if coupon["description"]:
            coupons.append(coupon)

    return coupons


if __name__ == "__main__":
    print(f"Recuperation des codes promo {{STORE_NAME}} depuis shopilo.fr...\n")
    coupons = fetch_coupons()

    if coupons:
        print(json.dumps(coupons, ensure_ascii=False, indent=2))
        print(f"\nTotal : {{len(coupons)}} coupons trouves")
    else:
        print(f"Aucun coupon trouve. Liste complete sur : {SHOPILO_URL}")
