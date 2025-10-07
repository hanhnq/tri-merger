import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_question_master_sheet():
    """Create the question master sheet with various question types"""
    
    questions_data = []
    
    # Q-001: Age and Gender (S/A)
    questions_data.extend([
        ['Q-001', 'Required', 'Please tell us your age and gender', 'S/A'],
        ['', '', '1. Male 10-19', ''],
        ['', '', '2. Male 20-29', ''],
        ['', '', '3. Male 30-39', ''],
        ['', '', '4. Male 40-49', ''],
        ['', '', '5. Male 50-59', ''],
        ['', '', '6. Male 60+', ''],
        ['', '', '7. Female 10-19', ''],
        ['', '', '8. Female 20-29', ''],
        ['', '', '9. Female 30-39', ''],
        ['', '', '10. Female 40-49', ''],
        ['', '', '11. Female 50-59', ''],
        ['', '', '12. Female 60+', ''],
        ['', '', '', '']
    ])
    
    # Q-002: Region (S/A)
    questions_data.extend([
        ['Q-002', 'Required', 'Which region do you live in?', 'S/A'],
        ['', '', '1. North America', ''],
        ['', '', '2. South America', ''],
        ['', '', '3. Europe', ''],
        ['', '', '4. Asia', ''],
        ['', '', '5. Africa', ''],
        ['', '', '6. Oceania', ''],
        ['', '', '', '']
    ])
    
    # Q-003: Occupation (S/A)
    questions_data.extend([
        ['Q-003', 'Required', 'What is your occupation?', 'S/A'],
        ['', '', '1. Student', ''],
        ['', '', '2. Office Worker', ''],
        ['', '', '3. Self-employed', ''],
        ['', '', '4. Part-time Worker', ''],
        ['', '', '5. Homemaker', ''],
        ['', '', '6. Retired', ''],
        ['', '', '7. Unemployed', ''],
        ['', '', '8. Other', ''],
        ['', '', '', '']
    ])
    
    # Q-004: Income Level (S/A)
    questions_data.extend([
        ['Q-004', 'Optional', 'What is your annual household income?', 'S/A'],
        ['', '', '1. Less than $30,000', ''],
        ['', '', '2. $30,000 - $50,000', ''],
        ['', '', '3. $50,000 - $75,000', ''],
        ['', '', '4. $75,000 - $100,000', ''],
        ['', '', '5. $100,000 - $150,000', ''],
        ['', '', '6. More than $150,000', ''],
        ['', '', '7. Prefer not to answer', ''],
        ['', '', '', '']
    ])
    
    # Q-005: Marital Status (S/A)
    questions_data.extend([
        ['Q-005', 'Required', 'What is your marital status?', 'S/A'],
        ['', '', '1. Single', ''],
        ['', '', '2. Married', ''],
        ['', '', '3. Divorced', ''],
        ['', '', '4. Widowed', ''],
        ['', '', '5. Other', ''],
        ['', '', '', '']
    ])
    
    # Q-006-Q-009: Satisfaction Questions (S/A with scale)
    for i, topic in enumerate(['Product Quality', 'Customer Service', 'Price Value', 'Overall Experience'], start=6):
        q_num = f'Q-{str(i).zfill(3)}'
        questions_data.extend([
            [q_num, 'Required', f'How satisfied are you with our {topic}?', 'S/A'],
            ['', '', '1. Very Dissatisfied', ''],
            ['', '', '2. Dissatisfied', ''],
            ['', '', '3. Neutral', ''],
            ['', '', '4. Satisfied', ''],
            ['', '', '5. Very Satisfied', ''],
            ['', '', '', '']
        ])
    
    # Q-010: Favorite Features (M/A - Multi Answer)
    questions_data.extend([
        ['Q-010', 'Required', 'Which features do you use most? (Select all that apply)', 'M/A'],
        ['', '', '1. Email notifications', ''],
        ['', '', '2. Mobile app', ''],
        ['', '', '3. Dashboard analytics', ''],
        ['', '', '4. Report generation', ''],
        ['', '', '5. Data export', ''],
        ['', '', '6. User management', ''],
        ['', '', '7. API integration', ''],
        ['', '', '8. Custom themes', ''],
        ['', '', '9. Multi-language support', ''],
        ['', '', '10. Cloud storage', ''],
        ['', '', '11. Real-time collaboration', ''],
        ['', '', '12. Version control', ''],
        ['', '', '13. Security features', ''],
        ['', '', '14. Automated backups', ''],
        ['', '', '15. Search functionality', ''],
        ['', '', '16. Calendar integration', ''],
        ['', '', '17. Social media sharing', ''],
        ['', '', '18. Customer support chat', ''],
        ['', '', '19. Tutorial videos', ''],
        ['', '', '20. Documentation', ''],
        ['', '', '21. Community forum', ''],
        ['', '', '22. Plugin marketplace', ''],
        ['', '', '23. Other (Please specify)', ''],
        ['', '', '', '']
    ])
    
    # Q-011: Frequency of Use (S/A)
    questions_data.extend([
        ['Q-011', 'Required', 'How often do you use our service?', 'S/A'],
        ['', '', '1. Daily', ''],
        ['', '', '2. Several times a week', ''],
        ['', '', '3. Once a week', ''],
        ['', '', '4. Several times a month', ''],
        ['', '', '5. Once a month', ''],
        ['', '', '6. Less than once a month', ''],
        ['', '', '7. This is my first time', ''],
        ['', '', '', '']
    ])
    
    # Q-012: Problems Encountered (M/A with FA)
    questions_data.extend([
        ['Q-012', 'Optional', 'What problems have you encountered? (Select all that apply)', 'M/A+FA'],
        ['', '', '1. Slow loading times', ''],
        ['', '', '2. Bugs or errors', ''],
        ['', '', '3. Difficult navigation', ''],
        ['', '', '4. Missing features', ''],
        ['', '', '5. Poor mobile experience', ''],
        ['', '', '6. Security concerns', ''],
        ['', '', '7. High pricing', ''],
        ['', '', '8. Poor customer support', ''],
        ['', '', '9. Limited customization', ''],
        ['', '', '10. Integration issues', ''],
        ['', '', '11. Data loss', ''],
        ['', '', '12. Account problems', ''],
        ['', '', '13. Payment issues', ''],
        ['', '', '14. Language barriers', ''],
        ['', '', '15. Documentation unclear', ''],
        ['', '', '16. Training inadequate', ''],
        ['', '', '17. Performance issues', ''],
        ['', '', '18. Compatibility problems', ''],
        ['', '', '19. Update problems', ''],
        ['', '', '20. Notification issues', ''],
        ['', '', '21. Search not working', ''],
        ['', '', '22. Export problems', ''],
        ['', '', '23. Import problems', ''],
        ['', '', '24. Sync issues', ''],
        ['', '', '25. Display problems', ''],
        ['', '', '26. Permission errors', ''],
        ['', '', '27. Network issues', ''],
        ['', '', '28. Storage limitations', ''],
        ['', '', '29. Other (Please specify)', ''],
        ['', '', '', '']
    ])
    
    # Q-013: Overall Rating (S/A)
    questions_data.extend([
        ['Q-013', 'Required', 'Rate our service from 1-10', 'S/A'],
        ['', '', '1', ''],
        ['', '', '2', ''],
        ['', '', '3', ''],
        ['', '', '4', ''],
        ['', '', '5', ''],
        ['', '', '6', ''],
        ['', '', '7', ''],
        ['', '', '8', ''],
        ['', '', '9', ''],
        ['', '', '10', ''],
        ['', '', '', '']
    ])
    
    # Q-014-Q-017: Preference Questions with Other option
    preferences = [
        ('Q-014', 'Preferred payment method'),
        ('Q-015', 'Preferred contact method'),
        ('Q-016', 'Preferred device'),
        ('Q-017', 'Preferred time to use service')
    ]
    
    for q_num, topic in preferences:
        if 'payment' in topic:
            options = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cryptocurrency', 
                      'Apple Pay', 'Google Pay', 'Cash', 'Check', 'Invoice', 'Installments', 'Gift Card']
        elif 'contact' in topic:
            options = ['Email', 'Phone', 'SMS', 'In-app messaging', 'Live chat', 'Video call',
                      'Social media', 'Mail', 'In-person', 'Support ticket', 'Community forum', 'FAQ']
        elif 'device' in topic:
            options = ['Desktop PC', 'Laptop', 'Tablet', 'Smartphone', 'Smart TV', 'Gaming console',
                      'Smartwatch', 'Voice assistant', 'VR headset', 'E-reader', 'Kiosk', 'Other device']
        else:  # time
            options = ['Early morning (5-8am)', 'Morning (8-12pm)', 'Lunch (12-1pm)', 'Afternoon (1-5pm)',
                      'Evening (5-8pm)', 'Night (8-11pm)', 'Late night (11pm-2am)', 'Overnight (2-5am)',
                      'Weekdays only', 'Weekends only', 'Holidays', 'Anytime']
        
        questions_data.extend([[q_num, 'Required', topic, 'S/A+FA']])
        for i, opt in enumerate(options, 1):
            questions_data.append(['', '', f'{i}. {opt}', ''])
        questions_data.append(['', '', f'{len(options)+1}. Other (Please specify)', ''])
        questions_data.append(['', '', '', ''])
    
    # Q-018: How did you hear about us (S/A+FA)
    questions_data.extend([
        ['Q-018', 'Required', 'How did you hear about us?', 'S/A+FA'],
        ['', '', '1. Search engine', ''],
        ['', '', '2. Social media', ''],
        ['', '', '3. Friend/Family recommendation', ''],
        ['', '', '4. Online advertisement', ''],
        ['', '', '5. Email marketing', ''],
        ['', '', '6. Blog/Article', ''],
        ['', '', '7. YouTube', ''],
        ['', '', '8. Podcast', ''],
        ['', '', '9. Event/Conference', ''],
        ['', '', '10. Other (Please specify)', ''],
        ['', '', '', '']
    ])
    
    # Q-019-Q-022: Yes/No Questions
    yn_questions = [
        ('Q-019', 'Would you recommend our service to others?'),
        ('Q-020', 'Have you used similar services before?'),
        ('Q-021', 'Do you plan to continue using our service?'),
        ('Q-022', 'Have you contacted our support team?')
    ]
    
    for q_num, question in yn_questions:
        questions_data.extend([
            [q_num, 'Required', question, 'S/A'],
            ['', '', '1. Yes', ''],
            ['', '', '2. No', ''],
            ['', '', '', '']
        ])
    
    # Q-023-Q-025: Feature Importance (M/A)
    importance_topics = [
        ('Q-023', 'Which features are most important to you?', 20),
        ('Q-024', 'Which improvements would you like to see?', 18),
        ('Q-025', 'Which integrations do you need?', 9)
    ]
    
    for q_num, question, num_options in importance_topics:
        questions_data.append([q_num, 'Optional', question, 'M/A+FA' if q_num in ['Q-023', 'Q-024', 'Q-025'] else 'M/A'])
        
        if q_num == 'Q-023':
            options = ['Better performance', 'More features', 'Lower price', 'Better UI', 'Mobile app',
                      'More integrations', 'Better support', 'More languages', 'Better security', 'More storage',
                      'Faster loading', 'Better documentation', 'More customization', 'Better search',
                      'More templates', 'Better collaboration', 'More automation', 'Better analytics',
                      'More export options']
        elif q_num == 'Q-024':
            options = ['UI redesign', 'Speed optimization', 'New features', 'Bug fixes', 'Mobile improvements',
                      'Security updates', 'Price reduction', 'Support improvements', 'Documentation updates',
                      'Training materials', 'API enhancements', 'Integration expansion', 'Search improvements',
                      'Reporting tools', 'Collaboration features', 'Automation tools', 'Analytics dashboard']
        else:  # Q-025
            options = ['Google Workspace', 'Microsoft 365', 'Slack', 'Zoom', 'Salesforce', 'Dropbox',
                      'GitHub', 'Jira']
        
        for i, opt in enumerate(options, 1):
            questions_data.append(['', '', f'{i}. {opt}', ''])
        questions_data.append(['', '', f'{num_options}. Other (Please specify)', ''])
        questions_data.append(['', '', '', ''])
    
    # Add more questions to reach similar count as original (up to Q-086)
    # Adding various question types for diversity
    
    # Q-026-Q-086: Mix of different question types
    for i in range(26, 87):
        q_num = f'Q-{str(i).zfill(3)}'
        
        if i % 5 == 0:  # Every 5th question is Free Answer
            questions_data.extend([
                [q_num, 'Optional', f'Please provide your feedback on aspect {i}', 'FA'],
                ['', '', '(Free text answer)', ''],
                ['', '', '', '']
            ])
        elif i % 3 == 0:  # Every 3rd question is Multi Answer
            questions_data.append([q_num, 'Optional', f'Select all that apply for category {i}', 'M/A'])
            num_opts = random.randint(5, 15)
            for j in range(1, num_opts):
                questions_data.append(['', '', f'{j}. Option {j}', ''])
            questions_data.append(['', '', f'{num_opts}. Other', ''])
            questions_data.append(['', '', '', ''])
        else:  # Single Answer
            questions_data.append([q_num, 'Required' if i % 2 == 0 else 'Optional', 
                                 f'Please rate aspect {i}', 'S/A'])
            for j in range(1, 6):
                questions_data.append(['', '', f'{j}. Level {j}', ''])
            questions_data.append(['', '', '', ''])
    
    # Create DataFrame
    df = pd.DataFrame(questions_data, columns=['Question_ID', 'Requirement', 'Question_Text', 'Type'])
    return df

