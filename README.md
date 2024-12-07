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
6. [Usage Instructions](#usage-instructions)
7. [Analysis Approach](#analysis-approach)
8. [Visual Analytics and Key Insights](#visual-analytics-and-key-insights)
9. [Mini-Challenge Answers](#mini-challenge-answers)
10. [Contributing](#contributing)

## Project Structure
```
firewall-ids-log-analysis/
|
├── data/                       # Raw and cleaned dataset files (CSV, XLSX)
│   ├── firewall-04062012.csv
│   ├── ids-04062012.csv
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
|
├── analysis/                   # Python scripts for data analysis
│   ├── data_cleaning.py
│   ├── event_detection.py
│   ├── trends_analysis.py
|
├── static/                     # Static files for visualizations
│   ├── images/
│       ├── notable_events_1.png
│       ├── notable_events_2.png
|
├── index.html                  # Main submission file
├── README.md                   # Description and setup instructions
├── package-lock.json
├── package.json
└── stats.txt   
```

## Datasets
- **Firewall Logs**: These logs contain details about network activities, such as source and destination IP addresses, ports, protocols, and operations (e.g., connection built/teardown). 
- **IDS Logs**: These logs capture suspicious network behaviors and generate alerts with important packet information and security classifications. Fields include source/destination IP, packet details, priority, and classification labels.

The data covers a specific timeframe and is instrumental in identifying suspicious activities, intrusion attempts, and general traffic behavior.

## Features
1. **Data Cleaning and Transformation**: Python scripts in the `analysis` folder clean and preprocess the logs to make them suitable for visualization.
2. **Interactive Dashboard**: A React-based dashboard providing:
   - **Heatmaps** to analyze the frequency of connections and events.
   - **Network Graphs** to visualize communication patterns between different IP addresses.
   - **Bar Charts** for the frequency of message codes and classification labels.
3. **Event Filtering and Detection**: Identify the five most notable events based on frequency and priority, and apply filters to isolate specific times, IPs, or protocols.
4. **Security Trend Analysis**: Using visual analytics, observe trends over the two-day period to identify patterns such as potential denial-of-service attacks or repeated suspicious activity.

## Technologies Used
- **Frontend**: React, D3.js, JavaScript.
- **Backend/Analysis**: Python, Pandas, Matplotlib.
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
