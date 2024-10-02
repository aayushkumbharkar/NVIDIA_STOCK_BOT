import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from transformers import pipeline  # For using a pre-trained GPT model

# Streamlit App Title
st.title("Stock Price Prediction and Generative AI Insights")

# Input from user
ticker = st.text_input("Enter Stock Ticker Symbol", value="NVDA")

# Define possible questions
questions = [
    "Show Stock Data",
    "Display Technical Indicators",
    "Predict Future Prices",
    "Compare with Another Stock",
    "Show Model Accuracy",
    "Generate Stock Report"  # New option for Generative AI
]

# Let user select a question
selected_question = st.selectbox("Select a Question to Ask", questions)

# Function to load and preprocess data
@st.cache_data  # Cache the data loading
def load_data(ticker):
    stock_data = yf.Ticker(ticker)
    df = stock_data.history(period="max")
    # Feature Engineering
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['Daily_Returns'] = df['Close'].pct_change()
    df['Volatility'] = df['Daily_Returns'].rolling(window=30).std() * np.sqrt(30)
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)
    return df

# Load stock data
df = load_data(ticker)

# Generative AI: Load pre-trained model for text generation (like GPT)
@st.cache_resource  # Cache the model loading
def load_generative_model():
    return pipeline('text-generation', model='gpt2')

generative_model = load_generative_model()

# Handle different questions
if selected_question == "Show Stock Data":
    st.subheader(f"Displaying Stock Data for {ticker}")
    st.write(df.tail())

elif selected_question == "Display Technical Indicators":
    st.subheader(f"{ticker} Technical Indicators")
    sma_window1 = st.slider("Select window size for SMA 1", min_value=10, max_value=100, value=20, step=5)
    sma_window2 = st.slider("Select window size for SMA 2", min_value=10, max_value=200, value=50, step=10)

    df['SMA_Custom1'] = df['Close'].rolling(window=sma_window1).mean()
    df['SMA_Custom2'] = df['Close'].rolling(window=sma_window2).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['Close'], label='Close Price', color='blue')
    ax.plot(df['SMA_Custom1'], label=f'{sma_window1}-day SMA', color='green')
    ax.plot(df['SMA_Custom2'], label=f'{sma_window2}-day SMA', color='orange')
    ax.legend()
    st.pyplot(fig)

    st.write("### Relative Strength Index (RSI)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['RSI'], label='RSI', color='purple')
    ax.axhline(70, linestyle='--', color='red')  # Overbought
    ax.axhline(30, linestyle='--', color='green')  # Oversold
    ax.legend()
    st.pyplot(fig)

elif selected_question == "Predict Future Prices":
    st.subheader(f"{ticker} Stock Price Prediction Model")
    X = df[['Close']]
    y = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    st.subheader(f"Actual vs Predicted Close Prices for {ticker}")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(y_test.values, label='Actual Prices', color='blue')
    ax.plot(predictions, label='Predicted Prices', color='orange')
    ax.legend()
    st.pyplot(fig)

elif selected_question == "Compare with Another Stock":
    st.subheader(f"Compare {ticker} with Another Stock")
    comparison_ticker = st.text_input("Enter Comparison Stock Ticker Symbol", value="AMD")
    if comparison_ticker:
        comparison_df = load_data(comparison_ticker)
        df['Comparison_Close'] = comparison_df['Close']

        combined_df = pd.concat([df['Close'], df['Comparison_Close']], axis=1)
        st.write(combined_df.tail())

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df['Close'], label=f'{ticker} Close Price', color='blue')
        ax.plot(df['Comparison_Close'], label=f'{comparison_ticker} Close Price', color='orange')
        ax.legend()
        st.pyplot(fig)

elif selected_question == "Show Model Accuracy":
    st.subheader(f"{ticker} Model Accuracy")
    st.write("Model R² score:", model.score(X_test, y_test))

elif selected_question == "Generate Stock Report":
    st.subheader(f"{ticker} Generative AI Stock Report")

    summary_prompt = (
        f"The stock {ticker} has recently shown the following trends:\n"
        f"- 20-day moving average: {df['SMA_20'].iloc[-1]:.2f}\n"
        f"- 50-day moving average: {df['SMA_50'].iloc[-1]:.2f}\n"
        f"- Relative Strength Index (RSI): {df['RSI'].iloc[-1]:.2f}\n"
        f"- Daily volatility: {df['Volatility'].iloc[-1]:.2f}\n"
        "Write a detailed report on the stock's performance and expected trends."
    )

    report = generative_model(summary_prompt, max_length=300)[0]['generated_text']
    st.write(report)
