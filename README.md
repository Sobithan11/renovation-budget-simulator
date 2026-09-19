# 🏠 Renovation Budget Risk & Planning Simulator

A full-stack web application for estimating renovation costs using **Monte Carlo simulation**. Instead of producing a single fixed estimate, the simulator models uncertainty in renovation costs and generates a range of possible outcomes, helping users understand both expected costs and financial risk.

## 🌐 Live Demo

[Open the live application](https://renovation-budget-simulator-1.onrender.com)

## ✨ Features

* 🏗️ Create and manage renovation projects
* 💷 Define renovation requirements including:

  * Extension size
  * Kitchen specification
  * Bathroom specification
  * Flooring area
  * Painting area
  * Landscaping area
  * Electrical work
  * Plumbing work
  * Plastering work
  * Windows and doors
* 🎲 Run **10,000 Monte Carlo simulations** for each project
* 📊 Calculate:

  * Mean estimated cost
  * Median estimated cost
  * P10 estimate
  * P90 estimate
  * Probability of exceeding the budget
  * Probability of remaining within budget
* 📈 Visualise simulated cost distributions
* 💰 View cost breakdowns by renovation category
* 🔄 Create and compare alternative renovation scenarios
* ✅ Validate project inputs and API requests
* 💾 Persist renovation projects using SQLite
* 🌐 REST API built with Flask
* 🧪 Automated backend testing with pytest

---

## 🎲 How It Works

The simulator uses probability distributions to represent the uncertainty associated with different renovation costs.

For example, rather than assuming that an extension will always cost one fixed amount per square metre, the model samples a cost from a **triangular distribution** defined by:

* **Minimum cost**
* **Typical cost**
* **Maximum cost**

For each simulation, the application independently samples the relevant costs for the selected renovation work and calculates a total project cost.

This process is repeated **10,000 times** to produce a distribution of possible project costs.

The resulting distribution is then used to calculate statistical measures such as the median, P10 and P90 estimates, as well as the probability that the project exceeds its specified budget.

---

## 🛠️ Technology Stack

### Frontend

* Vue
* TypeScript
* Vue Router
* Chart.js
* vue-chartjs
* HTML/CSS

### Backend

* Python
* Flask
* NumPy
* SQLite
* pytest

---

## 🚀 Running Locally

### Prerequisites

Make sure the following are installed:

* Python 3.13+
* Node.js
* npm

### Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask server:

```bash
python app.py
```

### Frontend

Open another terminal and navigate to the frontend:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Start the Vue development server:

```bash
npm run dev
```

The frontend will then be available through the local development URL provided by Vite.

---

## 🧪 Testing

The backend includes automated tests covering the cost model, Monte Carlo simulation, result calculations and API validation.

From the `backend` directory, activate the virtual environment and run:

```bash
pytest
```

The test suite verifies functionality including:

* Cost generation
* Renovation cost calculations
* Monte Carlo simulation results
* Statistical calculations
* API validation
* Invalid input handling
* Negative values
* Invalid renovation specifications
* API responses

---

## 🌐 API

The Flask backend provides REST endpoints for managing projects and running simulations.

### Projects

Project endpoints allow the frontend to:

* Create projects
* Retrieve saved projects
* Retrieve individual projects
* Delete projects
* Run simulations for saved projects

### Simulation

The simulation endpoint accepts renovation project information, validates the input and runs the Monte Carlo simulation.

The API returns the calculated statistical results and cost breakdown required by the frontend dashboard.

---

## 📊 Statistical Outputs

The simulator produces several measures to describe the simulated cost distribution.

### Mean

The arithmetic average of all simulated project costs.

### Median

The middle value of the simulated distribution.

### P10

A lower-end estimate representing the **10th percentile** of simulated costs.

### P90

A higher-end estimate representing the **90th percentile** of simulated costs.

### Budget Risk

The proportion of simulations where the simulated project cost exceeds the user's specified budget.

Together, these measures provide more information about potential renovation costs than a single deterministic estimate.

---

## 🔄 Scenario Analysis

The scenario system allows users to modify project assumptions and compare alternative renovation plans.

For example, users can change:

* Project budget
* Extension size
* Kitchen specification
* Bathroom specification
* Flooring area
* Painting area
* Landscaping area

Each scenario is simulated independently, allowing users to compare the resulting cost estimates and budget risk.

---

## 💷 Cost Modelling

Renovation cost assumptions are stored separately from the application logic in:

```text
backend/data/cost_data.json
```

This allows cost assumptions to be modified without changing the underlying simulation implementation.

The model supports different pricing structures including:

* Fixed project costs
* Cost per square metre
* Cost per item

Triangular probability distributions are used to model uncertainty using minimum, typical and maximum values.

---

## ✅ Validation

Input validation is performed by the Flask API before simulations are executed.

Examples of validated inputs include:

* Project name
* Budget
* Area measurements
* Number of windows and doors
* Renovation specification options
* Boolean renovation requirements

Invalid inputs return appropriate API errors rather than being passed to the simulation engine.

---

## 🎯 Development Goals

The project was designed to demonstrate practical full-stack development alongside probabilistic modelling.

Key areas demonstrated include:

* Full-stack web development
* REST API development
* Database persistence
* Statistical modelling
* Monte Carlo simulation
* Data visualisation
* Input validation
* Automated testing
* Frontend/backend integration
* Scenario analysis
