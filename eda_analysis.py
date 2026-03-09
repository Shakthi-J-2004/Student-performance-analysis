import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

def print_header(title):
    print(f"\n{'='*50}")
    print(f" {title} ")
    print(f"{'='*50}")
    time.sleep(1)

def run_eda():
    # Setup visualization directory
    os.makedirs('visualizations', exist_ok=True)
    
    # --- 5. Load Dataset ---
    print_header("5. Loading Dataset")
    if not os.path.exists("student_performance_data.xlsx"):
        print("Error: Dataset not found. Please run 'generate_data.py' first.")
        return

    df = pd.read_excel("student_performance_data.xlsx")
    print("Preview of first 5 rows:")
    print(df.head())
    
    # --- 6. Data Inspection ---
    print_header("6. Data Inspection")
    print("Information about the dataset:")
    df.info()
    print("\nSummary statistics of numerical columns:")
    print(df.describe())
    
    # --- 7. Data Cleaning ---
    print_header("7. Data Cleaning")
    print("Missing values before cleaning:")
    print(df.isnull().sum())
    
    # Fill missing StudyTime with the median
    df.fillna({'StudyTime': df['StudyTime'].median()}, inplace=True)
    print("Filled missing 'StudyTime' values with the median.")
    
    print("\nDropping unnecessary column: 'StudentID'")
    df.drop("StudentID", axis=1, inplace=True)
    
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())
    
    # Set default style for plots
    sns.set_theme(style="whitegrid")
    
    # --- 9. Univariate Analysis ---
    print_header("9. Univariate Analysis (Generating Plots...)")
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    sns.histplot(df['GPA'], kde=True, bins=20, color='skyblue')
    plt.title('Distribution of GPA')
    
    plt.subplot(1, 2, 2)
    sns.histplot(df['StudyTime'], kde=True, bins=20, color='lightgreen')
    plt.title('Distribution of Study Time')
    
    plt.tight_layout()
    plt.savefig('visualizations/01_univariate_analysis.png')
    plt.close()
    print("Saved 'visualizations/01_univariate_analysis.png'")

    # --- 10. Bivariate Analysis ---
    print_header("10. Bivariate Analysis (Generating Plots...)")
    plt.figure(figsize=(14, 5))
    
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=df, x='StudyTime', y='GPA', alpha=0.5, color='blue')
    sns.regplot(data=df, x='StudyTime', y='GPA', scatter=False, color='red')
    plt.title('Study Time vs GPA')
    
    plt.subplot(1, 2, 2)
    sns.scatterplot(data=df, x='Absences', y='GPA', alpha=0.5, color='orange')
    sns.regplot(data=df, x='Absences', y='GPA', scatter=False, color='red')
    plt.title('Absences vs GPA')
    
    plt.tight_layout()
    plt.savefig('visualizations/02_bivariate_analysis.png')
    plt.close()
    print("Saved 'visualizations/02_bivariate_analysis.png'")

    # --- 11. Additional Analysis ---
    print_header("11. Categorical vs Continuous Analysis (Generating Plots...)")
    plt.figure(figsize=(18, 5))
    
    plt.subplot(1, 3, 1)
    sns.boxplot(data=df, x='ParentalSupport', y='GPA', palette='Set2')
    plt.title('Parental Support vs GPA')
    
    plt.subplot(1, 3, 2)
    sns.boxplot(data=df, x='Tutoring', y='GPA', palette='Set1')
    plt.title('Tutoring vs GPA')
    
    plt.subplot(1, 3, 3)
    sns.boxplot(data=df, x='ExtracurricularActivities', y='GPA', palette='Set3')
    plt.title('Extracurricular Activities vs GPA')
    
    plt.tight_layout()
    plt.savefig('visualizations/03_categorical_analysis.png')
    plt.close()
    print("Saved 'visualizations/03_categorical_analysis.png'")

    # --- 12. Correlation Analysis ---
    print_header("12. Correlation Analysis (Generating Heatmap...)")
    plt.figure(figsize=(8, 6))
    numerical_cols = df.select_dtypes(include=['float64', 'int64', 'int32'])
    corr_matrix = numerical_cols.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('visualizations/04_correlation_heatmap.png')
    plt.close()
    print("Saved 'visualizations/04_correlation_heatmap.png'")
    
    print("\nCorrelation with GPA:")
    print(corr_matrix['GPA'].sort_values(ascending=False))

    # --- 13. Student Segmentation ---
    print_header("13. Student Segmentation")
    def segment_students(gpa):
        if gpa > 3.0:
            return 'High Performer'
        elif 2.0 <= gpa <= 3.0:
            return 'Average Student'
        else:
            return 'At Risk'

    df['PerformanceSegment'] = df['GPA'].apply(segment_students)
    print("Student Segments Breakdown:")
    print(df['PerformanceSegment'].value_counts())

    # --- 14. Visualizations (Pie Charts) ---
    print_header("14. Final Visualizations: Demographics & Activities")
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    df['Gender'].value_counts().plot.pie(autopct='%1.1f%%', ax=axes[0], colors=['#ff9999','#66b3ff'], startangle=90)
    axes[0].set_title('Gender Distribution')
    axes[0].set_ylabel('')
    
    df['Tutoring'].value_counts().plot.pie(autopct='%1.1f%%', ax=axes[1], colors=['#99ff99','#ffcc99'], startangle=90)
    axes[1].set_title('Tutoring Participation')
    axes[1].set_ylabel('')
    
    df['ExtracurricularActivities'].value_counts().plot.pie(autopct='%1.1f%%', ax=axes[2], colors=['#c2c2f0','#ffb3e6'], startangle=90)
    axes[2].set_title('Extracurricular Participation')
    axes[2].set_ylabel('')
    
    plt.tight_layout()
    plt.savefig('visualizations/05_pie_charts.png')
    plt.close()
    print("Saved 'visualizations/05_pie_charts.png'")
    
    print_header("Analysis Complete! Check the 'visualizations' folder for output plots.")

if __name__ == "__main__":
    run_eda()
