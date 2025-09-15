import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Define standard demographic questions that will be same across all surveys
STANDARD_DEMOGRAPHICS = {
    'Q-001': {
        'question': 'Please tell us your age and gender',
        'type': 'S/A',
        'requirement': 'Required',
        'options': [
            '1. Male 18-24',
            '2. Male 25-34', 
            '3. Male 35-44',
            '4. Male 45-54',
            '5. Male 55-64',
            '6. Male 65+',
            '7. Female 18-24',
            '8. Female 25-34',
            '9. Female 35-44', 
            '10. Female 45-54',
            '11. Female 55-64',
            '12. Female 65+'
        ]
    },
    'Q-002': {
        'question': 'What is your annual household income?',
        'type': 'S/A',
        'requirement': 'Optional',
        'options': [
            '1. Less than $25,000',
            '2. $25,000 - $40,000',
            '3. $40,000 - $60,000',
            '4. $60,000 - $80,000',
            '5. $80,000 - $100,000',
            '6. $100,000 - $150,000',
            '7. More than $150,000',
            '8. Prefer not to answer'
        ]
    },
    'Q-003': {
        'question': 'What is your highest level of education?',
        'type': 'S/A',
        'requirement': 'Required',
        'options': [
            '1. High school or less',
            '2. Some college/Associate degree',
            '3. Bachelor degree',
            '4. Master degree',
            '5. Doctorate/PhD',
            '6. Professional degree',
            '7. Other'
        ]
    },
    'Q-004': {
        'question': 'What is your employment status?',
        'type': 'S/A',
        'requirement': 'Required',
        'options': [
            '1. Full-time employed',
            '2. Part-time employed',
            '3. Self-employed',
            '4. Student',
            '5. Homemaker',
            '6. Retired',
            '7. Unemployed',
            '8. Other'
        ]
    },
    'Q-005': {
        'question': 'Which region do you live in?',
        'type': 'S/A',
        'requirement': 'Required',
        'options': [
            '1. North America',
            '2. South America',
            '3. Europe',
            '4. Asia Pacific',
            '5. Middle East',
            '6. Africa',
            '7. Other'
        ]
    }
}