def create_survey_data_sheet(num_respondents=156):
    """Create the survey response data sheet"""
    
    np.random.seed(42)  # For reproducibility
    data = {}
    
    # NO column (respondent ID)
    data['NO'] = [100000 + i * 1111 for i in range(num_respondents)]
    
    # Q-001: Age and Gender (12 options) - Single Answer stored as binary columns
    for i in range(1, 13):
        data[f'Q-001_{i}'] = [0] * num_respondents
    # Set one option to 1 for each respondent
    for idx in range(num_respondents):
        chosen = np.random.randint(1, 13)
        data[f'Q-001_{chosen}'][idx] = 1
    
    # Q-002: Region (6 options) - Single Answer stored as binary columns
    for i in range(1, 7):
        data[f'Q-002_{i}'] = [0] * num_respondents
    for idx in range(num_respondents):
        chosen = np.random.randint(1, 7)
        data[f'Q-002_{chosen}'][idx] = 1
    
    # Q-003: Occupation (8 options) - Single Answer with "Other" having free text
    for i in range(1, 9):
        data[f'Q-003_{i}'] = [0] * num_respondents
    data['Q-003_8_SA'] = [None] * num_respondents  # Free text for "Other" option
    for idx in range(num_respondents):
        chosen = np.random.randint(1, 9)
        data[f'Q-003_{chosen}'][idx] = 1
        if chosen == 8:  # If "Other" is selected
            data['Q-003_8_SA'][idx] = random.choice(['Consultant', 'Freelancer', 'Artist', 'Entrepreneur', 'Researcher'])
    
    # Q-004: Income (7 options) - Single Answer stored as binary columns
    for i in range(1, 8):
        data[f'Q-004_{i}'] = [0] * num_respondents
    for idx in range(num_respondents):
        chosen = np.random.randint(1, 8)
        data[f'Q-004_{chosen}'][idx] = 1
    
    # Q-005: Marital Status (5 options) - Single Answer with "Other" having free text
    for i in range(1, 6):
        data[f'Q-005_{i}'] = [0] * num_respondents
    data['Q-005_5_SA'] = [None] * num_respondents  # Free text for "Other" option
    for idx in range(num_respondents):
        chosen = np.random.randint(1, 6)
        data[f'Q-005_{chosen}'][idx] = 1
        if chosen == 5:  # If "Other" is selected
            data['Q-005_5_SA'][idx] = random.choice(['Engaged', 'Separated', 'Common-law'])
    
    # Q-006 to Q-009: Satisfaction (5 options each) - Single Answer stored as binary columns
    for q in range(6, 10):
        for i in range(1, 6):
            data[f'Q-{str(q).zfill(3)}_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 6)
            data[f'Q-{str(q).zfill(3)}_{chosen}'][idx] = 1
    
    # Q-010: Multi-answer (23 sub-questions)
    for i in range(1, 24):
        data[f'Q-010_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.7, 0.3])
    # Free answer for Q-010_23
    data['Q-010_23_FA'] = [random.choice(['Custom feature', 'API needs', 'Special request', None, None, None]) 
                           for _ in range(num_respondents)]
    
    # Q-011: Frequency (7 options) - Single Answer stored as binary columns
    for i in range(1, 8):
        data[f'Q-011_{i}'] = [0] * num_respondents
    for idx in range(num_respondents):
        chosen = np.random.randint(1, 8)
        data[f'Q-011_{chosen}'][idx] = 1
    
    # Q-012: Multi-answer with FA (29 sub-questions)
    for i in range(1, 30):
        data[f'Q-012_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.8, 0.2])
    data['Q-012_29_FA'] = [random.choice(['Technical issue', 'UI problem', None, None, None]) 
                           for _ in range(num_respondents)]
    
    # Q-013: Rating 1-10 - Single Answer stored as binary columns
    for i in range(1, 11):
        data[f'Q-013_{i}'] = [0] * num_respondents
    for idx in range(num_respondents):
        chosen = np.random.randint(1, 11)
        data[f'Q-013_{chosen}'][idx] = 1
    
    # Q-014 to Q-017: Single answer with FA option (13 options each)
    for q in range(14, 18):
        q_str = f'Q-{str(q).zfill(3)}'
        for i in range(1, 14):
            data[f'{q_str}_{i}'] = [0] * num_respondents
        data[f'{q_str}_13_FA'] = [None] * num_respondents
        
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 14)
            data[f'{q_str}_{chosen}'][idx] = 1
            if chosen == 13:  # If "Other" is selected
                data[f'{q_str}_13_FA'][idx] = random.choice(['Custom option', 'Special case', 'Alternative'])
    
    # Q-018: How heard about us with FA (10 options)
    for i in range(1, 11):
        data[f'Q-018_{i}'] = [0] * num_respondents
    data['Q-018_10_FA'] = [None] * num_respondents
    for idx in range(num_respondents):
        chosen = np.random.randint(1, 11)
        data[f'Q-018_{chosen}'][idx] = 1
        if chosen == 10:  # If "Other" is selected
            data['Q-018_10_FA'][idx] = random.choice(['Conference', 'Partner', 'Word of mouth'])
    
    # Q-019 to Q-022: Yes/No questions (2 options each)
    for q in range(19, 23):
        q_str = f'Q-{str(q).zfill(3)}'
        for i in range(1, 3):
            data[f'{q_str}_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.choice([1, 2])
            data[f'{q_str}_{chosen}'][idx] = 1
    
    # Q-023 to Q-025: Multi-answer questions
    for q in [23, 24, 25]:
        q_str = f'Q-{str(q).zfill(3)}'
        num_subs = 20 if q == 23 else (18 if q == 24 else 9)
        for i in range(1, num_subs + 1):
            data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.75, 0.25])
        data[f'{q_str}_{num_subs}_FA'] = [random.choice(['Additional need', None, None, None]) 
                                          for _ in range(num_respondents)]
    
    # Q-026 to Q-086: Mixed question types
    for q in range(26, 87):
        q_str = f'Q-{str(q).zfill(3)}'
        
        if q % 5 == 0:  # Free answer questions
            data[q_str] = [random.choice(['Great service', 'Needs improvement', 'Satisfied', 
                                        'Good value', 'Excellent', None, None]) 
                          for _ in range(num_respondents)]
        elif q % 3 == 0:  # Multi-answer questions
            num_subs = random.randint(5, 15)
            for i in range(1, num_subs + 1):
                data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.8, 0.2])
            data[f'{q_str}_{num_subs}_FA'] = [random.choice(['Other option', None, None, None]) 
                                              for _ in range(num_respondents)]
        else:  # Single answer (1-5 scale) stored as binary columns
            for i in range(1, 6):
                data[f'{q_str}_{i}'] = [0] * num_respondents
            for idx in range(num_respondents):
                chosen = np.random.randint(1, 6)
                data[f'{q_str}_{chosen}'][idx] = 1
    
    # Add timestamp column
    base_date = datetime(2025, 1, 1, 9, 0, 0)
    data['Response_DateTime'] = [base_date + timedelta(
        days=random.randint(0, 10),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    ) for _ in range(num_respondents)]
    
    # Create DataFrame with all columns
    df = pd.DataFrame(data)
    
    # Reorder columns to match the pattern (NO, Q-xxx columns, timestamp)
    cols = ['NO'] + [col for col in sorted(df.columns) if col.startswith('Q-')] + ['Response_DateTime']
    df = df[cols]
    
    return df

