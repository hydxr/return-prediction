import numpy as np
import pandas as pd

def generate_returns_dataset(n_samples=3000, random_seed=42):
    """
    Generates a realistic e-commerce order dataset with return labels.
    Reflects genuine retail dynamics: bracket purchasing, sizing sensitivity,
    customer history, discount impulsivity, and delivery friction.
    """
    np.random.seed(random_seed)

    order_ids = [f"ORD-{10000 + i}" for i in range(n_samples)]
    customer_ids = [f"CUST-{np.random.randint(1000, 1800)}" for _ in range(n_samples)]

    categories = [
        "Apparel & Fashion",
        "Footwear & Shoes",
        "Consumer Electronics",
        "Home & Kitchen",
        "Beauty & Cosmetics",
        "Jewelry & Accessories"
    ]
    category_weights = [0.35, 0.20, 0.15, 0.12, 0.10, 0.08]
    cat_choices = np.random.choice(categories, size=n_samples, p=category_weights)

    ages = np.random.randint(18, 68, size=n_samples)
    
    # Prices vary by category
    base_prices = {
        "Apparel & Fashion": (30, 220),
        "Footwear & Shoes": (45, 280),
        "Consumer Electronics": (80, 850),
        "Home & Kitchen": (25, 300),
        "Beauty & Cosmetics": (15, 120),
        "Jewelry & Accessories": (50, 600)
    }
    prices = [round(np.random.uniform(*base_prices[c]), 2) for c in cat_choices]

    discounts = np.random.choice([0, 10, 20, 30, 40, 50, 60, 70], size=n_samples, 
                                 p=[0.15, 0.20, 0.25, 0.15, 0.10, 0.08, 0.05, 0.02])

    past_return_rates = np.clip(np.random.beta(a=1.5, b=5.0, size=n_samples), 0.0, 0.85)

    items_in_order = np.random.choice([1, 2, 3, 4, 5, 6], size=n_samples, p=[0.45, 0.25, 0.15, 0.08, 0.04, 0.03])

    # Sizing bracket buying: purchasing multiple sizes of same garment to return the wrong fit
    bracket_buying = []
    for c, items in zip(cat_choices, items_in_order):
        if c in ["Apparel & Fashion", "Footwear & Shoes"] and items >= 2:
            bracket_buying.append(1 if np.random.rand() < 0.38 else 0)
        else:
            bracket_buying.append(0)

    payment_methods = np.random.choice(
        ["Credit Card", "Debit Card", "Cash on Delivery", "Buy Now Pay Later", "Digital Wallet"],
        size=n_samples,
        p=[0.35, 0.20, 0.18, 0.15, 0.12]
    )

    delivery_days = np.random.choice([1, 2, 3, 4, 5, 7, 10, 14], size=n_samples,
                                     p=[0.12, 0.28, 0.25, 0.15, 0.10, 0.05, 0.03, 0.02])

    is_first_purchase = np.random.choice([0, 1], size=n_samples, p=[0.68, 0.32])

    # Sizing variation tag
    size_variation = []
    for c in cat_choices:
        if c in ["Apparel & Fashion", "Footwear & Shoes"]:
            size_variation.append(np.random.choice(["Exact Fit", "Runs Small", "Runs Large"], p=[0.55, 0.25, 0.20]))
        else:
            size_variation.append("Not Applicable")

    # Probabilistic Return Model (Ground Truth with Non-linear Noise)
    # Logit calculation
    logits = -1.8  # baseline return rate around 15-20%
    
    # Sizing and category risks
    cat_risk = {
        "Apparel & Fashion": 0.85,
        "Footwear & Shoes": 0.95,
        "Consumer Electronics": -0.40,
        "Home & Kitchen": -0.30,
        "Beauty & Cosmetics": -0.60,
        "Jewelry & Accessories": -0.20
    }
    
    pay_risk = {
        "Cash on Delivery": 0.65,
        "Buy Now Pay Later": 0.50,
        "Credit Card": -0.15,
        "Debit Card": 0.00,
        "Digital Wallet": -0.10
    }

    returns = []
    probs = []
    for i in range(n_samples):
        log_odds = logits
        log_odds += cat_risk[cat_choices[i]]
        log_odds += pay_risk[payment_methods[i]]
        log_odds += 2.8 * past_return_rates[i]
        log_odds += 1.4 * bracket_buying[i]
        
        # Discount effect: excessive discount -> impulse buy remorse
        if discounts[i] >= 40:
            log_odds += 0.45
            
        # Delivery delay friction
        if delivery_days[i] > 5:
            log_odds += 0.35
            
        # Size mismatch factor
        if size_variation[i] in ["Runs Small", "Runs Large"]:
            log_odds += 0.60

        # High ticket price adds return scrutiny
        if prices[i] > 400:
            log_odds += 0.30

        # Sigmoid probability
        prob = 1.0 / (1.0 + np.exp(-log_odds))
        # Add slight natural randomness
        prob = np.clip(prob + np.random.normal(0, 0.04), 0.01, 0.99)
        returned = 1 if np.random.rand() < prob else 0
        
        probs.append(round(float(prob), 4))
        returns.append(returned)

    df = pd.DataFrame({
        "order_id": order_ids,
        "customer_id": customer_ids,
        "customer_age": ages,
        "product_category": cat_choices,
        "item_price": prices,
        "discount_percent": discounts,
        "past_return_rate": [round(float(x), 3) for x in past_return_rates],
        "items_in_order": items_in_order,
        "bracket_buying": bracket_buying,
        "payment_method": payment_methods,
        "delivery_days": delivery_days,
        "is_first_purchase": is_first_purchase,
        "size_variation": size_variation,
        "return_probability_score": probs,
        "returned": returns
    })

    return df

if __name__ == "__main__":
    df = generate_returns_dataset()
    df.to_csv("ecommerce_returns.csv", index=False)
    print(f"Generated {len(df)} records. Return Rate: {df['returned'].mean():.2%}")

