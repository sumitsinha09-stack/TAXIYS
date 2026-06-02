# TAXISYS (Greek for *Organized System*)

[![Python Flask](https://img.shields.io/badge/Backend-Flask-darkgreen.svg?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Express.js](https://img.shields.io/badge/Backend-Express.js-black.svg?style=for-the-badge&logo=express)](https://expressjs.com/)
[![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-orange.svg?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![Chart.js](https://img.shields.io/badge/Frontend-Chart.js-lightgrey.svg?style=for-the-badge&logo=chartdotjs)](https://www.chartjs.org/)

**TAXISYS** is an advanced, web-based platform designed to close the gap between manual data entry and intelligent data analysis. Using a sleek, responsive interface, TAXISYS allows users to input, manage, compare, and analyze investor records. Furthermore, it leverages a trained **Machine Learning** classifier to automatically predict trends and recommend stock/investment paths based on the submitted data.

---

## 🌟 Core Features

- **📊 Dynamic Investor Form**: Standardized structured fields including Name, Age, Salary, Position, Years of Experience (YOE), Bonus %, and Investment Expertise.
- **📈 Machine Learning Stock Predictor**: Runs all current records through a pipeline consisting of a preprocessor (`preprocessor.pkl`) and a trained classifier (`stock_predictor.pkl`) to identify positive trends.
- **⚙️ Full CRUD Operations**: Seamlessly **Add**, **Fetch**, **Update**, and **Delete** records directly from the sidebar.
- **⚡ Real-Time Spreadsheet View**: Renders the complete, live-updated spreadsheet instantly on the right panel using AJAX.
- **👥 Advanced Comparison Engine**: Select multiple investors to generate visual numeric comparisons, expertise breakdowns, and job position distributions using dynamic **Chart.js** canvases.
- **🔗 Microservices Architecture**: Includes a supplementary Node.js Express service for developer sandboxing and task validation.

---

## 🏗️ Project Architecture

```mermaid
graph TD
    User([User Browser]) -->|HTTP Requests / AJAX| Flask[Flask Server :5001]
    User -->|API Requests| Express[Express Server :3000]
    
    subgraph killerjack (Main Application)
        Flask -->|Load / Save| CSV[(data.csv)]
        Flask -->|Pipeline Input| Preprocessor[preprocessor.pkl]
        Preprocessor -->|Transformed Data| Model[stock_predictor.pkl]
        Model -->|Stock Predictions| Flask
        Flask -->|Render Template| Frontend[HTML/CSS + Chart.js]
    end
    
    subgraph backend-test (Test API Service)
        Express -->|In-Memory Store| Tasks[(Tasks Array)]
    end
```

---

## 💻 Tech Stack

### Main Application (`killerjack`)
- **Backend**: Flask (Python)
- **Data Engine**: Pandas
- **Machine Learning**: Scikit-Learn, Joblib
- **Frontend**: Vanilla HTML5, Premium CSS3 Custom Styles
- **Visualization**: Chart.js

### Auxiliary Test API (`backend-test`)
- **Runtime**: Node.js
- **Framework**: Express.js

---

## 🚀 How to Run Locally

### 1. Prerequisite Checks
Make sure you have Python 3.9+ and Node.js installed on your machine.

---

### 2. Launching TAXISYS Main App (`killerjack`)

The application is bundled with a pre-configured Python virtual environment (`.venv`) at the root.

1. **Navigate to the app folder**:
   ```bash
   cd killerjack
   ```

2. **Activate the virtual environment**:
   ```bash
   source ../.venv/bin/activate
   ```

3. **Install python packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Flask web server**:
   *Note: On macOS, Port `5000` is often reserved by AirPlay. Start the application on Port `5001` or another vacant port using the `PORT` environment variable:*
   ```bash
   PORT=5001 python app.py
   ```
5. **Open in browser**: Access the dashboard at **[http://localhost:5001](http://localhost:5001)**.

---

### 3. Launching Test Express Service (`backend-test`)

If you want to run the supplementary Task API service in parallel:

1. **Navigate to the test backend directory**:
   ```bash
   cd ../backend-test
   ```

2. **Install Node packages**:
   ```bash
   npm install
   ```

3. **Start the server**:
   ```bash
   node index.js
   ```
4. **Open in browser**: The API will be active at **[http://localhost:3000](http://localhost:3000)**.

---

## 📂 Directory Structure

```text
TAXISYS/
├── .venv/                     # Python Virtual Environment
├── killerjack/                # Main Application
│   ├── app.py                 # Flask server core logic & routes
│   ├── requirements.txt       # Python dependencies list
│   ├── data.csv               # Local database spreadsheet
│   ├── model.pkl              # Primary serialized classifier
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── index.html         # Main dashboard page
│   │   └── analyze.html       # ML results helper view
│   ├── static/                # Static assets (stylesheets, JS)
│   └── model/
│       └── saved/
│           ├── preprocessor.pkl      # Serialized scikit-learn preprocessor
│           └── stock_predictor.pkl   # Serialized stock predictor classifier
└── backend-test/              # Express JS test backend
    ├── index.js               # Express app routes and listener
    └── package.json           # Node.js dependencies configuration
```

---

## 📄 License
This project is licensed under the ISC License. Organized systems for better, intelligent spreadsheets.
