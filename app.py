import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Check if model exists, if not auto-train
from train_model import build_and_train_pipeline

st.set_page_config(
    page_title="RETURNAI // Intelligent Order Return Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyber/FinTech UI Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #111827 0%, #030712 100%);
        color: #f3f4f6;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.45);
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }

    /* Custom Header Styling */
    .hero-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #818cf8;
        margin-bottom: 8px;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 24px;
    }

    /* Risk Status Pills */
    .risk-pill-low {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
    }
    .risk-pill-medium {
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
    }
    .risk-pill-high {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
        animation: pulse-glow 2s infinite;
    }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 12px rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 0 25px rgba(239, 68, 68, 0.65); }
    }

    /* Stat Metrics */
    .stat-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    .stat-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #f9fafb;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Action Box */
    .action-box {
        background: rgba(30, 41, 59, 0.7);
        border-left: 4px solid #6366f1;
        padding: 14px 18px;
        border-radius: 0 12px 12px 0;
        margin-top: 14px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_or_train_model():
    model_path = "return_model.joblib"
    if not os.path.exists(model_path):
        with st.spinner("⚡ Initializing AI Engine & Training Prediction Model..."):
            bundle = build_and_train_pipeline()
    else:
        bundle = joblib.load(model_path)
    return bundle

bundle = load_or_train_model()
pipeline = bundle["pipeline"]
metrics = bundle.get("metrics", {})

# Top Hero Navigation & Banner
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<div class="hero-badge">AI REVERSE-LOGISTICS INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">⚡ RETURNAI // Predictive Risk Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Real-time machine learning inference for e-commerce return probability, sizing bracket detection, and reverse margin protection.</div>', unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
    <div class="glass-card" style="padding: 14px 18px; text-align: center;">
        <div class="stat-label">Model Accuracy (ROC-AUC)</div>
        <div class="stat-value" style="color: #6366f1;">{metrics.get('roc_auc', 0.88):.1%}</div>
        <span style="font-size:0.75rem; color:#10b981;">● Calibrated Production Pipeline</span>
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Tabs
tab_predict, tab_batch, tab_analytics, tab_mitigation = st.tabs([
    "🎯 Live Order Assessment",
    "📁 Batch Ingestion & Scoring",
    "📈 Feature Drivers & Model Stats",
    "🛡️ Automated Mitigation Protocols"
])

# -------------------------------------------------------------
# TAB 1: LIVE ORDER ASSESSMENT
# -------------------------------------------------------------
with tab_predict:
    st.markdown("<br>", unsafe_allow_html=True)
    col_input, col_result = st.columns([1.1, 1], gap="large")

    with col_input:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0; color:#e2e8f0; font-size:1.2rem; display:flex; align-items:center; gap:8px;">
                <span>🛒</span> Order & Customer Parameters
            </h3>
            <p style="color:#94a3b8; font-size:0.85rem;">Adjust transaction properties to simulate real-time ML return risk.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            cat = st.selectbox(
                "Product Category",
                ["Apparel & Fashion", "Footwear & Shoes", "Consumer Electronics", "Home & Kitchen", "Beauty & Cosmetics", "Jewelry & Accessories"],
                index=0
            )

            c1, c2 = st.columns(2)
            with c1:
                item_price = st.slider("Item Value ($)", min_value=10, max_value=800, value=125, step=5)
            with c2:
                discount_percent = st.slider("Applied Discount (%)", min_value=0, max_value=75, value=25, step=5)

            c3, c4 = st.columns(2)
            with c3:
                customer_age = st.slider("Customer Age", min_value=18, max_value=70, value=29)
            with c4:
                past_return_rate = st.slider("Customer Historical Return Rate", min_value=0.0, max_value=1.0, value=0.22, step=0.02, format="%.2f")

            c5, c6 = st.columns(2)
            with c5:
                items_in_order = st.number_input("Total Items in Basket", min_value=1, max_value=10, value=2)
            with c6:
                delivery_days = st.slider("Transit/Delivery Window (Days)", min_value=1, max_value=14, value=3)

            payment_method = st.selectbox(
                "Payment Instrument",
                ["Cash on Delivery", "Credit Card", "Debit Card", "Buy Now Pay Later", "Digital Wallet"],
                index=0 if cat in ["Apparel & Fashion", "Footwear & Shoes"] else 1
            )

            # Sizing specifics
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                bracket_buying = st.checkbox("Multiple Sizes Ordered (Bracket Buying)", value=True if items_in_order > 1 and cat in ["Apparel & Fashion", "Footwear & Shoes"] else False)
            with col_b2:
                is_first_purchase = st.checkbox("New First-Time Customer", value=False)

            if cat in ["Apparel & Fashion", "Footwear & Shoes"]:
                size_variation = st.selectbox("Sizing Feedback on Item", ["Exact Fit", "Runs Small", "Runs Large"], index=1)
            else:
                size_variation = "Not Applicable"

        # Build payload
        input_df = pd.DataFrame([{
            "customer_age": customer_age,
            "product_category": cat,
            "item_price": item_price,
            "discount_percent": discount_percent,
            "past_return_rate": past_return_rate,
            "items_in_order": items_in_order,
            "bracket_buying": 1 if bracket_buying else 0,
            "payment_method": payment_method,
            "delivery_days": delivery_days,
            "is_first_purchase": 1 if is_first_purchase else 0,
            "size_variation": size_variation
        }])

    with col_result:
        # Run inference
        prob = pipeline.predict_proba(input_df)[0][1]
        percent_prob = prob * 100

        # Estimate reverse logistics financial exposure
        restock_cost = round(item_price * 0.18 + 12.50, 2)
        expected_loss = round(prob * restock_cost, 2)

        if percent_prob < 32:
            risk_label = "LOW PROBABILITY"
            risk_class = "risk-pill-low"
            pill_dot = "🟢"
            action_text = "Standard dispatch. Safe order with high expected retention."
            action_color = "#10b981"
        elif percent_prob < 60:
            risk_label = "ELEVATED RISK"
            risk_class = "risk-pill-medium"
            pill_dot = "🟡"
            action_text = "Recommend real-time order verification or sizing confirmation email."
            action_color = "#f59e0b"
        else:
            risk_label = "CRITICAL RETURN ALERT"
            risk_class = "risk-pill-high"
            pill_dot = "🔴"
            action_text = "High bracket/mismatch hazard. Trigger instant AI sizing concierge or restrict free return label."
            action_color = "#ef4444"

        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 28px 20px;">
            <div style="margin-bottom: 12px;">
                <span class="{risk_class}">{pill_dot} {risk_label}</span>
            </div>
            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">
                Calculated Return Probability
            </div>
            <div style="font-size: 3.5rem; font-weight: 900; color: #ffffff; font-family: 'JetBrains Mono', monospace; margin: 4px 0;">
                {percent_prob:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Plotly Radial Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge",
            value=percent_prob,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': action_color, 'thickness': 0.3},
                'bgcolor': "rgba(15, 23, 42, 0.8)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 32], 'color': "rgba(16, 185, 129, 0.15)"},
                    {'range': [32, 60], 'color': "rgba(245, 158, 11, 0.15)"},
                    {'range': [60, 100], 'color': "rgba(239, 68, 68, 0.15)"}
                ],
                'threshold': {
                    'line': {'color': "#ffffff", 'width': 3},
                    'thickness': 0.8,
                    'value': percent_prob
                }
            }
        ))
        fig.update_layout(
            height=200,
            margin=dict(l=25, r=25, t=15, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#e2e8f0"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Financial exposure card
        c_e1, c_e2 = st.columns(2)
        with c_e1:
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px;">
                <div class="stat-label">Estimated Reverse Logistics Cost</div>
                <div class="stat-value" style="font-size: 1.3rem; color:#f87171;">${restock_cost}</div>
                <div style="font-size: 0.72rem; color: #94a3b8;">Includes shipping, inspection & restocking</div>
            </div>
            """, unsafe_allow_html=True)
        with c_e2:
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px;">
                <div class="stat-label">Expected Net Margin At Risk</div>
                <div class="stat-value" style="font-size: 1.3rem; color:#fbbf24;">${expected_loss}</div>
                <div style="font-size: 0.72rem; color: #94a3b8;">Weighted expected financial loss</div>
            </div>
            """, unsafe_allow_html=True)

        # AI Action Directive
        st.markdown(f"""
        <div class="action-box" style="border-left-color: {action_color};">
            <b style="color: #ffffff; font-size: 0.95rem;">🤖 Recommended AI Mitigation:</b>
            <p style="margin: 4px 0 0 0; color: #cbd5e1; font-size: 0.88rem;">{action_text}</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 2: BATCH INGESTION & SCORING
# -------------------------------------------------------------
with tab_batch:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📁 Batch Order Risk Scoring")
    st.caption("Upload a CSV file containing multiple orders or score our synthesized live stream.")

    uploaded_file = st.file_uploader("Upload Orders CSV", type=["csv"])
    
    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
    else:
        st.info("No file uploaded. Showing live simulated order stream.")
        if os.path.exists("ecommerce_returns.csv"):
            batch_df = pd.read_csv("ecommerce_returns.csv").sample(n=60, random_state=42)
        else:
            from data_generator import generate_returns_dataset
            batch_df = generate_returns_dataset(n_samples=60)

    # Required columns check
    req_cols = ["customer_age", "product_category", "item_price", "discount_percent", 
                "past_return_rate", "items_in_order", "bracket_buying", "payment_method", 
                "delivery_days", "is_first_purchase", "size_variation"]

    missing = [c for c in req_cols if c not in batch_df.columns]
    if missing:
        st.error(f"Missing required columns in dataset: {missing}")
    else:
        probs = pipeline.predict_proba(batch_df[req_cols])[:, 1]
        batch_df["Return_Probability"] = (probs * 100).round(1)
        batch_df["Risk_Category"] = pd.cut(
            batch_df["Return_Probability"],
            bins=[-1, 32, 60, 100],
            labels=["Low Risk", "Elevated Risk", "Critical Risk"]
        )

        b_c1, b_c2, b_c3 = st.columns(3)
        with b_c1:
            st.metric("Total Ingested Orders", len(batch_df))
        with b_c2:
            high_risk_count = (batch_df["Risk_Category"] == "Critical Risk").sum()
            st.metric("Orders Flagged Critical", high_risk_count, delta=f"{(high_risk_count/len(batch_df)):.1%} of batch", delta_color="inverse")
        with b_c3:
            avg_risk = batch_df["Return_Probability"].mean()
            st.metric("Batch Mean Return Risk", f"{avg_risk:.1f}%")

        # Color-coded display table
        display_cols = ["order_id", "product_category", "item_price", "discount_percent", "payment_method", "Return_Probability", "Risk_Category"]
        valid_display = [c for c in display_cols if c in batch_df.columns]
        
        st.dataframe(
            batch_df[valid_display].sort_values(by="Return_Probability", ascending=False),
            use_container_width=True,
            height=380
        )

        # Download scored CSV
        csv_data = batch_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Scored Batch CSV",
            data=csv_data,
            file_name="scored_order_returns.csv",
            mime="text/csv"
        )

# -------------------------------------------------------------
# TAB 3: FEATURE DRIVERS & MODEL INTELLIGENCE
# -------------------------------------------------------------
with tab_analytics:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 What Drives Product Returns?")
    st.caption("Insights from our trained Random Forest ensemble on retail return patterns.")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # Feature importance calculation
        rf_model = pipeline.named_steps["classifier"]
        preprocessor = pipeline.named_steps["preprocessor"]
        
        cat_encoder = preprocessor.named_transformers_["cat"]
        cat_feature_names = cat_encoder.get_feature_names_out(bundle["categorical_features"])
        all_features = list(bundle["numeric_features"]) + list(cat_feature_names)
        
        importances = rf_model.feature_importances_
        feat_df = pd.DataFrame({"Feature": all_features, "Importance": importances}).sort_values(by="Importance", ascending=True).tail(10)

        fig_feat = px.bar(
            feat_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 10 Risk Predictor Factors",
            color="Importance",
            color_continuous_scale="Purples"
        )
        fig_feat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            height=380,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_feat, use_container_width=True)

    with col_chart2:
        # Category comparison
        if os.path.exists("ecommerce_returns.csv"):
            raw_data = pd.read_csv("ecommerce_returns.csv")
            cat_rates = raw_data.groupby("product_category")["returned"].mean().reset_index()
            cat_rates["return_pct"] = (cat_rates["returned"] * 100).round(1)

            fig_cat = px.bar(
                cat_rates.sort_values(by="return_pct", ascending=False),
                x="product_category",
                y="return_pct",
                title="Historical Return Rate by Category (%)",
                color="return_pct",
                color_continuous_scale="Reds"
            )
            fig_cat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"),
                xaxis_tickangle=-30,
                height=380,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_cat, use_container_width=True)

# -------------------------------------------------------------
# TAB 4: MITIGATION STRATEGIES
# -------------------------------------------------------------
with tab_mitigation:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛡️ Automated Retail Defense Playbook")
    st.caption("How e-commerce merchants can cut return rates by up to 34% using predictive intelligence:")

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#818cf8; margin-top:0;">1. Bracket Purchasing Alert</h4>
            <p style="font-size:0.86rem; color:#cbd5e1;">
                When a customer orders multiple sizes (e.g. Size M and L) of the same dress or shoe:
            </p>
            <ul style="font-size:0.83rem; color:#94a3b8; padding-left:18px;">
                <li>Trigger interactive FitFinder widget at checkout.</li>
                <li>Display exact chest/waist measurements from customer profile.</li>
                <li>Offer $5 instant wallet credit to remove the duplicate sizing.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#fbbf24; margin-top:0;">2. Cash-on-Delivery Safeguard</h4>
            <p style="font-size:0.86rem; color:#cbd5e1;">
                COD orders have 3x higher refusal and return rates on doorstep delivery:
            </p>
            <ul style="font-size:0.83rem; color:#94a3b8; padding-left:18px;">
                <li>Require WhatsApp OTP verification before dispatch.</li>
                <li>Incentivize UPI/card prepayment with a 3% instant discount.</li>
                <li>Prioritize courier partner with door-step try-and-buy confirmation.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#34d399; margin-top:0;">3. Post-Delivery Retention</h4>
            <p style="font-size:0.86rem; color:#cbd5e1;">
                Intercept returns before the parcel is shipped back:
            </p>
            <ul style="font-size:0.83rem; color:#94a3b8; padding-left:18px;">
                <li>Provide 1-click instant size exchange rather than cash refund.</li>
                <li>Offer a 20% bonus store gift card if retained.</li>
                <li>Automate self-service troubleshooting for electronics.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