def create_question_master_sheet(survey_theme="general"):
    """Create question master sheet with consistent demographics + theme-specific questions"""
    
    questions_data = []
    
    # Add standard demographic questions (Q-001 to Q-005)
    for q_id, q_info in STANDARD_DEMOGRAPHICS.items():
        questions_data.append([q_id, q_info['requirement'], q_info['question'], q_info['type']])
        for option in q_info['options']:
            questions_data.append(['', '', option, ''])
        questions_data.append(['', '', '', ''])
    
    # Add theme-specific questions starting from Q-006
    if survey_theme == "retail":
        # Retail/Shopping survey
        theme_questions = [
            ('Q-006', 'Required', 'How often do you shop online?', 'S/A', [
                '1. Daily', '2. Weekly', '3. Monthly', '4. Quarterly', '5. Rarely', '6. Never'
            ]),
            ('Q-007', 'Required', 'What do you primarily shop for online?', 'S/A+FA', [
                '1. Clothing & Fashion', '2. Electronics', '3. Books & Media', '4. Home & Garden',
                '5. Food & Groceries', '6. Health & Beauty', '7. Sports & Outdoors', '8. Toys & Games',
                '9. Automotive', '10. Other (Please specify)'
            ]),
            ('Q-008', 'Required', 'Which payment methods do you prefer?', 'M/A', [
                '1. Credit card', '2. Debit card', '3. PayPal', '4. Apple Pay', '5. Google Pay',
                '6. Bank transfer', '7. Cash on delivery', '8. Buy now pay later', '9. Cryptocurrency'
            ]),
        ]
    elif survey_theme == "healthcare":
        # Healthcare survey
        theme_questions = [
            ('Q-006', 'Required', 'How often do you visit healthcare providers?', 'S/A', [
                '1. Weekly', '2. Monthly', '3. Every 3 months', '4. Every 6 months', 
                '5. Annually', '6. Only when sick', '7. Rarely'
            ]),
            ('Q-007', 'Required', 'Which healthcare services have you used in the past year?', 'M/A', [
                '1. Primary care physician', '2. Specialist consultation', '3. Emergency room',
                '4. Urgent care', '5. Dental care', '6. Mental health services', '7. Physical therapy',
                '8. Laboratory tests', '9. Imaging services', '10. Pharmacy services'
            ]),
            ('Q-008', 'Optional', 'What type of health insurance do you have?', 'S/A', [
                '1. Employer-sponsored', '2. Individual plan', '3. Government plan (Medicare/Medicaid)',
                '4. No insurance', '5. Other', '6. Prefer not to answer'
            ]),
        ]
    elif survey_theme == "technology":
        # Technology survey
        theme_questions = [
            ('Q-006', 'Required', 'Which devices do you use daily?', 'M/A', [
                '1. Smartphone', '2. Laptop', '3. Desktop computer', '4. Tablet',
                '5. Smart watch', '6. Smart TV', '7. Gaming console', '8. Smart home devices'
            ]),
            ('Q-007', 'Required', 'What is your primary operating system?', 'S/A', [
                '1. Windows', '2. macOS', '3. iOS', '4. Android', '5. Linux', '6. Other'
            ]),
            ('Q-008', 'Required', 'How would you rate your technology expertise?', 'S/A', [
                '1. Beginner', '2. Basic', '3. Intermediate', '4. Advanced', '5. Expert'
            ]),
        ]
    elif survey_theme == "food":
        # Food & Dining survey
        theme_questions = [
            ('Q-006', 'Required', 'How often do you dine out per week?', 'S/A', [
                '1. Never', '2. Once', '3. 2-3 times', '4. 4-5 times', 
                '5. 6-7 times', '6. More than 7 times'
            ]),
            ('Q-007', 'Required', 'What types of cuisine do you prefer?', 'M/A+FA', [
                '1. American', '2. Italian', '3. Chinese', '4. Japanese', '5. Mexican',
                '6. Indian', '7. French', '8. Thai', '9. Mediterranean', '10. Korean',
                '11. Other (Please specify)'
            ]),
            ('Q-008', 'Required', 'What factors influence your restaurant choice?', 'M/A', [
                '1. Price', '2. Food quality', '3. Service quality', '4. Location',
                '5. Atmosphere', '6. Reviews/ratings', '7. Menu variety', '8. Healthy options',
                '9. Speed of service', '10. Parking availability'
            ]),
        ]
    else:  # travel
        # Travel survey
        theme_questions = [
            ('Q-006', 'Required', 'How often do you travel for leisure per year?', 'S/A', [
                '1. Never', '2. Once', '3. 2-3 times', '4. 4-5 times', 
                '5. 6-10 times', '6. More than 10 times'
            ]),
            ('Q-007', 'Required', 'What type of accommodation do you prefer?', 'S/A+FA', [
                '1. Hotels', '2. Vacation rentals (Airbnb)', '3. Hostels', '4. Resorts',
                '5. Camping', '6. Staying with friends/family', '7. Bed & Breakfast',
                '8. Other (Please specify)'
            ]),
            ('Q-008', 'Required', 'How do you typically book your travel?', 'M/A', [
                '1. Online travel sites (Expedia, Booking.com)', '2. Airline websites directly',
                '3. Travel agent', '4. Hotel websites directly', '5. Mobile apps',
                '6. Phone reservations', '7. Walk-in bookings'
            ]),
        ]
    
    # Add theme-specific questions
    for q_id, requirement, question, q_type, options in theme_questions:
        questions_data.append([q_id, requirement, question, q_type])
        for option in options:
            questions_data.append(['', '', option, ''])
        questions_data.append(['', '', '', ''])
    
    # Add common satisfaction questions Q-009 to Q-013
    satisfaction_questions = [
        ('Q-009', 'Required', 'Rate your overall satisfaction', 'S/A', [
            '1. Very Dissatisfied', '2. Dissatisfied', '3. Neutral', 
            '4. Satisfied', '5. Very Satisfied'
        ]),
        ('Q-010', 'Required', 'Rate the value for money', 'S/A', [
            '1. Very Poor', '2. Poor', '3. Fair', '4. Good', '5. Excellent'
        ]),
        ('Q-011', 'Required', 'Rate the quality of service/product', 'S/A', [
            '1. Very Poor', '2. Poor', '3. Fair', '4. Good', '5. Excellent'
        ]),
        ('Q-012', 'Required', 'Would you recommend us to others?', 'S/A', [
            '1. Definitely not', '2. Probably not', '3. Might or might not',
            '4. Probably yes', '5. Definitely yes'
        ]),
        ('Q-013', 'Optional', 'What improvements would you suggest?', 'FA', [
            '(Open text response)'
        ])
    ]
    
    for q_id, requirement, question, q_type, options in satisfaction_questions:
        questions_data.append([q_id, requirement, question, q_type])
        for option in options:
            questions_data.append(['', '', option, ''])
        questions_data.append(['', '', '', ''])
    
    # Add more questions Q-014 to Q-086 with mixed types
    for q in range(14, 87):
        q_num = f'Q-{str(q).zfill(3)}'
        
        if q % 8 == 0:  # Free answer questions
            questions_data.extend([
                [q_num, 'Optional', f'Please share your experience with topic {q}', 'FA'],
                ['', '', '(Open text response)', ''],
                ['', '', '', '']
            ])
        elif q % 5 == 0:  # Multi-answer with FA
            questions_data.append([q_num, 'Optional', f'Select all relevant items for category {q}', 'M/A+FA'])
            num_opts = random.randint(8, 15)
            for i in range(1, num_opts):
                questions_data.append(['', '', f'{i}. Option {i} for Q{q}', ''])
            questions_data.append(['', '', f'{num_opts}. Other (Please specify)', ''])
            questions_data.append(['', '', '', ''])
        elif q % 3 == 0:  # Multi-answer
            questions_data.append([q_num, 'Required' if q % 2 == 0 else 'Optional', 
                                 f'Choose all applicable items for area {q}', 'M/A'])
            num_opts = random.randint(6, 12)
            for i in range(1, num_opts + 1):
                questions_data.append(['', '', f'{i}. Choice {i}', ''])
            questions_data.append(['', '', '', ''])
        else:  # Single answer
            has_fa = q % 7 == 1
            questions_data.append([q_num, 'Required' if q % 2 == 0 else 'Optional', 
                                 f'Please evaluate aspect {q}', 'S/A+FA' if has_fa else 'S/A'])
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

