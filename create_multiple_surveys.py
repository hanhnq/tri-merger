import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_question_master_sheet(survey_type="general"):
    """Create the question master sheet with various question types for different survey themes"""
    
    questions_data = []
    
    if survey_type == "product":
        # Product satisfaction survey
        # Q-001: Age and Gender (same structure)
        questions_data.extend([
            ['Q-001', 'Required', 'Please tell us your age and gender', 'S/A'],
            ['', '', '1. Male 18-24', ''],
            ['', '', '2. Male 25-34', ''],
            ['', '', '3. Male 35-44', ''],
            ['', '', '4. Male 45-54', ''],
            ['', '', '5. Male 55-64', ''],
            ['', '', '6. Male 65+', ''],
            ['', '', '7. Female 18-24', ''],
            ['', '', '8. Female 25-34', ''],
            ['', '', '9. Female 35-44', ''],
            ['', '', '10. Female 45-54', ''],
            ['', '', '11. Female 55-64', ''],
            ['', '', '12. Female 65+', ''],
            ['', '', '', '']
        ])
        
        # Q-002: How long have you been using our product?
        questions_data.extend([
            ['Q-002', 'Required', 'How long have you been using our product?', 'S/A'],
            ['', '', '1. Less than 1 month', ''],
            ['', '', '2. 1-3 months', ''],
            ['', '', '3. 3-6 months', ''],
            ['', '', '4. 6-12 months', ''],
            ['', '', '5. 1-2 years', ''],
            ['', '', '6. More than 2 years', ''],
            ['', '', '', '']
        ])
        
        # Q-003: Which version do you use?
        questions_data.extend([
            ['Q-003', 'Required', 'Which version of our product do you primarily use?', 'S/A'],
            ['', '', '1. Free version', ''],
            ['', '', '2. Basic paid plan', ''],
            ['', '', '3. Premium plan', ''],
            ['', '', '4. Enterprise plan', ''],
            ['', '', '5. Trial version', ''],
            ['', '', '6. Other', ''],
            ['', '', '', '']
        ])
        
    elif survey_type == "service":
        # Service quality survey
        questions_data.extend([
            ['Q-001', 'Required', 'Please tell us your age and gender', 'S/A'],
            ['', '', '1. Male Under 25', ''],
            ['', '', '2. Male 25-35', ''],
            ['', '', '3. Male 36-45', ''],
            ['', '', '4. Male 46-55', ''],
            ['', '', '5. Male Over 55', ''],
            ['', '', '6. Female Under 25', ''],
            ['', '', '7. Female 25-35', ''],
            ['', '', '8. Female 36-45', ''],
            ['', '', '9. Female 46-55', ''],
            ['', '', '10. Female Over 55', ''],
            ['', '', '', '']
        ])
        
        # Q-002: Service frequency
        questions_data.extend([
            ['Q-002', 'Required', 'How often do you use our services?', 'S/A'],
            ['', '', '1. Daily', ''],
            ['', '', '2. Weekly', ''],
            ['', '', '3. Monthly', ''],
            ['', '', '4. Quarterly', ''],
            ['', '', '5. Rarely', ''],
            ['', '', '6. First time user', ''],
            ['', '', '', '']
        ])
        
        # Q-003: Service type
        questions_data.extend([
            ['Q-003', 'Required', 'Which service did you use most recently?', 'S/A'],
            ['', '', '1. Customer support', ''],
            ['', '', '2. Technical consultation', ''],
            ['', '', '3. Installation service', ''],
            ['', '', '4. Maintenance service', ''],
            ['', '', '5. Training service', ''],
            ['', '', '6. Repair service', ''],
            ['', '', '7. Upgrade service', ''],
            ['', '', '8. Other', ''],
            ['', '', '', '']
        ])
        
    elif survey_type == "website":
        # Website usability survey
        questions_data.extend([
            ['Q-001', 'Required', 'Please tell us your age and gender', 'S/A'],
            ['', '', '1. Male 16-20', ''],
            ['', '', '2. Male 21-30', ''],
            ['', '', '3. Male 31-40', ''],
            ['', '', '4. Male 41-50', ''],
            ['', '', '5. Male 51+', ''],
            ['', '', '6. Female 16-20', ''],
            ['', '', '7. Female 21-30', ''],
            ['', '', '8. Female 31-40', ''],
            ['', '', '9. Female 41-50', ''],
            ['', '', '10. Female 51+', ''],
            ['', '', '11. Other', ''],
            ['', '', '', '']
        ])
        
        # Q-002: Device used
        questions_data.extend([
            ['Q-002', 'Required', 'What device did you primarily use to visit our website?', 'S/A'],
            ['', '', '1. Desktop computer', ''],
            ['', '', '2. Laptop', ''],
            ['', '', '3. Tablet', ''],
            ['', '', '4. Smartphone', ''],
            ['', '', '5. Smart TV', ''],
            ['', '', '', '']
        ])
        
        # Q-003: Browser
        questions_data.extend([
            ['Q-003', 'Required', 'Which browser did you use?', 'S/A'],
            ['', '', '1. Chrome', ''],
            ['', '', '2. Firefox', ''],
            ['', '', '3. Safari', ''],
            ['', '', '4. Edge', ''],
            ['', '', '5. Opera', ''],
            ['', '', '6. Other', ''],
            ['', '', '', '']
        ])
        
    else:  # marketing survey
        # Marketing effectiveness survey
        questions_data.extend([
            ['Q-001', 'Required', 'Please tell us your age and gender', 'S/A'],
            ['', '', '1. Male Teen (13-19)', ''],
            ['', '', '2. Male Young Adult (20-29)', ''],
            ['', '', '3. Male Adult (30-39)', ''],
            ['', '', '4. Male Middle-aged (40-49)', ''],
            ['', '', '5. Male Mature (50-59)', ''],
            ['', '', '6. Male Senior (60+)', ''],
            ['', '', '7. Female Teen (13-19)', ''],
            ['', '', '8. Female Young Adult (20-29)', ''],
            ['', '', '9. Female Adult (30-39)', ''],
            ['', '', '10. Female Middle-aged (40-49)', ''],
            ['', '', '11. Female Mature (50-59)', ''],
            ['', '', '12. Female Senior (60+)', ''],
            ['', '', '', '']
        ])
        
        # Q-002: Income bracket
        questions_data.extend([
            ['Q-002', 'Optional', 'What is your household income range?', 'S/A'],
            ['', '', '1. Under $25,000', ''],
            ['', '', '2. $25,000 - $40,000', ''],
            ['', '', '3. $40,000 - $60,000', ''],
            ['', '', '4. $60,000 - $80,000', ''],
            ['', '', '5. $80,000 - $100,000', ''],
            ['', '', '6. Over $100,000', ''],
            ['', '', '7. Prefer not to say', ''],
            ['', '', '', '']
        ])
        
        # Q-003: Education level
        questions_data.extend([
            ['Q-003', 'Required', 'What is your highest level of education?', 'S/A'],
            ['', '', '1. High school or less', ''],
            ['', '', '2. Some college', ''],
            ['', '', '3. Bachelor degree', ''],
            ['', '', '4. Master degree', ''],
            ['', '', '5. Doctorate', ''],
            ['', '', '6. Professional degree', ''],
            ['', '', '7. Other', ''],
            ['', '', '', '']
        ])
    
    # Add common questions for all survey types
    # Satisfaction questions Q-004 to Q-008
    satisfaction_topics = ['Overall satisfaction', 'Value for money', 'Quality', 'Ease of use', 'Customer support']
    for i, topic in enumerate(satisfaction_topics, start=4):
        q_num = f'Q-{str(i).zfill(3)}'
        questions_data.extend([
            [q_num, 'Required', f'Rate your {topic}', 'S/A'],
            ['', '', '1. Very Poor', ''],
            ['', '', '2. Poor', ''],
            ['', '', '3. Fair', ''],
            ['', '', '4. Good', ''],
            ['', '', '5. Excellent', ''],
            ['', '', '', '']
        ])
    
    # Multi-answer question Q-009
    if survey_type == "product":
        features = ['User interface', 'Performance', 'Reliability', 'Features', 'Integration', 'Mobile app', 
                   'Documentation', 'Support', 'Updates', 'Security', 'Customization', 'Reports', 'API']
    elif survey_type == "service":
        features = ['Response time', 'Staff knowledge', 'Problem solving', 'Follow-up', 'Communication', 
                   'Availability', 'Professionalism', 'Equipment quality', 'Scheduling', 'Cost transparency']
    elif survey_type == "website":
        features = ['Navigation', 'Loading speed', 'Mobile experience', 'Search function', 'Content quality',
                   'Design', 'Checkout process', 'Account management', 'Help section', 'Contact options']
    else:  # marketing
        features = ['TV ads', 'Online ads', 'Social media', 'Email campaigns', 'Print ads', 'Radio ads',
                   'Billboards', 'Events', 'Influencers', 'Word of mouth', 'Referral program']
    
    questions_data.extend([
        ['Q-009', 'Required', f'Which aspects are most important to you? (Select all that apply)', 'M/A'],
    ])
    for i, feature in enumerate(features, 1):
        questions_data.append(['', '', f'{i}. {feature}', ''])
    questions_data.append(['', '', f'{len(features)+1}. Other (Please specify)', ''])
    questions_data.append(['', '', '', ''])
    
    # Continue with more questions following the same pattern as the original
    # Q-010 to Q-086 with mixed question types
    for q in range(10, 87):
        q_num = f'Q-{str(q).zfill(3)}'
        
        if q % 7 == 0:  # Free answer questions
            questions_data.extend([
                [q_num, 'Optional', f'Please share your thoughts on improvement area {q}', 'FA'],
                ['', '', '(Open text response)', ''],
                ['', '', '', '']
            ])
        elif q % 4 == 0:  # Multi-answer with FA
            questions_data.append([q_num, 'Optional', f'Select all relevant options for category {q}', 'M/A+FA'])
            num_opts = random.randint(6, 12)
            for i in range(1, num_opts):
                questions_data.append(['', '', f'{i}. Option {i} for Q{q}', ''])
            questions_data.append(['', '', f'{num_opts}. Other (Please specify)', ''])
            questions_data.append(['', '', '', ''])
        elif q % 3 == 0:  # Multi-answer
            questions_data.append([q_num, 'Required' if q % 2 == 0 else 'Optional', 
                                 f'Choose all that apply for topic {q}', 'M/A'])
            num_opts = random.randint(5, 10)
            for i in range(1, num_opts + 1):
                questions_data.append(['', '', f'{i}. Choice {i}', ''])
            questions_data.append(['', '', '', ''])
        else:  # Single answer with or without FA
            has_fa = q % 5 == 1
            questions_data.append([q_num, 'Required' if q % 2 == 0 else 'Optional', 
                                 f'Please rate aspect {q}', 'S/A+FA' if has_fa else 'S/A'])
            num_opts = random.randint(4, 8)
            for i in range(1, num_opts):
                questions_data.append(['', '', f'{i}. Level {i}', ''])
            if has_fa:
                questions_data.append(['', '', f'{num_opts}. Other (Please specify)', ''])
            else:
                questions_data.append(['', '', f'{num_opts}. Level {num_opts}', ''])
            questions_data.append(['', '', '', ''])
    
    df = pd.DataFrame(questions_data, columns=['Question_ID', 'Requirement', 'Question_Text', 'Type'])
    return df

