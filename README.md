# Firewall and IDS Log Analysis

**VAST 2012 Mini-Challenge 2** 

**University of Luxembourg** 

Team Members: 

- Parsa Vares, University of Luxembourg, [parsa.vares.001@student.uni.lu](mailto:parsa.vares.001@student.uni.lu)
- Daniele Ferrario, University of Luxembourg, [daniele.ferrario.001@student.uni.lu](mailto:daniele.ferrario.001@student.uni.lu)
- Giorgio Bettonte, University of Luxembourg, [giorgio.bettonte.001@student.uni.lu](mailto:giorgio.bettonte.001@student.uni.lu)
- Yufei Wei, University of Luxembourg, [yufei.wei.001@student.uni.lu](mailto:yufei.wei.001@student.uni.lu)

## Project Overview
This project addresses Mini-Challenge 2 from the VAST 2012 competition by developing a visual analytics tool for analyzing firewall and IDS logs. The dataset consists of raw logs collected from a corporate network to investigate security concerns, identify trends, and uncover anomalous behavior. We utilized a combination of **React**, **D3.js**, **JavaScript**, and **Python** to create an interactive visual tool that assists with the security analysis process.

The main goal of this project is to enable visual exploration of security events, detect suspicious activities, and identify underlying trends using effective data visualizations.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Datasets](#datasets)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Installation and Setup](#installation-and-setup)
6. [Setup with Yarn](Setup_with_Yarn)
7. [Python Dashboard Setup Instructions](Python_Dashboard_Setup_Instructions)
8. [Usage Instructions](#usage-instructions)
9. [Analysis Approach](#analysis-approach)
10. [Visual Analytics and Key Insights](#visual-analytics-and-key-insights)
11. [Mini-Challenge Answers](#mini-challenge-answers)
12. [Contributing](#contributing)

## Project Structure
```
firewall-ids-log-analysis/
|
├── public/                       
│   ├── favicon.ico
│   ├── index.html              # Start page
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   ├── robots.txt
|
├── src/                        # Frontend code for visualization
│   ├── App.js
│   ├── App.css
│   ├── App.test.js
│   ├── index.css
│   ├── index.js
│   ├── logo.svg
│   ├── reportWebVitals.js
│   ├── setupTests.js
│   ├── store.js
│   ├── pages
│       ├── DashboardPage.js
│       ├── FerraPage.js
│       ├── GiorgioPage.js
│       ├── ParsaPage.js
│       ├── YufeiPage.js
│   ├── redux
│       ├── DatasetSlice.js
│   ├── components
│       ├── Heatmap
│           ├── HeatmapContainer.js
│           ├── HeatmapD3.js
│           ├── generate_data.js
│           ├── heatmap_data.csv
│       ├── ParallelSets
│           ├── ParallelSetsContainer.js
│           ├── ParallelSetsD3.js
│       ├── StackedBarchart
│           ├── StackedBarchartContainer.js
│           ├── StackedBarchartD3.js
|
├── scripts/                    # Python scripts for data analysis
│   ├── analysis_summaries
│       ├── top_20_external_ips.csv
│       ├── top_50_destination_ports.csv
│       ├── top_50_destination_services.csv
│   ├── DataProcessing.py
│   ├── GeoLite2-City.mmdb
│   ├── Patterns.py
|   ├── Patterns2-out.txt
│   ├── Patterns2.py
│   ├── dashboard.py
│   ├── dataset_analysis.py
│   ├── dataset_summary.txt
│   ├── firewall_stats.py
│   ├── ids_stats.py
│   ├── new_analysis.py
│   ├── query.py
│   ├── refine_data.py
│   ├── test-post-cleaning.py
│   ├── test.py
|
├── server/                    
│   ├── __pycache__
│       ├── data_handler.cpython-39.pyc
│       ├── heatmap.cpython-39.pyc
│       ├── stacked_barchart.cpython-39.pyc
│       ├── utils.cpython-39.pyc
│   ├── data_handler.py
│   ├── heatmap.py
│   ├── parallel_sets.py
│   ├── server.py
│   ├── stacked_barchart.py
│   ├── utils.py
|
├── README.md                   # Description and setup instructions
├── package-lock.json
├── package.json
├── records
└── stats.txt                   # Statistics
```

## Datasets
- **Firewall Logs**: These logs contain details about network activities, such as source and destination IP addresses, ports, protocols, and operations (e.g., connection built/teardown). 
- **IDS Logs**: These logs capture suspicious network behaviors and generate alerts with important packet information and security classifications. Fields include source/destination IP, packet details, priority, and classification labels.

The data covers a specific timeframe and is instrumental in identifying suspicious activities, intrusion attempts, and general traffic behavior.

## Features
1. **Configuration Setup**: Define paths to datasets and the output summary file.
2. **Data Cleaning**: Replace empty fields with NaN, removing duplicates, etc.
3. **Data Transformation**: Transform logs to make them suitable for visualization, including checking errors, changing data and time format, refining columns for final output.
4. **Interactive Dashboard**: A React-based dashboard providing:
   - **Heatmaps** to analyze the frequency of connections and events.
   - **Network Graphs** to visualize communication patterns between different IP addresses.
   - **Bar Charts** for the frequency of message codes and classification labels.
5. **Event Filtering and Detection**: Identify the five most notable events based on frequency and priority, and apply filters to isolate specific times, IPs, or protocols.
6. **Security Trend Analysis**: Using visual analytics, observe trends over the two-day period to identify patterns such as potential denial-of-service attacks or repeated suspicious activity.

## Technologies Used
- **Frontend**: React, D3.js, JavaScript.
- **Backend/Analysis**: Python, Dask, Matplotlib, Pandas, Plotly, Seaborn.
- **Visualization Dashboard**: React with D3.js components for interactive visualizations.

## Installation and Setup
1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/firewall-ids-log-analysis.git
    cd firewall-ids-log-analysis
    ```
2. **Install Python Requirements**:
    ```sh
    pip install -r requirements.txt
    ```
3. **Install Frontend Dependencies**:
    ```sh
    cd src
    npm install
    ```
4. **Run the Analysis Scripts**:
    - Use the Python scripts in the `analysis` directory to clean and preprocess the data.
    ```sh
    python analysis/data_cleaning.py
    ```
5. **Run the Application**:
    ```sh
    npm start
    ```
    The application will be accessible at `http://localhost:3000`.
   
## Setup with Yarn

To install dependencies and run the project using Yarn, follow these steps:

1. **Install Yarn** (if not already installed):
   ```bash
   npm install -g yarn
   ```

2. **Install dependencies**:
   Navigate to the project directory and run:
   ```bash
   yarn install
   ```

3. **Start the application**:
   Run the application (replace `yarn start` with the actual start command for your project):
   ```bash
   yarn start
   ```

4. **Other useful Yarn commands**:
   - Build the project for production:
     ```bash
     yarn build
     ```
   - Run tests:
     ```bash
     yarn test
     ```

For more information on using Yarn, visit the [official Yarn documentation](https://yarnpkg.com/).

---

## **Python Dashboard Setup Instructions**

---

#### **Installation and Setup**

To run the Python Plotly Dashboard, follow these simple instructions:

---

#### **1. Prerequisites**

Ensure you have **Python 3.8 or later** installed on your system. Check your Python version with:
```bash
python --version
```

---

#### **2. Required Python Packages**

To install the required Python libraries, run the following command:
```bash
pip install pandas dask numpy plotly dash geoip2
```

This command installs the following essential libraries:
- **pandas**: Data manipulation and analysis.
- **dask**: Parallel computing for large datasets.
- **numpy**: Numerical computations.
- **plotly**: For creating interactive plots and charts.
- **dash**: For creating web-based interactive dashboards.
- **geoip2**: For IP location lookup.

---

#### **3. Run the Preprocessing Scripts**

The following scripts must be executed **in order** to prepare and process the data before launching the dashboard. 

Run each of the following scripts from the **scripts** directory using Python:
```bash
cd scripts
```

1. **Run the Dataset Analysis**:
    ```bash
    python dataset_analysis.py
    ```

2. **Run the Patterns Detection (Phase 1)**:
    ```bash
    python Patterns.py
    ```

3. **Run the Patterns Detection (Phase 2)**:
    ```bash
    python Patterns2.py
    ```

4. **Run Data Processing and Cleaning**:
    ```bash
    python DataProcessing.py
    ```

These scripts process, clean, and generate intermediate summary files. You will see outputs like:
```
[INFO] Successfully loaded and cleaned 2 firewall files.
[INFO] Successfully loaded and cleaned 2 IDS files.
[INFO] Exported top_50_destination_services.csv with top 24696 entries.
[INFO] Exported top_50_destination_ports.csv with top 24696 entries.
[INFO] Exported top_50_external_ips.csv with top 95 entries.
[INFO] Exported external_firewall_traffic.csv.
[INFO] Exported external_ids_traffic.csv.
[INFO] Data processing complete.
```

Once you see this output, you're ready to run the dashboard.

---

#### **4. Run the Dashboard**

Run the dashboard by executing the following command in the **scripts** directory:
```bash
python dashboard.py
```

If everything is successful, you will see an output similar to:
```
Dash is running on http://127.0.0.1:8050/
```

Open your web browser and navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to see the live dashboard.

---

### **Dashboard Overview**

The dashboard has **4 key sections**, each designed to answer one of the 4 primary questions related to security analysis.

---

#### **1️⃣ Question 1: Critical Security Events**

**Charts:**
- **Sunburst Chart**: Displays the classification and priority of top 5 critical IDS events.
- **Treemap**: Visualizes the top sources of external attacks.

**Usage:**
- Identify and analyze critical events flagged in the IDS logs.
- View which IP addresses are generating the most alerts.

---

#### **2️⃣ Question 2: Security Trends**

**Charts:**
- **Line Chart**: Shows the number of connections built over time in the firewall.
- **Line Chart**: Displays the IDS alert counts over time.

**Usage:**
- Identify key time periods with abnormal spikes in connections or IDS alerts.
- Detect and analyze patterns of network activity and security events.

---

#### **3️⃣ Question 3: Root Cause Analysis**

**Charts:**
- **Scatter Plot**: Shows the frequency and distribution of ports that were most frequently used, helping to identify potential vulnerabilities.
- **Scatter Plot**: Plots Source IP vs Destination IP for network attack tracing.

**Usage:**
- Detect abnormal use of ports and connections that may indicate potential exploits.
- Trace the source-destination interactions that might reveal suspicious IP behavior.

---

#### **4️⃣ Hybrid Analysis (Combined Firewall + IDS)**

**Charts:**
- **Interactive Scatter Plot**: Combines **IDS and Firewall** source IPs and destination IPs in one chart.

**Usage:**
- View how Source IPs and Destination IPs from both IDS and Firewall logs relate.
- Identify network flows and locate malicious IPs across both log sources.
- Highlight which IPs might be involved in multiple attack vectors.

---

## Usage Instructions
1. **Load the Data**: Once the app is running, use the provided interface to load the cleaned data files.
2. **Explore the Dashboard**: Use the filters to explore the connections between IP addresses, notable event occurrences, and overall traffic behavior.
3. **Analyze Events**: Identify anomalies, perform detailed inspections of repeated connections, and highlight any high-priority security concerns.

## Analysis Approach
- **Data Cleaning**: We started by removing unnecessary columns, handling missing values, and standardizing date-time formats.
- **Visualization Design**:
  - Chose **heatmaps** to show time-based event frequency, allowing an overview of connection surges.
  - Used **network graphs** for mapping IP interactions and identifying unusual communication.
  - Developed **bar charts** to represent the distribution of different log classifications, helping detect prevalent issues.
- **Anomaly Detection**: Focused on detecting repeated teardown/rebuild of connections, and identifying suspicious IPs from IDS alerts.

## Visual Analytics and Key Insights
1. **Noteworthy Events** (MC2.1):
   - Using the visualizations, we identified five notable events such as repeated attempts to access critical servers and network traffic spikes that align with potential denial-of-service.
2. **Security Trends** (MC2.2):
   - A distinct trend of repeated teardown and rebuild requests, suggesting potential service interruptions or attacks, was visualized using time-based heatmaps.
3. **Root Cause and Mitigation** (MC2.3):
   - The root cause appears to be unauthorized access attempts, especially targeting port `445` (commonly associated with SMB). Mitigation recommendations include stricter access control, improved network segmentation, and setting up alerts for repeated teardown events.

## Mini-Challenge Answers
1. **MC 2.1 - Noteworthy Events**: 
   - Screenshots and detailed descriptions of five critical events are included in the `index.html` file.
2. **MC 2.2 - Security Trend**: 
   - Observed trend of repeated teardown/rebuild illustrated with a **time-series line chart**.
3. **MC 2.3 - Root Causes and Mitigation**: 
   - Recommendations include blocking suspicious IPs, restricting access to vulnerable ports, and increasing the sensitivity of IDS alerts.

## Contributing
We welcome contributions from the community! Please feel free to submit a pull request or open an issue if you have suggestions or find a bug.

To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---
Thank you for checking out our project! We hope this tool provides valuable insights and helps highlight network security concerns effectively.
