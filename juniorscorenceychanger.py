import streamlit as st

# ---------- Sample exchange rates (per 1 USD) ----------
rates_per_usd = {
    "USD": 1.00,
    "EUR": 0.90,
    "GBP": 0.76,
    "NGN": 1600.0,
    "JPY": 150.0,
    "CNY": 7.20,
    "CAD": 1.33,
    "AUD": 1.50,
    "INR": 83.0,
    "ZAR": 18.5,
}

CURRENCIES = list(rates_per_usd.keys())

st.title("💱 juniors currency changer")

# ---------- Sidebar controls ----------
with st.sidebar:
    st.subheader("Settings")
    amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)
    colA, colB = st.columns(2)
    with colA:
        from_curr = st.selectbox("From", CURRENCIES, index=CURRENCIES.index("USD"))
    with colB:
        to_curr = st.selectbox("To", CURRENCIES, index=CURRENCIES.index("NGN"))

    use_custom = st.checkbox("Use a custom exchange rate (override)")
    if use_custom:
        custom_rate = st.number_input(
            f"1 {from_curr} =", min_value=0.0, value=1.0, step=0.01, format="%f"
        )
        st.write(f"… {custom_rate} {to_curr}")

st.write("")

# ---------- Conversion logic ----------
def convert(amount: float, from_code: str, to_code: str) -> float:
    """Convert using cross-rates where rates_per_usd are units of currency per 1 USD."""
    if from_code == to_code:
        return amount
    # Convert from 'from_code' to USD, then USD to 'to_code'
    usd_value = amount / rates_per_usd[from_code]
    return usd_value * rates_per_usd[to_code]

if use_custom:
    # Custom-rate mode: directly multiply amount by the provided rate.
    result = amount * custom_rate
else:
    result = convert(amount, from_curr, to_curr)

# ---------- Output ----------
st.markdown(
    f"<div style='font-size:1.5rem; font-weight:700;'>{amount:,.2f} {from_curr} = {result:,.2f} {to_curr}</div>",
    unsafe_allow_html=True,
)

# Extra context
if not use_custom:
    st.info(
        "Using built-in sample rates (per 1 USD). These values are for demo only and might not be up-to-date. "
        "Tick 'Use a custom exchange rate' in the sidebar to override.",
        icon="ℹ️",
    )
else:
    st.success(
        "Custom exchange rate is active. Your conversion uses your provided rate.", icon="✅"
    )

# Show current cross-rate for reference
if not use_custom and from_curr != to_curr:
    cross = convert(1.0, from_curr, to_curr)
    st.caption(f"Reference: 1 {from_curr} ≈ {cross:,.6f} {to_curr} (demo rate)")

st.divider()
st.markdown(
    "<span style='opacity:0.8;'>Tip: Use the Swap button in the sidebar to reverse the conversion direction.</span>",
    unsafe_allow_html=True,

)

