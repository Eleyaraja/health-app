# BAT Health AI - Advanced Nutritional Analysis 🍏

BAT Health AI is an advanced food analysis tool powered by Google Gemini AI. It provides detailed nutritional insights from food images, including calorie estimates, macronutrient breakdowns, and dietary recommendations.

## 🚀 Features
- 📷 **AI-Powered Food Analysis**: Upload food images and get a detailed breakdown.
- 📊 **Nutritional Insights**: Calories, macronutrients, and health scores.
- 💬 **Chat Interface**: Ask follow-up questions about your meal.
- 🎯 **Dietary Preferences**: Customize results for Vegan, Keto, Low-Carb, and more.
- 🔍 **Interactive Data Visualizations**: View macronutrient charts and health scores.

## 🛠️ Installation

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/bat-health-ai.git
cd bat-health-ai
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```sh
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file and add your Google Gemini API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## ▶️ Usage
Run the Streamlit app:
```sh
streamlit run bat_health.py
```

## 🖼️ Example
Upload a food image and receive:
```json
{
    "food_analysis": {
        "items": [
            {
                "name": "Apple",
                "quantity": "1 medium",
                "calories": "95 kcal",
                "proteins": "0.5 g",
                "carbs": "25 g",
                "fats": "0.3 g",
                "health_score": 9,
                "allergens": [],
                "micronutrients": ["Vitamin C", "Fiber"]
            }
        ],
        "total_calories": "95 kcal",
        "overall_health_score": 9,
        "dietary_recommendations": ["Great for a healthy snack!"]
    }
}
```

## 📌 Contribution
Contributions are welcome! Feel free to submit issues or pull requests.

## 🛡️ License
This project is licensed under the MIT License.

---
### 🌟 Show Your Support
⭐ Star this repo if you found it useful!