def main():
    print("Creating Internet Survey Excel file...")
    print("="*60)
    
    # Create both sheets
    question_master = create_question_master_sheet()
    survey_data = create_survey_data_sheet()
    
    print(f"✓ Created Question Master sheet: {question_master.shape[0]} rows x {question_master.shape[1]} columns")
    print(f"✓ Created Survey Data sheet: {survey_data.shape[0]} rows x {survey_data.shape[1]} columns")
    
    # Save to Excel
    output_file = 'Internet_Survey_Correct_Structure.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write sheets
        question_master.to_excel(writer, sheet_name='Question_Master', index=False)
        survey_data.to_excel(writer, sheet_name='Data', index=False)
        
        # Format sheets
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                
                # Set width (max 50 characters)
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print("\n" + "="*60)
    print(f"✅ Successfully created '{output_file}'")
    print("\nFile structure:")
    print("1. Question_Master sheet:")
    print("   - Question_ID: Question codes (Q-001 to Q-086)")
    print("   - Requirement: Required/Optional")
    print("   - Question_Text: The actual questions and answer options")
    print("   - Type: S/A (Single Answer), M/A (Multi Answer), M/A+FA (Multi with Free), FA (Free Answer)")
    print("\n2. Data sheet:")
    print(f"   - {survey_data.shape[0]} respondents")
    print(f"   - {survey_data.shape[1]} columns including all questions and sub-questions")
    print("   - Response timestamps included")

if __name__ == "__main__":
    main()