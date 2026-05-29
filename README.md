# Health-Insurance-Cost-Prediction-and-Affordability-Analysis-Using-Machine-Learning
An AI-powered system that predicts health insurance costs and recommends affordable plans using machine learning.
# Smart Health Insurance Cost Analyzer and Recommendation System

## Overview
The Smart Health Insurance Cost Analyzer and Recommendation System is a Machine Learning-based application designed to predict health insurance premiums and recommend the most suitable insurance plan based on affordability and user health conditions. The system helps users make informed decisions by analyzing insurance costs, financial affordability, and health risk factors.

## One-Line Description
**An AI-powered system that predicts health insurance costs and recommends affordable insurance plans using machine learning.**

## Features
- Health insurance premium prediction using Machine Learning
- Smart insurance plan recommendation
- Insurance affordability analysis based on income
- Risk assessment using BMI and smoking status
- Multiple insurance plan comparison (Basic, Standard, Premium)
- Monthly, yearly, and total cost calculation
- Interactive dashboard with charts and insights
- User-friendly interface built with Streamlit

## Technologies Used
- **Programming Language:** Python  
- **Framework:** Streamlit  
- **Machine Learning:** Scikit-learn  
- **Data Processing:** Pandas, NumPy  
- **Model Saving:** Pickle  

## Machine Learning Models Used
- Linear Regression
- Support Vector Regression (SVR)

## Dataset Features
The model predicts insurance cost using the following parameters:

- Age  
- Gender  
- BMI (Body Mass Index)  
- Number of Children  
- Smoking Status  
- Region  

## Project Structure

```text
Smart-Health-Insurance-System/
│── app.py
│── insurance.csv
│── insurance1.ipynb
│── lr_model.pkl
│── svr_model.pkl
│── y_scaler.pkl
│── README.md
```

## Installation and Setup

### 1. Clone the Repository
```bash
git clone <your-github-repository-link>
cd Smart-Health-Insurance-System
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

## How the System Works
1. Enter personal details such as age, BMI, and gender.  
2. Provide health-related information like smoking status and number of children.  
3. Enter salary details and choose an insurance plan.  
4. The system predicts insurance costs using trained ML models.  
5. Compare different plans and receive a smart recommendation.  
6. View affordability analysis and health risk insights.

## Key Benefits
- Helps users estimate insurance premiums quickly  
- Suggests affordable plans based on income  
- Provides health risk analysis  
- Supports financial planning for medical expenses  

## Future Enhancements
- Integration with real insurance providers  
- More accurate prediction models  
- User authentication system  
- PDF report generation  
- Cloud database integration  

## Applications
- Health insurance premium estimation  
- Smart healthcare financial planning  
- Insurance decision support system  

## Author
**Zack**

## License
This project is developed for educational and academic purposes.
