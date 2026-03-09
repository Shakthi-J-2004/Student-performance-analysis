import pandas as pd
import numpy as np
import os

def generate_student_data(n_students=1000):
    np.random.seed(42)
    
    print(f"Generating synthetic dataset for {n_students} students...")
    
    # Generate base features
    study_time = np.random.normal(12, 5, n_students).clip(0, 35) # hours per week
    absences = np.random.normal(4, 3, n_students).clip(0, 25)
    tutoring = np.random.choice(['Yes', 'No'], n_students, p=[0.25, 0.75])
    parental_support = np.random.choice(['High', 'Medium', 'Low'], n_students, p=[0.35, 0.45, 0.20])
    extracurricular = np.random.choice(['Yes', 'No'], n_students, p=[0.55, 0.45])
    gender = np.random.choice(['Male', 'Female'], n_students)
    
    # Calculate GPA based on features to ensure correlations match the expected EDA findings
    # Base GPA
    gpa = 2.4 
    
    # Positive impact from study time
    gpa += (study_time * 0.04)
    
    # Negative impact from absences
    gpa -= (absences * 0.09)
    
    # Positive impact from tutoring and parental support
    gpa += np.where(tutoring == 'Yes', 0.25, 0)
    gpa += np.where(parental_support == 'High', 0.2, np.where(parental_support == 'Low', -0.15, 0))
    
    # Random noise to make it realistic
    gpa += np.random.normal(0, 0.25, n_students)
    
    # Clip GPA between strictly 0.0 and 4.0
    gpa = gpa.clip(0.0, 4.0)
    
    # Create DataFrame
    df = pd.DataFrame({
        'StudentID': [f'STU{str(i).zfill(4)}' for i in range(1, n_students + 1)],
        'Gender': gender,
        'StudyTime': np.round(study_time, 1),
        'Absences': np.round(absences).astype(int),
        'ParentalSupport': parental_support,
        'Tutoring': tutoring,
        'ExtracurricularActivities': extracurricular,
        'GPA': np.round(gpa, 2)
    })
    
    # Introduce some missing values intentionally for the "Data Cleaning" step in EDA
    missing_indices = np.random.choice(n_students, 25, replace=False)
    df.loc[missing_indices, 'StudyTime'] = np.nan
    
    # Save to Excel
    output_file = 'student_performance_data.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Dataset successfully saved to '{output_file}'!")

if __name__ == "__main__":
    generate_student_data()
