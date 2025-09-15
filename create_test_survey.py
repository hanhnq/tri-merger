import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

# Create sample survey data
def create_survey_data():
    # Number of respondents
    n_respondents = 100
    
    # Generate respondent IDs
    respondent_ids = [f"R{str(i).zfill(4)}" for i in range(1, n_respondents + 1)]
    
    # Generate timestamps
    base_date = datetime(2025, 1, 1, 9, 0, 0)
    timestamps = [base_date + timedelta(minutes=random.randint(0, 7200)) for _ in range(n_respondents)]
    
    # Demographics
    ages = [random.choice([18, 25, 30, 35, 40, 45, 50, 55, 60, 65]) for _ in range(n_respondents)]
    genders = [random.choice(['Male', 'Female', 'Other']) for _ in range(n_respondents)]
    regions = [random.choice(['North', 'South', 'East', 'West', 'Central']) for _ in range(n_respondents)]
    
    # Survey questions (5-point Likert scale)
    q1_satisfaction = [random.randint(1, 5) for _ in range(n_respondents)]
    q2_frequency = [random.choice(['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']) for _ in range(n_respondents)]
    q3_recommend = [random.randint(1, 10) for _ in range(n_respondents)]
    q4_quality = [random.randint(1, 5) for _ in range(n_respondents)]
    q5_value = [random.randint(1, 5) for _ in range(n_respondents)]
    
    # Multiple choice questions
    q6_preference = [random.choice(['Option A', 'Option B', 'Option C', 'Option D']) for _ in range(n_respondents)]
    q7_source = [random.choice(['Internet', 'TV', 'Radio', 'Newspaper', 'Social Media']) for _ in range(n_respondents)]
    
    # Yes/No questions
    q8_purchase = [random.choice(['Yes', 'No']) for _ in range(n_respondents)]
    q9_awareness = [random.choice(['Yes', 'No']) for _ in range(n_respondents)]
    
    # Open-ended (simulated with predefined responses)
    comments = [
        random.choice([
            'Great service, very satisfied',
            'Could be improved',
            'Average experience',
            'Excellent quality',
            'Poor customer support',
            'Good value for money',
            'Needs more features',
            'Very user-friendly',
            'Too expensive',
            'Highly recommend',
            np.nan  # Some empty responses
        ]) for _ in range(n_respondents)
    ]
    
    # Create main dataframe
    df_main = pd.DataFrame({
        'Respondent_ID': respondent_ids,
        'Timestamp': timestamps,
        'Age': ages,
        'Gender': genders,
        'Region': regions,
        'Q1_Overall_Satisfaction': q1_satisfaction,
        'Q2_Usage_Frequency': q2_frequency,
        'Q3_Recommend_Score': q3_recommend,
        'Q4_Quality_Rating': q4_quality,
        'Q5_Value_Rating': q5_value,
        'Q6_Preferred_Feature': q6_preference,
        'Q7_Information_Source': q7_source,
        'Q8_Recent_Purchase': q8_purchase,
        'Q9_Brand_Awareness': q9_awareness,
        'Q10_Comments': comments
    })
    
    # Create summary statistics sheet
    summary_data = {
        'Metric': [
            'Total Responses',
            'Average Age',
            'Avg Satisfaction Score',
            'Avg Recommend Score',
            'Avg Quality Rating',
            'Avg Value Rating',
            'Purchase Rate (%)',
            'Awareness Rate (%)'
        ],
        'Value': [
            n_respondents,
            round(np.mean(ages), 1),
            round(np.mean(q1_satisfaction), 2),
            round(np.mean(q3_recommend), 2),
            round(np.mean(q4_quality), 2),
            round(np.mean(q5_value), 2),
            round(q8_purchase.count('Yes') / n_respondents * 100, 1),
            round(q9_awareness.count('Yes') / n_respondents * 100, 1)
        ]
    }
    df_summary = pd.DataFrame(summary_data)
    
    # Create demographic breakdown
    gender_counts = pd.DataFrame({
        'Gender': ['Male', 'Female', 'Other'],
        'Count': [genders.count('Male'), genders.count('Female'), genders.count('Other')]
    })
    
    region_counts = pd.DataFrame({
        'Region': ['North', 'South', 'East', 'West', 'Central'],
        'Count': [regions.count('North'), regions.count('South'), regions.count('East'), 
                 regions.count('West'), regions.count('Central')]
    })
    
    # Create question mapping sheet
    question_map = pd.DataFrame({
        'Question_ID': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10'],
        'Question_Text': [
            'How satisfied are you with our service overall?',
            'How frequently do you use our service?',
            'How likely are you to recommend us to others? (1-10)',
            'How would you rate the quality of our service?',
            'How would you rate the value for money?',
            'Which feature do you prefer most?',
            'Where did you first hear about us?',
            'Have you made a purchase in the last 30 days?',
            'Were you aware of our brand before this survey?',
            'Do you have any additional comments or suggestions?'
        ],
        'Question_Type': [
            'Likert Scale (1-5)',
            'Multiple Choice',
            'Scale (1-10)',
            'Likert Scale (1-5)',
            'Likert Scale (1-5)',
            'Multiple Choice',
            'Multiple Choice',
            'Yes/No',
            'Yes/No',
            'Open Text'
        ]
    })
    
    return df_main, df_summary, gender_counts, region_counts, question_map

# Create the Excel file
def create_excel_file():
    df_main, df_summary, gender_counts, region_counts, question_map = create_survey_data()
    
    # Create Excel writer
    output_file = 'Internet_Survey_January_2025.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write each dataframe to a different sheet
        df_main.to_excel(writer, sheet_name='Survey_Responses', index=False)
        df_summary.to_excel(writer, sheet_name='Summary_Statistics', index=False)
        gender_counts.to_excel(writer, sheet_name='Gender_Distribution', index=False)
        region_counts.to_excel(writer, sheet_name='Region_Distribution', index=False)
        question_map.to_excel(writer, sheet_name='Question_Mapping', index=False)
        
        # Get workbook
        workbook = writer.book
        
        # Auto-adjust column widths for openpyxl
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            
            # Get the dataframe for this sheet
            if sheet_name == 'Survey_Responses':
                df = df_main
            elif sheet_name == 'Summary_Statistics':
                df = df_summary
            elif sheet_name == 'Gender_Distribution':
                df = gender_counts
            elif sheet_name == 'Region_Distribution':
                df = region_counts
            else:
                df = question_map
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"Excel file '{output_file}' has been created successfully!")
    print(f"The file contains {len(df_main)} survey responses with the following sheets:")
    print("1. Survey_Responses - Main survey data")
    print("2. Summary_Statistics - Key metrics summary")
    print("3. Gender_Distribution - Breakdown by gender")
    print("4. Region_Distribution - Breakdown by region")
    print("5. Question_Mapping - Survey questions reference")

if __name__ == "__main__":
    create_excel_file()