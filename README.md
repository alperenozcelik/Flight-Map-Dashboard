# Flight Data Collection and Simulation

This repository contains two Python scripts:
1. **Flight Data Collector**: Collects real-time flight data from the OpenSky API and saves it into a CSV file.
2. **Flight Simulation Dashboard**: Visualizes the collected flight data on an interactive map using Dash and Plotly.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Running the Flight Data Collector](#running-the-flight-data-collector)
  - [Running the Flight Simulation Dashboard](#running-the-flight-simulation-dashboard)
- [File Structure](#file-structure)
- [Code Explanation](#code-explanation)

---

## Overview

This project allows you to:
- **Collect real-time flight data** from the OpenSky API every 30 seconds for one hour.
- **Visualize and simulate** flight movements on an interactive map, with controls for adjusting playback speed and viewing detailed flight information.

## Installation

To set up this project, follow these steps:

### Step 1: Create a Conda Environment

First, create a new Conda environment with Python 3.9 and activate it:

```bash
conda create -n flight-sim python=3.9
conda activate flight-sim
