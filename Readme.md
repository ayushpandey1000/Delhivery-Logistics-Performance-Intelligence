# Delhivery Logistics & Last-Mile Delivery Performance Intelligence

An end-to-end data analytics project focused on analyzing logistics operations, route performance, delivery time variations, and potential operational outliers using Python, SQL, and Power BI.

## Project Overview

The project analyzes logistics and last-mile delivery data to understand route-level performance and identify variations between actual transportation time and estimated time.

The objective is to transform raw logistics data into meaningful insights that can help understand delivery efficiency, route performance, and operational inconsistencies.

## Business Objectives

- Analyze overall trip and route performance.
- Compare actual transportation time with estimated time.
- Identify routes with significant time variations.
- Detect potential outliers in route performance.
- Build an interactive Power BI dashboard for data-driven analysis.

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | Data cleaning, preprocessing and analysis |
| Pandas & NumPy | Data manipulation and numerical analysis |
| Matplotlib | Data visualization |
| SQL | Data querying and analysis |
| Power BI | Interactive dashboard and reporting |
| Git & GitHub | Version control and project hosting |

## Dataset Information

The project uses a logistics dataset containing trip-level and route-level information.

**Dataset Statistics:**

| Metric | Value |
|---|---:|
| Total Records | 144,867 |
| Total Columns | 24 |
| Unique Trips | 14,817 |
| Route-Level Records | 26,368 |
| Exact Duplicate Rows | 0 |

## Data Cleaning & Preprocessing

The following operations were performed using Python:

- Inspected dataset structure and data types.
- Identified and handled missing source and destination names.
- Checked for duplicate records.
- Converted relevant columns into datetime format.
- Identified invalid date values.
- Prepared route-level data for performance analysis.

## Exploratory Data Analysis

The analysis focused on:

- Actual Time vs Estimated Time
- Route-Level Time Difference
- Route Performance Comparison
- Top Routes with Higher Time Variation
- Potential Outlier Detection

The time difference was calculated as:

`Time Difference = Actual Time - Estimated Time`

Potential outliers were identified using the Interquartile Range (IQR) method.

## Key Findings

- The dataset contains 14,817 unique trips and 26,368 route-level records.
- Average route-level time difference was approximately 109.62 dataset time units.
- Median route-level time difference was 42 dataset time units.
- 3,007 route records were identified as potential outliers using the IQR method.
- Several routes showed substantial differences between actual and estimated time.

*Note: These findings are based on the current route-level aggregation and exploratory analysis. Time units and operational causes should be independently validated before interpreting these differences as actual delivery delays.*

## Power BI Dashboard

An interactive Power BI dashboard was developed to present key performance indicators and route-level insights.

**Dashboard Features:**

- Total Trips
- Total Route Records
- Average Actual Time
- Average Time Difference
- Segments Above Estimate
- Potential Outliers
- Route Performance Analysis
- Source, Destination and Route Type Filters

### Dashboard Preview

Add your Power BI dashboard screenshot here.

`image/your-dashboard-screenshot.png`

## Project Structure

```text
Delhivery-Logistics-Performance-Intelligence/
│
├── data/
│   ├── Dataset and processed data files
│
├── image/
│   └── Dashboard screenshots
│
├── powerbi/
│   └── Power BI dashboard file
│
├── python/
│   └── Python analysis files
│
└── README.md
```

*Folder contents may vary depending on the files included in the repository.*

## Conclusion

This project demonstrates an end-to-end logistics analytics workflow, starting from data cleaning and exploratory analysis to route-level performance evaluation and interactive dashboard development.

It highlights how data analytics tools can be used to examine logistics operations, identify unusual patterns, and support data-driven decision-making.

## Author

**Ayush Pandey**

GitHub: [ayushpandey1000](https://github.com/ayushpandey1000)

Project Repository: [Delhivery Logistics Performance Intelligence](https://github.com/ayushpandey1000/Delhivery-Logistics-Performance-Intelligence)
