import pandas as pd
import os

def extract_questions_from_survey(survey_file):
    """Extract questions from survey file's Question_Master sheet"""
    try:
        # Read the Question_Master sheet
        df = pd.read_excel(survey_file, sheet_name='Question_Master')
        
        questions = []
        current_question = None
        
        for _, row in df.iterrows():
            question_id = str(row['Question_ID']).strip()
            question_text = str(row['Question_Text']).strip()
            
            # If we have a question ID (not empty), this is a new question
            if question_id and question_id != 'nan' and question_id.startswith('Q-'):
                current_question = question_text
                questions.append(current_question)
        
        return questions
    
    except Exception as e:
        print(f"Error reading {survey_file}: {e}")
        return []

def main():
    """Extract questions from all survey files"""
    
    survey_files = [
        "Automotive_Vehicle_Survey_2025.xlsx",
        "Fitness_Health_Survey_2025.xlsx", 
        "Entertainment_Media_Survey_2025.xlsx",
        "Education_Learning_Survey_2025.xlsx",
        "Environmental_Awareness_Survey_2025.xlsx"
    ]
    
    all_questions = {}
    
    for survey_file in survey_files:
        if os.path.exists(survey_file):
            print(f"Extracting questions from {survey_file}...")
            questions = extract_questions_from_survey(survey_file)
            all_questions[survey_file] = questions
            print(f"Found {len(questions)} questions")
            
            # Show first 15 questions
            print("First 15 questions:")
            for i, q in enumerate(questions[:15], 1):
                print(f"  Q-{str(i).zfill(3)}: {q}")
            print("\n" + "-"*60 + "\n")
        else:
            print(f"File not found: {survey_file}")
    
    return all_questions

if __name__ == "__main__":
    questions_data = main()