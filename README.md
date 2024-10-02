## NVIDIA Stock Price Prediction Bot Application

This project demonstrates a Stock Price Prediction Bot for NVIDIA using Machine Learning and Generative AI. It integrates stock data analysis with a linear regression model to predict future prices and utilizes a pre-trained GPT model to generate detailed stock market summaries.

🚀 Features
Stock Data Visualization: View historical stock data, technical indicators (SMA, RSI, Volatility), and closing prices.
Stock Price Prediction: Linear regression model to predict the next day's closing price.
Generative AI Insights: Leverages GPT-2 to generate detailed stock performance reports.
User-Friendly Interface: Built with Streamlit, offering an interactive interface for easy stock analysis and predictions.
🛠️ Installation
Clone the repository:
https://github.com/aayushkumbharkar/NVIDIA_STOCK_BOT

Navigate to the project directory:


cd NVIDIA-stock-price-prediction-app
Install the required dependencies:


pip install -r requirements.txt
💻 Running the Application
Launch the app with Streamlit:
streamlit run App.py
Open your browser and enter the stock ticker (e.g., NVDA) to see stock data, predictions, and AI-generated summaries.

⚙️ How It Works
Data Collection: Uses yfinance to fetch historical stock data.
Prediction Model: Implements a linear regression model using scikit-learn to predict future stock prices.
Generative AI: Utilizes Hugging Face's transformers library to generate stock summaries with GPT-2.
Visualization: Plots stock data and predictions using matplotlib.
📈 Prediction Example
The app predicts future NVIDIA stock prices and compares them to actual historical data:
Actual Prices vs Predicted Prices
🧠 AI-Generated Report Example
Here’s an example of an AI-generated stock performance report:
The stock NVDA has recently shown the following trends:
- 20-day moving average: 460.45
- 50-day moving average: 450.12
- Relative Strength Index (RSI): 62.45
🛠️ Technologies Used
Streamlit: For building the web app interface.
YFinance: To fetch stock market data.
Scikit-learn: For the linear regression prediction model.
Transformers: GPT-2 for generating AI-based stock reports.
Matplotlib: For data visualization.
🎥 Video Demo
Check out the full video demo of the project on YouTube: NVIDIA Stock Prediction Bot Demo[https://youtu.be/d1XLEF34vmc]
📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.
