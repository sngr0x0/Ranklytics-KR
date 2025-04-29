# Korean LoL Pro Players Tier Change Analysis

This project analyzes tier changes and performance trends of Korean professional League of Legends (LoL) players over different timeframes (daily, weekly, monthly). It leverages web scraping, statistical analysis, and data visualization to provide insights into individual and team performances based on data collected from OP.GG.

## 🔍 Project Overview

The system tracks:

- LP (League Points) gains/losses
- Win rates
- Team performance trends
- Correlations between performance metrics

## 📁 Project Structure

### 1. Data Collection

Uses [Playwright](https://playwright.dev/) for web scraping:

- **Command-line Interface:** Users can select data collection intervals (daily, weekly, monthly).
- **Scraper:** Extracts player data including:
  - Player ID
  - Team affiliation
  - LP changes
  - Win rate (interval-specific)
- **Data Export:** Outputs CSV files:
  - `daily_improvement.csv`
  - `weekly_improvement.csv`
  - `monthly_improvement.csv`

### 2. Data Analysis

- **Cleaning:**
  - Standardizes team names
  - Marks unaffiliated players as "Retired"
  - Converts win rates to decimals, LP changes to integers
- **Statistical Analysis:**
  - Descriptive stats on player and team performance
  - Correlation between win rates and LP changes
- **Storage:** Stores cleaned data in an SQLite database
- **Visualization:**
  - Bar plots (team LP gains)
  - Scatter plots (win rates vs. LP changes)
  - Player performance charts (Korean character support included)

## 📊 Key Insights

- Top-performing teams by average LP gains
- Strong correlation trends between win rates and LP growth
- Identification of consistent player improvements
- Timeframe-based player rankings

## 🛠 Technologies Used

- **Python**
- **Playwright** (Web Scraping)
- **SQLite** (Data Storage)
- **Matplotlib / Seaborn** (Visualization)
- **Pandas / NumPy** (Data Processing)

## 📌 Conclusion

This project delivers a full data pipeline from web scraping to insight visualization, offering valuable perspectives on player progression and team impact in the Korean professional LoL scene.

---
