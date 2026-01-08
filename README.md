# 📊 IT Job Market Analysis Dashboard (Poland)

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=Power%20BI&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-00758F?style=for-the-badge&logo=powerbi&logoColor=white)
![Power Query](https://img.shields.io/badge/Power_Query-29B96D?style=for-the-badge&logo=powerbi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

## 💡 Project Overview
This project is an end-to-end data analysis solution tracking the current state of the IT job market in Poland based on data from **No Fluff Jobs**.

The goal was to transform raw, unstructured web data into actionable insights for candidates and recruiters. The final report analyzes over **2,494 active job offers** and **831 unique skills**, providing answers to questions about salary progression, remote work trends, and the most valuable technical skills.

📥 **[Download the Full PDF Report](No_Fluff_Jobs_Report.pdf)**

---

## 🏗️ Technical Workflow & Methodology

This project was executed in 4 main stages:

### 1. Data Collection (Python) 🐍
* **Script:** `job_scraper.py`
* **Process:** Automated scraping of job offers using Python libraries.
* **Scope:** Extracted key data points: Job Title, Company, Salary Range (Junior/Mid/Senior), Tech Stack, Requirements, and Location.
* **Output:** Raw data exported to Excel/CSV for further processing.

### 2. ETL & Data Cleaning (Power Query) 🧹
* **Currency Normalization:** Handled mixed currencies (PLN/EUR/USD) and converted them to a standard format.
* **String Manipulation:** Split complex "Location" strings to separate remote work flags from physical cities.
* **Bridge Table Implementation:** Solved the *Many-to-Many* relationship problem between `Job Offers` and `Skills` (since one offer requires multiple skills) by creating a dedicated Bridge Table. This prevents data duplication and allows for accurate filtering.

### 3. Data Modeling & DAX 🧮
* **Star Schema:** Built an optimized data model connecting *Fact Tables* (Offers) with *Dimension Tables* (Skills, Locations, Calendar).
* **Advanced Measures:**
    * **`Avg Salary`**: Calculated dynamically to avoid the "Sum Trap" and handle salary ranges correctly.
    * **`Requirements_Count`**: Used `DISTINCTCOUNT` to analyze how many unique skills are required per offer.
    * **`Remote %`**: Calculated the share of fully remote offers vs. hybrid/office.

### 4. Data Visualization (Power BI) 📊
Designed a 3-page interactive report focused on UX and storytelling:
* **Market Overview:** High-level KPIs and salary progression by seniority.
* **Tech Analytics:** "Top N" analysis distinguishing between *Most Popular* skills (e.g., Python) and *Highest Paying* niche skills (e.g. Kafka).
* **Geo-Analytics:** Analysis of salary discrepancies between Polish hubs.
---

## 🖼️ Dashboard Preview

### Page 1: Market Overview
*Key insights: 87.9% of offers are remote. Significant salary jump between Mid and Senior levels.*
<img width="1808" height="1024" alt="NoFluffJobs2" src="https://github.com/user-attachments/assets/c402801e-a575-4cd4-8008-ee7d7a6b3f75" />

### Page 2: Technology & Skills
*Key insights: While Java/Python dominate popularity, niche architectural skills and specific tools (Kafka, Oracle) command the highest average salaries.*
<img width="1808" height="1024" alt="NoFluffJobs1" src="https://github.com/user-attachments/assets/f3248013-0a04-4eab-9429-844e740e4cc3" />

### Page 3: Location & Remote Trends
*Key insights: Comparison of salaries across major cities and the distribution of Remote vs. Office work.*
<img width="1804" height="1021" alt="NoFluffJobs3" src="https://github.com/user-attachments/assets/34ebaafc-a613-4508-b1b0-8520eb7d12f3" />

---

## 📂 Repository Structure

* `No Fluff Jobs.pbix` - The main Power BI source file (requires Power BI Desktop).
* `No_Fluff_Jobs_Report.pdf` - High-quality export of the final report.
* `job_scraper.py` - Python script used for data collection.
* `requirements.txt` - List of Python dependencies.

## 💻 Development Environment
Although Power BI requires Windows, this project was developed using a **hybrid workflow**:
* **Data Visualization:** Microsoft Windows 11 (Power BI Desktop).
* **Scripting & Version Control:** **WSL 2 (Ubuntu)**. All Python scripts and Git commands were executed via the Linux terminal (Bash), demonstrating familiarity with Unix-based environments.
 
## 🚀 How to Run

1.  **Python Scraper:**
    ```bash
    pip install -r requirements.txt
    python job_scraper.py
    ```
2.  **Power BI:**
    * Download `No Fluff Jobs.pbix`.
    * Open with Microsoft Power BI Desktop.
    * (Optional) Refresh data if you have the local Excel source connected.

---
© 2026 Anna Grzywa. All rights reserved.

*Data Source: Publicly available data from No Fluff Jobs (Educational Project).*
