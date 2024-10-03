# Flight Data Collection and Simulation

This project includes two main Python scripts:

- **Flight Data Collector**: Collects real-time flight data from the OpenSky API and saves it in a CSV file.
- **Flight Simulation Dashboard**: Visualizes the collected flight data on an interactive map using Dash and Plotly.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
  - [Step 1: Create a Conda Environment](#step-1-create-a-conda-environment)
  - [Step 2: Install Required Libraries](#step-2-install-required-libraries)
- [Usage](#usage)
  - [Running the Flight Data Collector](#running-the-flight-data-collector)
  - [Running the Flight Simulation Dashboard](#running-the-flight-simulation-dashboard)
- [File Structure](#file-structure)
- [Code Explanation](#code-explanation)
  - [Flight Data Collector](#flight-data-collector)
  - [Flight Simulation Dashboard](#flight-simulation-dashboard)

## Overview

This project is designed to:

- Collect real-time flight data from the OpenSky API.
- Simulate and visualize flights using an interactive map.

### Features:

- **Flight Data Collection**: Retrieves flight data every 30 seconds for one hour.
- **Flight Visualization**: Simulates the movement of flights over time on a map with controls for playback.

## Installation

To install the required dependencies for this project, we will use conda to create a new environment and install the necessary libraries.

### Step 1: Create a Conda Environment

Create and activate a new environment using conda.

```bash
conda create -n flight-sim python=3.9
conda activate flight-sim
```

### Step 2: Install Required Libraries

After activating the environment, install the required libraries using the appropriate conda command.

```bash
conda install -c conda-forge requests pandas dash plotly
```

These libraries are required for:

- **requests**: Making API calls to the OpenSky API.
- **pandas**: Handling and cleaning flight data.
- **dash**: Creating the interactive web-based dashboard.
- **plotly**: Visualizing the flight data on an interactive map using `Scattermapbox`.

## Usage

### Running the Flight Data Collector

The Flight Data Collector script retrieves real-time flight data from OpenSky. To run it:

1. Open the script `opensky_flight_data_collector.py`.
2. Ensure that you have the OpenSky API credentials (username and password) set where required.
3. Run the script.

This script:

- Sends requests to OpenSky every 30 seconds for one hour.
- Collects data for up to 300 flights at a time.
- Saves the flight data to `opensky_flights_60min.csv`.

### Running the Flight Simulation Dashboard

Once you have collected flight data, you can visualize it using the Flight Simulation Dashboard. To run the dashboard:

1. Open the script `flight_map_dashboard.py`.
2. Run the script.

This will:

- Launch a Dash web application at `http://127.0.0.1:8050/`.
- Display flights on a map, allowing you to control playback speed, view flight details, and pause/restart the simulation.

## File Structure