def create_survey_data_sheet(num_respondents=156, survey_theme="general"):
    """Create survey response data with consistent demographic structure"""
    
    np.random.seed(random.randint(1, 2000))
    data = {}
    
    # NO column (different ranges for each survey)
    base_ids = {
        'retail': 300000,
        'healthcare': 400000, 
        'technology': 500000,
        'food': 600000,
        'travel': 700000
    }
    base_id = base_ids.get(survey_theme, 100000)
    data['NO'] = [base_id + i * 1234 for i in range(num_respondents)]
    
    # Standard demographic questions Q-001 to Q-005 (same structure for all)
    demo_questions = ['Q-001', 'Q-002', 'Q-003', 'Q-004', 'Q-005']
    demo_options = [12, 8, 7, 8, 7]  # Number of options for each demo question
    demo_fa_questions = ['Q-003', 'Q-004']  # Questions with "Other" option needing FA
    
    for i, (q_id, num_opts) in enumerate(zip(demo_questions, demo_options)):
        # Create binary columns
        for opt in range(1, num_opts + 1):
            data[f'{q_id}_{opt}'] = [0] * num_respondents
        
        # Add FA column for questions with "Other" option
        if q_id in demo_fa_questions:
            if q_id == 'Q-003':
                data[f'{q_id}_7_SA'] = [None] * num_respondents
            elif q_id == 'Q-004':
                data[f'{q_id}_8_SA'] = [None] * num_respondents
        
        # Fill data
        for idx in range(num_respondents):
            chosen = np.random.randint(1, num_opts + 1)
            data[f'{q_id}_{chosen}'][idx] = 1
            
            # Fill FA if applicable
            if q_id == 'Q-003' and chosen == 7:
                data[f'{q_id}_7_SA'][idx] = random.choice([
                    'Vocational training', 'Military training', 'Online certification'
                ])
            elif q_id == 'Q-004' and chosen == 8:
                data[f'{q_id}_8_SA'][idx] = random.choice([
                    'Consultant', 'Freelancer', 'Contractor', 'Entrepreneur'
                ])
    
    # Theme-specific questions Q-006 to Q-008
    if survey_theme == "retail":
        # Q-006: Shopping frequency (6 options)
        for i in range(1, 7):
            data[f'Q-006_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 7)
            data[f'Q-006_{chosen}'][idx] = 1
            
        # Q-007: Shopping categories (10 options with FA)
        for i in range(1, 11):
            data[f'Q-007_{i}'] = [0] * num_respondents
        data['Q-007_10_SA'] = [None] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 11)
            data[f'Q-007_{chosen}'][idx] = 1
            if chosen == 10:
                data['Q-007_10_SA'][idx] = random.choice([
                    'Office supplies', 'Pet supplies', 'Arts & crafts'
                ])
        
        # Q-008: Payment methods (9 options, multi-answer)
        for i in range(1, 10):
            data[f'Q-008_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.7, 0.3])
            
    elif survey_theme == "healthcare":
        # Q-006: Visit frequency (7 options)
        for i in range(1, 8):
            data[f'Q-006_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 8)
            data[f'Q-006_{chosen}'][idx] = 1
            
        # Q-007: Services used (10 options, multi-answer)
        for i in range(1, 11):
            data[f'Q-007_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.6, 0.4])
            
        # Q-008: Insurance type (6 options)
        for i in range(1, 7):
            data[f'Q-008_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 7)
            data[f'Q-008_{chosen}'][idx] = 1
            
    elif survey_theme == "technology":
        # Q-006: Daily devices (8 options, multi-answer)
        for i in range(1, 9):
            data[f'Q-006_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.4, 0.6])
            
        # Q-007: Primary OS (6 options)
        for i in range(1, 7):
            data[f'Q-007_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 7)
            data[f'Q-007_{chosen}'][idx] = 1
            
        # Q-008: Tech expertise (5 options)
        for i in range(1, 6):
            data[f'Q-008_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 6)
            data[f'Q-008_{chosen}'][idx] = 1
            
    elif survey_theme == "food":
        # Q-006: Dining frequency (6 options)
        for i in range(1, 7):
            data[f'Q-006_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 7)
            data[f'Q-006_{chosen}'][idx] = 1
            
        # Q-007: Cuisine preferences (11 options with FA)
        for i in range(1, 12):
            data[f'Q-007_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.7, 0.3])
        data['Q-007_11_FA'] = [random.choice([
            'Vietnamese', 'German', 'Brazilian', None, None
        ]) for _ in range(num_respondents)]
        
        # Q-008: Choice factors (10 options, multi-answer)
        for i in range(1, 11):
            data[f'Q-008_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.6, 0.4])
            
    else:  # travel
        # Q-006: Travel frequency (6 options)
        for i in range(1, 7):
            data[f'Q-006_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 7)
            data[f'Q-006_{chosen}'][idx] = 1
            
        # Q-007: Accommodation preferences (8 options with FA)
        for i in range(1, 9):
            data[f'Q-007_{i}'] = [0] * num_respondents
        data['Q-007_8_SA'] = [None] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 9)
            data[f'Q-007_{chosen}'][idx] = 1
            if chosen == 8:
                data['Q-007_8_SA'][idx] = random.choice([
                    'Cruise ships', 'RV/Motorhome', 'House sitting'
                ])
        
        # Q-008: Booking methods (7 options, multi-answer)
        for i in range(1, 8):
            data[f'Q-008_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.7, 0.3])
    
    # Common satisfaction questions Q-009 to Q-012 (same for all surveys)
    for q in range(9, 13):
        q_str = f'Q-{str(q).zfill(3)}'
        for i in range(1, 6):
            data[f'{q_str}_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 6)
            data[f'{q_str}_{chosen}'][idx] = 1
    
    # Q-013: Free answer question (same for all)
    data['Q-013'] = [random.choice([
        'Great service overall', 'Could improve response time', 'Very satisfied',
        'Good value for money', 'Excellent quality', 'Professional staff',
        'Easy to use', 'Reliable service', None, None, None
    ]) for _ in range(num_respondents)]
    
    # Q-014 to Q-086: Mixed question types
    for q in range(14, 87):
        q_str = f'Q-{str(q).zfill(3)}'
        
        if q % 8 == 0:  # Free answer
            data[q_str] = [random.choice([
                'Very positive experience', 'Room for improvement', 'Meets expectations',
                'Outstanding service', 'Good quality', None, None, None
            ]) for _ in range(num_respondents)]
        elif q % 5 == 0:  # Multi-answer with FA
            num_subs = random.randint(8, 15)
            for i in range(1, num_subs + 1):
                data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.8, 0.2])
            data[f'{q_str}_{num_subs}_FA'] = [random.choice([
                'Additional requirement', 'Custom solution', None, None
            ]) for _ in range(num_respondents)]
        elif q % 3 == 0:  # Multi-answer
            num_subs = random.randint(6, 12)
            for i in range(1, num_subs + 1):
                data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.75, 0.25])
        else:  # Single answer
            has_fa = q % 7 == 1
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
                        'Special case', 'Alternative option', None
                    ])
    
    # Add timestamp
    base_dates = {
        'retail': datetime(2025, 1, 15, 10, 0, 0),
        'healthcare': datetime(2025, 2, 1, 11, 30, 0),
        'technology': datetime(2025, 2, 15, 14, 0, 0),
        'food': datetime(2025, 3, 1, 12, 0, 0),
        'travel': datetime(2025, 3, 15, 16, 30, 0)
    }
    base_date = base_dates.get(survey_theme, datetime(2025, 1, 1, 9, 0, 0))
    
    data['Response_DateTime'] = [base_date + timedelta(
        days=random.randint(0, 20),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    ) for _ in range(num_respondents)]
    
    # Create DataFrame with proper column ordering
    df = pd.DataFrame(data)
    cols = ['NO'] + [col for col in sorted(df.columns) if col.startswith('Q-')] + ['Response_DateTime']
    df = df[cols]
    
    return df

def create_survey_file(survey_name, survey_theme, num_respondents):
    """Create a complete survey Excel file with consistent structure"""
    
    print(f"Creating {survey_name}...")
    
    question_master = create_question_master_sheet(survey_theme)
    survey_data = create_survey_data_sheet(num_respondents, survey_theme)
    
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
    """Create 5 survey files with consistent demographic structure"""
    
    print("Creating 5 Internet Survey Excel files with consistent structure...")
    print("="*70)
    
    surveys = [
        ("Retail_Shopping_Survey_2025", "retail", 148),
        ("Healthcare_Experience_Survey_2025", "healthcare", 165),
        ("Technology_Usage_Survey_2025", "technology", 139),
        ("Food_Dining_Survey_2025", "food", 157),
        ("Travel_Preferences_Survey_2025", "travel", 143)
    ]
    
    created_files = []
    
    print("All surveys will have identical demographic questions Q-001 to Q-005:")
    print("  Q-001: Age and Gender (12 options)")
    print("  Q-002: Annual Household Income (8 options)")
    print("  Q-003: Education Level (7 options)")
    print("  Q-004: Employment Status (8 options)")
    print("  Q-005: Geographic Region (7 options)")
    print("  Q-009-Q-013: Common satisfaction questions")
    print()
    
    for survey_name, survey_theme, num_resp in surveys:
        file_path = create_survey_file(survey_name, survey_theme, num_resp)
        created_files.append(file_path)
        print()
    
    print("="*70)
    print("✅ All 5 survey files created successfully!")
    print("\nFiles created:")
    for i, file_path in enumerate(created_files, 1):
        print(f"{i}. {file_path}")
    
    print("\n🎯 Key features:")
    print("✓ Consistent Q-001 to Q-005 demographic questions across all surveys")
    print("✓ Theme-specific questions Q-006 to Q-008 for each survey")
    print("✓ Common satisfaction questions Q-009 to Q-013")
    print("✓ Binary column structure for Single Answer questions")
    print("✓ Proper handling of Multi Answer and Free Answer questions")
    print("✓ Different respondent counts and timestamps for each survey")

if __name__ == "__main__":
    main()