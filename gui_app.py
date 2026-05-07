import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
from datetime import datetime, timedelta
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SmartCity AI Command Center",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME/COLOR DEFINITIONS (For Graphs) ---
if st.config.get_option("theme.base") == "light":
    PLOTLY_TEMPLATE = "plotly_white"
    MAIN_COLOR = "#FF4B4B"  # Light Red
    ACCENT_COLOR = "#00B4D8" # Light Blue
else:
    PLOTLY_TEMPLATE = "plotly_dark"
    MAIN_COLOR = "#FF6B6B"  # Darker Red
    ACCENT_COLOR = "#90E0EF" # Cyan

# --- HELPER FUNCTIONS ---
def load_lottieurl(url: str):
    """Loads a Lottie animation from a URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Lottie Animation URLs
lottie_city = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_5njpXv.json")
lottie_weather = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_jm1w6yof.json")

def get_predicted_data(city):
    """Simulates ML Data Generation based on city input."""
    dates = [(datetime.now() + timedelta(days=i)).strftime('%d %b') for i in range(7)]
    seed = sum(ord(char) for char in city)
    random.seed(seed)
    
    temps = [random.randint(18, 35) for _ in range(7)]
    rain_prob = [random.randint(5, 95) for _ in range(7)]
    
    return pd.DataFrame({"Date": dates, "Temperature (°C)": temps, "Rain Probability (%)": rain_prob})

# --- MAIN UI ---

st.title("🏙️ Smart City AI: Predictive Weather Intelligence")
st.markdown("Monitor current conditions and access ML-driven 7-day monsoon forecasts.")

# Session State for persistence
if 'city_searched' not in st.session_state:
    st.session_state['city_searched'] = False
if 'last_city' not in st.session_state:
    st.session_state['last_city'] = ""

# --- SIDEBAR ---
with st.sidebar:
    st.info("💡 **Tip:** Go to Settings -> Theme to toggle Dark/Light mode.")
    st.header("Search Parameters")
    city_input = st.text_input("Target City/Region", "Himachal", placeholder="e.g. Delhi, London")
    
    analyze_btn = st.button("Analyze Weather", type="primary")

    if not st.session_state['city_searched'] and lottie_city:
        st_lottie(lottie_city, height=200, key="city_sidebar")

# --- DISPLAY RESULTS ---
if analyze_btn or st.session_state['city_searched']:
    st.session_state['city_searched'] = True
    active_city = city_input if analyze_btn else st.session_state['last_city']
    st.session_state['last_city'] = active_city

    with st.spinner(f"Processing Intelligence for {active_city}..."):
        df = get_predicted_data(active_city)
        curr_temp = df['Temperature (°C)'][0]
        curr_rain_prob = df['Rain Probability (%)'][0]

        # --- ROW 1: LIVE STATUS ---
        st.header(f"Live Intelligence: {active_city.title()}")
        c1, c2, c3 = st.columns([1, 2, 1])
        
        with c1:
            st.metric(label="Predicted Temp", value=f"{curr_temp}°C", delta=f"{random.randint(-2, 2)}°C")
            st.metric(label="Rain Chance (Today)", value=f"{curr_rain_prob}%")
            
        with c2:
            if lottie_weather:
                st_lottie(lottie_weather, height=220, key="weather_anim")
                
        with c3:
            if curr_rain_prob > 70:
                st.error("⛈️ Monsoon Active")
                status_desc = "High humidity detected. Expect rain."
            elif 40 <= curr_rain_prob <= 70:
                st.warning("⛅ Moderate Risk")
                status_desc = "Conditions unstable. Possible showers."
            else:
                st.success("🌤️ Stable Skies")
                status_desc = "Ideal conditions for city activity."
            st.write(f"**Insight:** {status_desc}")

        # --- ROW 2: GRAPHICAL ANALYSIS ---
        st.divider()
        st.subheader("📊 7-Day ML-Driven Predictive Trend")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Temperature (°C)'], 
                                 name='Temp (°C)', mode='lines+markers',
                                 line=dict(color=MAIN_COLOR, width=4)))
        
        fig.add_trace(go.Bar(x=df['Date'], y=df['Rain Probability (%)'], 
                             name='Rain %', marker_color=ACCENT_COLOR, opacity=0.6))

        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            hovermode="x unified",
            yaxis=dict(title="Temperature (°C)", showgrid=False),
            yaxis2=dict(title="Rain %", overlaying='y', side='right', showgrid=False, range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- ROW 3: VISUAL CONTEXT (IMAGE) ---
        st.divider()
        st.subheader(f"🖼️ Visual Context: {active_city.title()}")
        
        # Using Unsplash source for dynamic city images
        image_url = f"https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=1000&q=80" # Fallback
        # Dynamic search URL
        dynamic_img = f"https://source.unsplash.com/featured/?{active_city.replace(' ', '')},city,landscape"
        
        col_img, col_text = st.columns([2, 1])
        with col_img:
            # We use a trick to force image refresh by adding a random number to the URL
            st.image(f"{dynamic_img}&sig={random.randint(1,1000)}", 
                     caption=f"AI-Generated Snapshot for {active_city}", 
                     use_column_width=True)
        
        with col_text:
            st.info(f"**Visual Intelligence:** Integrating satellite and ground-level views allows the AI to analyze urban heat islands in {active_city}.")
            if st.button("Refresh City View"):
                st.rerun()

        # --- ROW 4: DATA TABLE ---
        with st.expander("View Raw Prediction Matrix"):
            st.dataframe(df, use_container_width=True)
