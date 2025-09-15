import pandas as pd

def create_automotive_client_settings():
    """Create client settings for automotive survey"""
    client_name = "AutoMotion Inc"
    questions = [
        "Please tell us your age and gender",
        "What is your annual household income?", 
        "What is your highest level of education?",
        "What is your employment status?",
        "Which region do you live in?",
        "How many vehicles does your household currently own?",
        "What type is your primary vehicle?",
        "Which car brands do you prefer?",
        "How often do you drive?",
        "What factors are most important when buying a car?",
        "Where do you prefer to service your vehicle?",
        "When do you plan to buy your next vehicle?",
        "How interested are you in electric vehicles?",
        "What are your biggest concerns about car ownership?",
        "What would make your driving experience better?"
    ]
    
    data = {
        'Client Name': [client_name] * len(questions),
        'Target Questions for Analysis': questions
    }
    
    return pd.DataFrame(data)

def create_fitness_client_settings():
    """Create client settings for fitness survey"""
    client_name = "FitLife Wellness"
    questions = [
        "Please tell us your age and gender",
        "What is your annual household income?",
        "What is your highest level of education?", 
        "What is your employment status?",
        "Which region do you live in?",
        "How often do you exercise or engage in physical activity?",
        "What types of physical activities do you enjoy?",
        "Where do you primarily work out?",
        "What are your primary fitness goals?",
        "What prevents you from exercising more?",
        "Do you track your fitness or health metrics?",
        "What fitness technology do you use?",
        "How important is nutrition in your fitness routine?",
        "Have you ever worked with fitness professionals?",
        "What motivates you most to stay active and healthy?"
    ]
    
    data = {
        'Client Name': [client_name] * len(questions),
        'Target Questions for Analysis': questions
    }
    
    return pd.DataFrame(data)

def create_entertainment_client_settings():
    """Create client settings for entertainment survey"""
    client_name = "StreamVibe Media"
    questions = [
        "Please tell us your age and gender",
        "What is your annual household income?",
        "What is your highest level of education?",
        "What is your employment status?", 
        "Which region do you live in?",
        "How many hours per day do you spend on entertainment?",
        "What are your favorite entertainment activities?",
        "Which streaming services do you subscribe to?",
        "What types of games do you enjoy?",
        "What music genres do you listen to most?",
        "How do you prefer to consume news and information?",
        "Which social media platforms do you use regularly?",
        "Do you create any content online?",
        "How much do you spend monthly on entertainment?",
        "What new entertainment trends interest you most?"
    ]
    
    data = {
        'Client Name': [client_name] * len(questions),
        'Target Questions for Analysis': questions
    }
    
    return pd.DataFrame(data)

def create_education_client_settings():
    """Create client settings for education survey"""
    client_name = "LearnForward Academy"
    questions = [
        "Please tell us your age and gender",
        "What is your annual household income?",
        "What is your highest level of education?",
        "What is your employment status?",
        "Which region do you live in?",
        "What motivates you to learn new things?",
        "How do you prefer to learn new skills?", 
        "What subjects are you most interested in learning?",
        "How much time do you dedicate to learning weekly?",
        "What prevents you from learning more?",
        "How important are certificates/credentials to you?",
        "Where do you learn most effectively?",
        "What devices do you use for learning?",
        "How do you apply newly learned skills?",
        "What would make online learning more effective for you?"
    ]
    
    data = {
        'Client Name': [client_name] * len(questions),
        'Target Questions for Analysis': questions
    }
    
    return pd.DataFrame(data)

def create_environment_client_settings():
    """Create client settings for environmental survey"""
    client_name = "EcoGreen Solutions"
    questions = [
        "Please tell us your age and gender",
        "What is your annual household income?",
        "What is your highest level of education?",
        "What is your employment status?",
        "Which region do you live in?", 
        "How concerned are you about environmental issues?",
        "What environmentally-friendly actions do you take?",
        "What environmental issues concern you most?",
        "When shopping, how important are eco-friendly options?",
        "What transportation methods do you use regularly?",
        "What steps do you take to reduce energy consumption?",
        "Where do you get environmental news and information?",
        "What prevents you from being more environmentally conscious?",
        "What environmental changes do you plan to make this year?",
        "What would motivate you to take more environmental action?"
    ]
    
    data = {
        'Client Name': [client_name] * len(questions),
        'Target Questions for Analysis': questions
    }
    
    return pd.DataFrame(data)

def create_client_settings_file(client_type, output_filename):
    """Create a client settings Excel file for specific client type"""
    
    if client_type == "automotive":
        df = create_automotive_client_settings()
    elif client_type == "fitness": 
        df = create_fitness_client_settings()
    elif client_type == "entertainment":
        df = create_entertainment_client_settings()
    elif client_type == "education":
        df = create_education_client_settings()
    else:  # environment
        df = create_environment_client_settings()
    
    # Save to Excel
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        
        # Format the sheet
        worksheet = writer.sheets['Sheet1']
        
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
            
            # Set width with reasonable limits
            adjusted_width = min(max_length + 2, 80)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    client_name = df['Client Name'].iloc[0]
    num_questions = len(df)
    print(f"✅ Created {output_filename} for client '{client_name}' with {num_questions} questions")
    
    return output_filename

def main():
    """Create 5 client settings files for different industries"""
    
    print("Creating 5 Client Settings files for different industries...")
    print("="*65)
    
    clients = [
        ("automotive", "AutoMotion_Client_Settings.xlsx"),
        ("fitness", "FitLife_Client_Settings.xlsx"), 
        ("entertainment", "StreamVibe_Client_Settings.xlsx"),
        ("education", "LearnForward_Client_Settings.xlsx"),
        ("environment", "EcoGreen_Client_Settings.xlsx")
    ]
    
    created_files = []
    
    for client_type, filename in clients:
        file_path = create_client_settings_file(client_type, filename)
        created_files.append(file_path)
        print()
    
    print("="*65)
    print("✅ All 5 client settings files created successfully!")
    print("\nFiles created:")
    for i, file_path in enumerate(created_files, 1):
        print(f"{i}. {file_path}")
    
    print("\n🎯 Client Settings Summary:")
    print("1. AutoMotion Inc - Automotive industry client")
    print("2. FitLife Wellness - Fitness & health industry client") 
    print("3. StreamVibe Media - Entertainment & media industry client")
    print("4. LearnForward Academy - Education & learning industry client")
    print("5. EcoGreen Solutions - Environmental & sustainability client")
    
    print("\n📋 Each file contains:")
    print("✓ Client name specific to the industry")
    print("✓ 15 target questions for analysis")
    print("✓ Standard demographics (Q-001 to Q-005)")
    print("✓ Industry-specific questions (Q-006 to Q-015)")
    print("✓ English content matching survey themes")
    print("✓ Same structure as original client_settings.xlsx")

if __name__ == "__main__":
    main()