# dashboard/app.py

# dashboard/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import joblib

# Ensure the app can find the 'src' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_ingestion import get_data
from src.modeling import get_forecast
from src.portfolio import optimize_portfolio
from src.backtest import run_dynamic_backtest, analyze_backtest_performance
from src.config import TICKERS, BENCHMARK_WEIGHTS, FORECAST_ASSET

# --- Page Configuration ---
st.set_page_config(
    page_title="GMF Investments | Portfolio Optimizer",
    page_icon="📈",
    layout="wide"
)

# --- Caching ---
@st.cache_data
def cached_get_data(tickers):
    """Cached function to fetch financial data to avoid repeated API calls."""
    try:
        return get_data(tickers)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

@st.cache_resource
def load_models(path_arima, path_lstm):
    """Cached function to load the trained models from disk."""
    models = {}
    if os.path.exists(path_arima):
        models['arima'] = joblib.load(path_arima)
    if os.path.exists(path_lstm):
        models['lstm'] = joblib.load(path_lstm)
    return models

# --- Main App ---
st.title("📈 GMF Investments Portfolio Optimization Dashboard")
st.write("An interactive tool to explore, forecast, and optimize financial portfolios using data-driven insights.")

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    available_tickers = set(TICKERS + ['NVDA', 'MSFT', 'GOOGL'])
    selected_tickers = st.multiselect(
        "Select Assets for Portfolio", 
        options=list(available_tickers), 
        default=TICKERS
    )
    
    if not selected_tickers:
        st.error("Please select at least one asset.")
        st.stop()
    
    # We now allow the user to select the model to use for forecasting
    selected_model_type = st.selectbox("Select Forecasting Model", options=["ARIMA", "LSTM"])

# --- Data Loading ---
data = cached_get_data(selected_tickers)
models = load_models("reports/arima_model.pkl", "reports/lstm_model.pkl")

if not models:
    st.error("Forecasting models not found. Please run the main pipeline (`make run`) to train and save the models.")
    st.stop()

# Get the selected model
selected_model = models.get(selected_model_type.lower())
if not selected_model:
    st.warning(f"{selected_model_type} model not available. Using ARIMA instead.")
    selected_model = models.get('arima')
    
# --- UI Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Explorer", "🔮 Forecasting", "⚖️ Portfolio Optimization", "⏪ Backtesting"])

with tab1:
    st.header("Historical Price Data Explorer")
    st.dataframe(data.tail(), use_container_width=True)
    fig = px.line(data, title="Historical Adjusted Close Prices", labels={"value": "Price (USD)", "variable": "Ticker"})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header(f"{selected_model_type} Forecast for {FORECAST_ASSET}")
    
    if selected_model:
        # We use the pre-trained model on the selected asset's data for forecasting
        annual_return, forecast, conf_int = get_forecast(selected_model, data[FORECAST_ASSET])
        
        plot_data = pd.concat([data[FORECAST_ASSET]['2023':], forecast], axis=1)
        plot_data.columns = ['Historical', 'Forecast']
        
        fig = px.line(plot_data, title=f"1-Year Forecast for {FORECAST_ASSET}")
        fig.add_scatter(x=conf_int.index, y=conf_int['upper'], fill='tonexty', fillcolor='rgba(0,176,246,0.2)', line_color='rgba(255,255,255,0)', name='95% Confidence')
        fig.add_scatter(x=conf_int.index, y=conf_int['lower'], fill='tonexty', fillcolor='rgba(0,176,246,0.2)', line_color='rgba(255,255,255,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Model-Forecasted Annual Return", f"{annual_return:.2%}")
    else:
        st.error("Forecasting model not found. Please run the main pipeline to train and save the models.")

with tab3:
    st.header("Modern Portfolio Theory Optimization")
    if 'annual_return' in locals():
        weights, ef = optimize_portfolio(data, annual_return, FORECAST_ASSET)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Optimal Portfolio Weights")
            st.dataframe(pd.Series(weights).to_frame('Weight').style.format('{:.1%}'))
        
        with col2:
            st.subheader("Expected Portfolio Performance")
            perf = ef.portfolio_performance(verbose=False)
            st.metric("Expected Annual Return", f"{perf[0]:.2%}")
            st.metric("Annual Volatility (Risk)", f"{perf[1]:.2%}")
            st.metric("Sharpe Ratio", f"{perf[2]:.2f}")
    else:
        st.warning("Run the forecast first to enable optimization.")

with tab4:
    st.header("Dynamic Strategy Backtesting")
    # This tab is completely revised to use the new rolling backtest function.
    if 'selected_model' in locals():
        rebalance_freq = st.radio(
            "Select Rebalancing Frequency", 
            ('D', 'W', 'M'), 
            index=2, 
            horizontal=True, 
            help="D=Daily, W=Weekly, M=Monthly"
        )
        
        with st.spinner('Running dynamic backtest...'):
            cumulative_returns = run_dynamic_backtest(
                data, 
                selected_model, 
                rebalance_freq, 
                BENCHMARK_WEIGHTS
            )
            
            st.subheader("Performance: Strategy vs. Benchmark")
            fig = px.line(
                cumulative_returns, 
                title="Cumulative Growth of $1", 
                labels={"value": "Portfolio Value", "variable": "Portfolio"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Performance Metrics")
            metrics = analyze_backtest_performance(cumulative_returns)
            st.dataframe(pd.DataFrame(metrics).T)
    else:
        st.warning("Forecasting model not available. Please run the pipeline first.")