def create_survey_data_sheet(num_respondents=156, survey_type="general"):
    """Create the survey response data sheet with proper binary structure"""
    
    np.random.seed(random.randint(1, 1000))  # Different seed for each survey
    data = {}
    
    # NO column (respondent ID)
    data['NO'] = [200000 + i * 1357 for i in range(num_respondents)]
    
    # Q-001: Demographics (varies by survey type)
    if survey_type == "website":
        num_options = 11
    else:
        num_options = 12
    
    for i in range(1, num_options + 1):
        data[f'Q-001_{i}'] = [0] * num_respondents
    for idx in range(num_respondents):
        chosen = np.random.randint(1, num_options + 1)
        data[f'Q-001_{chosen}'][idx] = 1
    
    # Q-002: Different options based on survey type
    if survey_type == "product":
        num_options = 6
    elif survey_type == "service":
        num_options = 6
    elif survey_type == "website":
        num_options = 5
    else:  # marketing
        num_options = 7
    
    for i in range(1, num_options + 1):
        data[f'Q-002_{i}'] = [0] * num_respondents
    for idx in range(num_respondents):
        chosen = np.random.randint(1, num_options + 1)
        data[f'Q-002_{chosen}'][idx] = 1
    
    # Q-003: Different options based on survey type
    if survey_type == "product":
        num_options = 6
        # Add FA for "Other" option
        data['Q-003_6_SA'] = [None] * num_respondents
        for i in range(1, num_options + 1):
            data[f'Q-003_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, num_options + 1)
            data[f'Q-003_{chosen}'][idx] = 1
            if chosen == 6:
                data['Q-003_6_SA'][idx] = random.choice(['Custom plan', 'Beta version', 'Partner edition'])
    elif survey_type == "service":
        num_options = 8
        data['Q-003_8_SA'] = [None] * num_respondents
        for i in range(1, num_options + 1):
            data[f'Q-003_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, num_options + 1)
            data[f'Q-003_{chosen}'][idx] = 1
            if chosen == 8:
                data['Q-003_8_SA'][idx] = random.choice(['Emergency service', 'Custom solution', 'Consultation'])
    elif survey_type == "website":
        num_options = 6
        data['Q-003_6_SA'] = [None] * num_respondents
        for i in range(1, num_options + 1):
            data[f'Q-003_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, num_options + 1)
            data[f'Q-003_{chosen}'][idx] = 1
            if chosen == 6:
                data['Q-003_6_SA'][idx] = random.choice(['Internet Explorer', 'Brave', 'Custom browser'])
    else:  # marketing
        num_options = 7
        data['Q-003_7_SA'] = [None] * num_respondents
        for i in range(1, num_options + 1):
            data[f'Q-003_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, num_options + 1)
            data[f'Q-003_{chosen}'][idx] = 1
            if chosen == 7:
                data['Q-003_7_SA'][idx] = random.choice(['Technical certification', 'Online course', 'Bootcamp'])
    
    # Q-004 to Q-008: Satisfaction ratings (5 options each)
    for q in range(4, 9):
        q_str = f'Q-{str(q).zfill(3)}'
        for i in range(1, 6):
            data[f'{q_str}_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 6)
            data[f'{q_str}_{chosen}'][idx] = 1
    
    # Q-009: Multi-answer question
    if survey_type == "product":
        num_subs = 13
    elif survey_type == "service":
        num_subs = 10
    elif survey_type == "website":
        num_subs = 10
    else:  # marketing
        num_subs = 11
    
    for i in range(1, num_subs + 2):  # +1 for "Other" option
        data[f'Q-009_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.7, 0.3])
    data[f'Q-009_{num_subs+1}_FA'] = [random.choice(['Custom need', 'Special requirement', None, None, None]) 
                                      for _ in range(num_respondents)]
    
    # Q-010 to Q-086: Mixed question types
    for q in range(10, 87):
        q_str = f'Q-{str(q).zfill(3)}'
        
        if q % 7 == 0:  # Free answer questions
            data[q_str] = [random.choice([
                'Very satisfied with the service', 'Could use some improvements', 
                'Meeting expectations', 'Excellent quality', 'Good value',
                'Professional service', None, None, None
            ]) for _ in range(num_respondents)]
        elif q % 4 == 0:  # Multi-answer with FA
            num_subs = random.randint(6, 12)
            for i in range(1, num_subs + 1):
                data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.75, 0.25])
            data[f'{q_str}_{num_subs}_FA'] = [random.choice(['Additional option', 'Custom choice', None, None]) 
                                              for _ in range(num_respondents)]
        elif q % 3 == 0:  # Multi-answer
            num_subs = random.randint(5, 10)
            for i in range(1, num_subs + 1):
                data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.8, 0.2])
        else:  # Single answer
            has_fa = q % 5 == 1
            num_opts = random.randint(4, 8)
            
            for i in range(1, num_opts + 1):
                data[f'{q_str}_{i}'] = [0] * num_respondents
            
            if has_fa:
                data[f'{q_str}_{num_opts}_FA'] = [None] * num_respondents
            
            for idx in range(num_respondents):
                chosen = np.random.randint(1, num_opts + 1)
                data[f'{q_str}_{chosen}'][idx] = 1
                if has_fa and chosen == num_opts:
                    data[f'{q_str}_{num_opts}_FA'][idx] = random.choice([
                        'Custom response', 'Special case', 'Alternative option', None
                    ])
    
    # Add timestamp column
    base_dates = [
        datetime(2025, 2, 1, 10, 0, 0),  # February
        datetime(2025, 3, 1, 11, 0, 0),  # March  
        datetime(2025, 4, 1, 9, 30, 0),  # April
        datetime(2025, 5, 1, 14, 0, 0),  # May
    ]
    base_date = random.choice(base_dates)
    
    data['Response_DateTime'] = [base_date + timedelta(
        days=random.randint(0, 15),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    ) for _ in range(num_respondents)]
    
    # Create DataFrame with proper column ordering
    df = pd.DataFrame(data)
    cols = ['NO'] + [col for col in sorted(df.columns) if col.startswith('Q-')] + ['Response_DateTime']
    df = df[cols]
    
    return df

def create_survey_file(survey_name, survey_type, num_respondents=156):
    """Create a complete survey Excel file"""
    
    print(f"Creating {survey_name}...")
    
    question_master = create_question_master_sheet(survey_type)
    survey_data = create_survey_data_sheet(num_respondents, survey_type)
    
    # Save to Excel
    output_file = f'{survey_name}.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        question_master.to_excel(writer, sheet_name='Question_Master', index=False)
        survey_data.to_excel(writer, sheet_name='Data', index=False)
        
        # Format sheets
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"✅ Created {output_file} ({survey_data.shape[0]} respondents, {survey_data.shape[1]} columns)")
    return output_file

def main():
    """Create 4 different survey files"""
    
    print("Creating 4 Internet Survey Excel files...")
    print("="*60)
    
    surveys = [
        ("Product_Satisfaction_Survey_2025", "product", 145),
        ("Service_Quality_Survey_2025", "service", 172), 
        ("Website_Usability_Survey_2025", "website", 138),
        ("Marketing_Effectiveness_Survey_2025", "marketing", 164)
    ]
    
    created_files = []
    
    for survey_name, survey_type, num_resp in surveys:
        file_path = create_survey_file(survey_name, survey_type, num_resp)
        created_files.append(file_path)
        print()
    
    print("="*60)
    print("✅ All survey files created successfully!")
    print("\nFiles created:")
    for i, file_path in enumerate(created_files, 1):
        print(f"{i}. {file_path}")
    
    print("\nEach file contains:")
    print("- Question_Master sheet with question structure")
    print("- Data sheet with binary column structure for single answers")
    print("- Different survey themes and response counts")
    print("- Proper handling of free answer fields")

if __name__ == "__main__":
    main()