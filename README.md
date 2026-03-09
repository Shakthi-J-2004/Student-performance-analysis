# Student Performance EDA Project

This project contains an end-to-end Exploratory Data Analysis (EDA) on student performance, built exactly as requested. 

It includes:
1. A realistic data generation script (`generate_data.py`).
2. An interactive analysis runner (`eda_analysis.py`) that exports high-quality visualizations and terminal insights.

## Project Structure
```text
d:\Student_project\
│-- README.md                    # Project documentation
│-- requirements.txt             # Python dependencies
│-- generate_data.py             # Script to create the synthetic dataset
│-- eda_analysis.py              # Main script performing the EDA process
└-- visualizations/              # Folder (auto-created) where charts are saved
```

## How to Run the Project

**1. Install Dependencies**
Open your terminal in `d:\Student_project` and run:
```bash
pip install -r requirements.txt
```

**2. Generate the Dataset**
Create the `student_performance_data.xlsx` file containing realistic, correlational mock data:
```bash
python generate_data.py
```

**3. Run the EDA Analysis**
Execute the main analysis. This will output summary statistics/correlations to your console and save all the charts to the `visualizations` folder:
```bash
python eda_analysis.py
```

## Output Visualizations
After running the EDA script, look inside the `visualizations/` folder for:
- `01_univariate_analysis.png` (GPA & Study Time distributions)
- `02_bivariate_analysis.png` (Scatter plots with trendlines)
- `03_categorical_analysis.png` (Boxplots for Support & Activities)
- `04_correlation_heatmap.png` (Correlation matrix)
- `05_pie_charts.png` (Demographic breakdown)

## How to Deploy to Streamlit Community Cloud (Free)

To share this analytics dashboard live on the internet, you can use **Streamlit Community Cloud**, which natively hosts Streamlit Python applications for free.

**1. Push to GitHub**
First, upload this entire project folder (`d:\Student_project`) to a public or private GitHub repository. 
Ensure the following files are included in the repository:
*   `app.py`
*   `requirements.txt`
*   `student_performance_data.xlsx`

**2. Deploy via Streamlit**
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Log in using your GitHub account.
3. Click exactly: **"New App"** -> **"Deploy a public app from GitHub"**.
4. Fill in the fields:
   * **Repository**: *[Select your GitHub Repository name]*
   * **Branch**: `main` (or `master`)
   * **Main file path**: `app.py`
5. Click **Deploy!**

In about 1-2 minutes, Streamlit will spin up a server, install your `requirements.txt`, and generate a live, shareable URL for your dashboard!
