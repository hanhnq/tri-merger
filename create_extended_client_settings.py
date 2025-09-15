import pandas as pd
import random

# Standard demographic questions (same for all clients)
STANDARD_QUESTIONS = [
    "Please tell us your age and gender",
    "What is your annual household income?",
    "What is your highest level of education?", 
    "What is your employment status?",
    "Which region do you live in?"
]

def create_automotive_extended_questions():
    """Create extended question list for automotive client"""
    questions = STANDARD_QUESTIONS.copy()
    
    # Theme-specific questions Q-006 to Q-015
    theme_questions = [
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
    questions.extend(theme_questions)
    
    # Extended questions Q-016 to Q-086 with automotive focus
    extended_questions = [
        "How satisfied are you with your current vehicle's performance?",
        "Rate the importance of fuel efficiency in your vehicle choice",
        "How likely are you to recommend your current car brand?", 
        "Evaluate the value for money of your vehicle purchase",
        "Rate the ease of finding parking in your area",
        "How important is vehicle safety technology to you?",
        "Assess the quality of your vehicle's interior features",
        "Rate your trust in automotive dealerships",
        "How important are advanced driver assistance features?",
        "What factors influence your car insurance decisions?",
        "Rate your satisfaction with vehicle maintenance costs",
        "How do you typically research new vehicle purchases?",
        "Evaluate the importance of vehicle resale value",
        "Rate your experience with vehicle financing options",
        "How satisfied are you with automotive customer service?",
        "Assess the effectiveness of car advertising and marketing",
        "Rate the accessibility of vehicle service centers",
        "How important is environmental impact in vehicle choice?",
        "Evaluate automotive brand social responsibility",
        "Rate the importance of vehicle customization options",
        "How satisfied are you with vehicle warranty coverage?",
        "Assess the quality of automotive mobile apps",
        "Rate the importance of vehicle connectivity features",
        "How do you prefer to receive vehicle maintenance reminders?",
        "Evaluate the effectiveness of roadside assistance services",
        "Rate your satisfaction with vehicle trade-in processes",
        "How important is vehicle appearance and styling?",
        "Assess the reliability of automotive review websites",
        "Rate the importance of local dealership reputation",
        "How satisfied are you with vehicle delivery experiences?",
        "Please share your thoughts on future automotive innovations",
        "What aspects of vehicle ownership frustrate you most?",
        "Describe your ideal car buying experience",
        "What improvements would you suggest for automotive services?",
        "Share your experience with vehicle recalls or safety issues",
        "What motivates your automotive brand loyalty?",
        "Describe how technology has changed your driving habits",
        "What concerns do you have about autonomous vehicles?",
        "Share your thoughts on the future of transportation",
        "What would convince you to switch to electric vehicles?",
        "Rate the importance of vehicle performance and speed",
        "How satisfied are you with automotive financing terms?",
        "Evaluate the quality of vehicle owner communities",
        "Rate the effectiveness of vehicle comparison tools",
        "How important is vehicle cargo space and utility?",
        "Assess your satisfaction with automotive parts availability",
        "Rate the importance of vehicle driving comfort",
        "How do you evaluate vehicle long-term reliability?",
        "Share your experience with vehicle subscription services",
        "What factors determine your vehicle replacement timing?",
        "Rate the importance of vehicle entertainment systems",
        "How satisfied are you with automotive mobile service?",
        "Evaluate the effectiveness of vehicle safety ratings",
        "Rate your confidence in automotive repair quality",
        "How important is vehicle fuel type variety?",
        "Assess the value of extended vehicle warranties",
        "Rate your satisfaction with automotive loyalty programs",
        "How do you prefer automotive companies communicate with you?",
        "Evaluate the importance of vehicle award recognition",
        "Rate your trust in automotive safety testing",
        "How satisfied are you with vehicle recall communications?",
        "Assess the effectiveness of automotive consumer advocacy",
        "Rate the importance of vehicle historical performance data",
        "How do you evaluate automotive environmental claims?",
        "Share your thoughts on automotive industry regulation",
        "What role does vehicle heritage play in your choices?",
        "Rate the importance of automotive innovation leadership",
        "How satisfied are you with automotive transparency?",
        "Evaluate the effectiveness of automotive customer feedback systems",
        "Rate your confidence in automotive quality control",
        "How important is automotive supply chain transparency?",
        "Share your perspective on automotive industry future trends"
    ]
    
    questions.extend(extended_questions)
    return questions

def create_fitness_extended_questions():
    """Create extended question list for fitness client"""
    questions = STANDARD_QUESTIONS.copy()
    
    # Theme-specific questions
    theme_questions = [
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
    questions.extend(theme_questions)
    
    # Extended fitness-related questions
    extended_questions = [
        "How satisfied are you with your current fitness level?",
        "Rate the importance of cardiovascular health in your routine",
        "How likely are you to recommend your current gym?",
        "Evaluate the value for money of your fitness expenses",
        "Rate the ease of accessing fitness facilities in your area",
        "How important is group fitness motivation to you?",
        "Assess the quality of fitness equipment you use",
        "Rate your trust in fitness professionals and trainers", 
        "How important are wearable fitness devices to your routine?",
        "What factors influence your fitness supplement choices?",
        "Rate your satisfaction with fitness class variety",
        "How do you typically find new workout routines?",
        "Evaluate the importance of fitness community support",
        "Rate your experience with fitness membership options",
        "How satisfied are you with fitness facility cleanliness?",
        "Assess the effectiveness of fitness marketing and promotions",
        "Rate the accessibility of fitness programs for your needs",
        "How important is environmental sustainability in fitness choices?",
        "Evaluate fitness brand social responsibility initiatives",
        "Rate the importance of personalized fitness programming",
        "How satisfied are you with fitness progress tracking?",
        "Assess the quality of fitness mobile applications",
        "Rate the importance of fitness data privacy and security",
        "How do you prefer to receive fitness motivation and tips?",
        "Evaluate the effectiveness of virtual fitness platforms",
        "Rate your satisfaction with fitness injury prevention programs",
        "How important is fitness fashion and apparel to you?",
        "Assess the reliability of fitness and health information sources",
        "Rate the importance of local fitness community involvement",
        "How satisfied are you with fitness goal achievement support?",
        "Please share your thoughts on future fitness innovations",
        "What aspects of fitness routines challenge you most?",
        "Describe your ideal fitness and wellness experience",
        "What improvements would you suggest for fitness facilities?",
        "Share your experience with fitness plateaus and setbacks",
        "What motivates your loyalty to fitness brands or facilities?",
        "Describe how technology has changed your fitness habits",
        "What concerns do you have about fitness data tracking?",
        "Share your thoughts on the future of home fitness",
        "What would encourage you to try new fitness activities?",
        "Rate the importance of fitness flexibility and mobility work",
        "How satisfied are you with fitness nutrition guidance?",
        "Evaluate the quality of fitness recovery and rest programs",
        "Rate the effectiveness of fitness progress measurement tools",
        "How important is fitness social interaction and community?",
        "Assess your satisfaction with fitness professional expertise",
        "Rate the importance of fitness routine variety and novelty",
        "How do you evaluate fitness program long-term sustainability?",
        "Share your experience with fitness challenges and competitions",
        "What factors determine your fitness routine consistency?",
        "Rate the importance of fitness mental health benefits",
        "How satisfied are you with fitness facility hours and access?",
        "Evaluate the effectiveness of fitness education and workshops",
        "Rate your confidence in fitness advice and guidance quality",
        "How important is fitness activity seasonal adaptation?",
        "Assess the value of fitness premium services and amenities",
        "Rate your satisfaction with fitness community inclusivity",
        "How do you prefer fitness companies communicate health updates?",
        "Evaluate the importance of fitness achievement recognition",
        "Rate your trust in fitness equipment safety and maintenance",
        "How satisfied are you with fitness emergency and safety protocols?",
        "Assess the effectiveness of fitness lifestyle integration support",
        "Rate the importance of fitness long-term health outcome data",
        "How do you evaluate fitness and wellness holistic approaches?",
        "Share your thoughts on fitness industry standards and certification",
        "What role does fitness tradition and culture play in your choices?",
        "Rate the importance of fitness innovation and research leadership",
        "How satisfied are you with fitness transparency and honesty?",
        "Evaluate the effectiveness of fitness feedback and improvement systems",
        "Rate your confidence in fitness industry quality and safety standards",
        "How important is fitness supply chain and product transparency?",
        "Share your perspective on fitness and wellness industry future directions"
    ]
    
    questions.extend(extended_questions)
    return questions

def create_entertainment_extended_questions():
    """Create extended question list for entertainment client"""
    questions = STANDARD_QUESTIONS.copy()
    
    # Theme-specific questions
    theme_questions = [
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
    questions.extend(theme_questions)
    
    # Extended entertainment-related questions
    extended_questions = [
        "How satisfied are you with current streaming content quality?",
        "Rate the importance of original content in streaming services",
        "How likely are you to recommend your favorite entertainment platform?",
        "Evaluate the value for money of your entertainment subscriptions",
        "Rate the ease of discovering new entertainment content",
        "How important is ad-free entertainment experience to you?",
        "Assess the quality of entertainment recommendation algorithms",
        "Rate your trust in entertainment platform content curation",
        "How important are offline entertainment options to you?",
        "What factors influence your entertainment subscription decisions?",
        "Rate your satisfaction with entertainment content variety",
        "How do you typically discover new entertainment content?",
        "Evaluate the importance of entertainment social features",
        "Rate your experience with entertainment platform user interfaces",
        "How satisfied are you with entertainment streaming quality?",
        "Assess the effectiveness of entertainment marketing and trailers",
        "Rate the accessibility of entertainment content for diverse audiences",
        "How important is entertainment content cultural representation?",
        "Evaluate entertainment platform social responsibility initiatives",
        "Rate the importance of entertainment content personalization",
        "How satisfied are you with entertainment release scheduling?",
        "Assess the quality of entertainment platform mobile apps",
        "Rate the importance of entertainment data privacy protection",
        "How do you prefer to receive entertainment recommendations?",
        "Evaluate the effectiveness of live entertainment streaming",
        "Rate your satisfaction with entertainment content archival",
        "How important is entertainment merchandise and collectibles?",
        "Assess the reliability of entertainment reviews and ratings",
        "Rate the importance of local entertainment content availability",
        "How satisfied are you with entertainment customer support?",
        "Please share your thoughts on future entertainment innovations",
        "What aspects of modern entertainment frustrate you most?",
        "Describe your ideal entertainment consumption experience",
        "What improvements would you suggest for streaming platforms?",
        "Share your experience with entertainment content censorship",
        "What motivates your loyalty to entertainment brands?",
        "Describe how technology has changed your entertainment habits",
        "What concerns do you have about entertainment data collection?",
        "Share your thoughts on the future of interactive entertainment",
        "What would encourage you to try new entertainment formats?",
        "Rate the importance of entertainment educational content",
        "How satisfied are you with entertainment pricing models?",
        "Evaluate the quality of entertainment community features",
        "Rate the effectiveness of entertainment parental controls",
        "How important is entertainment cross-platform compatibility?",
        "Assess your satisfaction with entertainment content moderation",
        "Rate the importance of entertainment behind-the-scenes content",
        "How do you evaluate entertainment platform long-term value?",
        "Share your experience with entertainment live events",
        "What factors determine your entertainment viewing schedule?",
        "Rate the importance of entertainment subtitle and language options",
        "How satisfied are you with entertainment search and discovery?",
        "Evaluate the effectiveness of entertainment loyalty programs",
        "Rate your confidence in entertainment content authenticity",
        "How important is entertainment creator compensation transparency?",
        "Assess the value of entertainment premium features",
        "Rate your satisfaction with entertainment platform stability",
        "How do you prefer entertainment companies handle controversial content?",
        "Evaluate the importance of entertainment industry awards",
        "Rate your trust in entertainment content age ratings",
        "How satisfied are you with entertainment platform updates?",
        "Assess the effectiveness of entertainment audience feedback systems",
        "Rate the importance of entertainment production transparency",
        "How do you evaluate entertainment environmental impact?",
        "Share your thoughts on entertainment industry regulation",
        "What role does nostalgia play in your entertainment choices?",
        "Rate the importance of entertainment innovation and technology",
        "How satisfied are you with entertainment industry transparency?",
        "Evaluate the effectiveness of entertainment creator support systems",
        "Rate your confidence in entertainment industry quality standards",
        "How important is entertainment supply chain ethical practices?",
        "Share your perspective on entertainment industry future evolution"
    ]
    
    questions.extend(extended_questions)
    return questions

def create_education_extended_questions():
    """Create extended question list for education client"""
    questions = STANDARD_QUESTIONS.copy()
    
    # Theme-specific questions
    theme_questions = [
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
    questions.extend(theme_questions)
    
    # Extended education-related questions
    extended_questions = [
        "How satisfied are you with current online learning platforms?",
        "Rate the importance of interactive learning content",
        "How likely are you to recommend your preferred learning platform?",
        "Evaluate the value for money of educational courses",
        "Rate the ease of finding relevant learning materials",
        "How important is peer interaction in online learning?",
        "Assess the quality of educational content presentation",
        "Rate your trust in educational platform credibility",
        "How important are practical exercises in learning?",
        "What factors influence your course selection decisions?",
        "Rate your satisfaction with learning progress tracking",
        "How do you typically evaluate course quality before enrollment?",
        "Evaluate the importance of instructor expertise and credentials",
        "Rate your experience with educational platform user interfaces",
        "How satisfied are you with learning material accessibility?",
        "Assess the effectiveness of educational marketing and course descriptions",
        "Rate the accessibility of education for diverse learning styles",
        "How important is cultural diversity in educational content?",
        "Evaluate educational platform social responsibility initiatives",
        "Rate the importance of personalized learning paths",
        "How satisfied are you with course completion certificates?",
        "Assess the quality of educational mobile learning apps",
        "Rate the importance of learning data privacy protection",
        "How do you prefer to receive learning recommendations?",
        "Evaluate the effectiveness of live educational sessions",
        "Rate your satisfaction with educational content updates",
        "How important is educational community and networking?",
        "Assess the reliability of educational reviews and ratings",
        "Rate the importance of local educational opportunities",
        "How satisfied are you with educational customer support?",
        "Please share your thoughts on future educational innovations",
        "What aspects of online learning frustrate you most?",
        "Describe your ideal learning experience",
        "What improvements would you suggest for educational platforms?",
        "Share your experience with educational content accessibility",
        "What motivates your loyalty to educational brands?",
        "Describe how technology has changed your learning habits",
        "What concerns do you have about educational data privacy?",
        "Share your thoughts on the future of skill-based learning",
        "What would encourage you to pursue advanced certifications?",
        "Rate the importance of educational content practical application",
        "How satisfied are you with educational pricing models?",
        "Evaluate the quality of educational peer learning features",
        "Rate the effectiveness of educational assessment methods",
        "How important is educational content multimedia integration?",
        "Assess your satisfaction with educational progress feedback",
        "Rate the importance of educational content regular updates",
        "How do you evaluate educational program long-term career value?",
        "Share your experience with educational mentorship programs",
        "What factors determine your learning schedule consistency?",
        "Rate the importance of educational content global perspectives",
        "How satisfied are you with educational technical support?",
        "Evaluate the effectiveness of educational gamification features",
        "Rate your confidence in educational content accuracy",
        "How important is educational instructor availability and responsiveness?",
        "Assess the value of educational premium features and services",
        "Rate your satisfaction with educational community moderation",
        "How do you prefer educational companies communicate course updates?",
        "Evaluate the importance of educational industry partnerships",
        "Rate your trust in educational credential recognition",
        "How satisfied are you with educational platform performance?",
        "Assess the effectiveness of educational feedback collection systems",
        "Rate the importance of educational content version control",
        "How do you evaluate educational environmental and social impact?",
        "Share your thoughts on educational industry accreditation standards",
        "What role does educational tradition play in your course choices?",
        "Rate the importance of educational innovation and research",
        "How satisfied are you with educational transparency practices?",
        "Evaluate the effectiveness of educational learner support systems",
        "Rate your confidence in educational quality assurance processes",
        "How important is educational content creator ethical practices?",
        "Share your perspective on educational industry future transformation"
    ]
    
    questions.extend(extended_questions)
    return questions

def create_environment_extended_questions():
    """Create extended question list for environment client"""
    questions = STANDARD_QUESTIONS.copy()
    
    # Theme-specific questions
    theme_questions = [
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
    questions.extend(theme_questions)
    
    # Extended environment-related questions
    extended_questions = [
        "How satisfied are you with current environmental protection efforts?",
        "Rate the importance of renewable energy in environmental solutions",
        "How likely are you to recommend eco-friendly products to others?",
        "Evaluate the value for money of sustainable product options",
        "Rate the ease of accessing environmental information and resources",
        "How important is community involvement in environmental action?",
        "Assess the quality of environmental education and awareness programs",
        "Rate your trust in environmental organizations and initiatives",
        "How important are government environmental policies to you?",
        "What factors influence your eco-friendly purchasing decisions?",
        "Rate your satisfaction with environmental product labeling",
        "How do you typically verify environmental claims and certifications?",
        "Evaluate the importance of corporate environmental responsibility",
        "Rate your experience with environmental community programs",
        "How satisfied are you with environmental waste management systems?",
        "Assess the effectiveness of environmental awareness campaigns",
        "Rate the accessibility of sustainable lifestyle options",
        "How important is environmental justice and equity?",
        "Evaluate environmental organization transparency and accountability",
        "Rate the importance of environmental impact measurement",
        "How satisfied are you with environmental protection progress?",
        "Assess the quality of environmental monitoring and reporting",
        "Rate the importance of environmental data transparency",
        "How do you prefer to receive environmental updates and information?",
        "Evaluate the effectiveness of environmental policy implementation",
        "Rate your satisfaction with environmental conservation efforts",
        "How important is environmental innovation and technology?",
        "Assess the reliability of environmental research and studies",
        "Rate the importance of local environmental protection initiatives",
        "How satisfied are you with environmental emergency response?",
        "Please share your thoughts on future environmental solutions",
        "What aspects of environmental protection frustrate you most?",
        "Describe your ideal sustainable community",
        "What improvements would you suggest for environmental programs?",
        "Share your experience with environmental lifestyle changes",
        "What motivates your commitment to environmental causes?",
        "Describe how environmental awareness has changed your behavior",
        "What concerns do you have about environmental data and privacy?",
        "Share your thoughts on the future of environmental technology",
        "What would encourage you to increase environmental activism?",
        "Rate the importance of environmental education in schools",
        "How satisfied are you with environmental product pricing?",
        "Evaluate the quality of environmental community engagement",
        "Rate the effectiveness of environmental incentive programs",
        "How important is environmental impact of digital technology?",
        "Assess your satisfaction with environmental regulation enforcement",
        "Rate the importance of environmental restoration projects",
        "How do you evaluate environmental solution long-term effectiveness?",
        "Share your experience with environmental volunteer activities",
        "What factors determine your environmental action consistency?",
        "Rate the importance of environmental global cooperation",
        "How satisfied are you with environmental scientific communication?",
        "Evaluate the effectiveness of environmental behavior change programs",
        "Rate your confidence in environmental measurement accuracy",
        "How important is environmental solution scalability and adoption?",
        "Assess the value of environmental premium services and products",
        "Rate your satisfaction with environmental progress transparency",
        "How do you prefer environmental organizations communicate updates?",
        "Evaluate the importance of environmental industry collaboration",
        "Rate your trust in environmental impact assessments",
        "How satisfied are you with environmental crisis response?",
        "Assess the effectiveness of environmental public participation systems",
        "Rate the importance of environmental long-term planning",
        "How do you evaluate environmental solution cost-effectiveness?",
        "Share your thoughts on environmental regulation adequacy",
        "What role does environmental heritage play in your values?",
        "Rate the importance of environmental leadership and innovation",
        "How satisfied are you with environmental sector transparency?",
        "Evaluate the effectiveness of environmental stakeholder engagement",
        "Rate your confidence in environmental protection quality standards",
        "How important is environmental solution ethical implementation?",
        "Share your perspective on environmental sector future development"
    ]
    
    questions.extend(extended_questions)
    return questions

def create_client_settings_file(client_type, client_name, output_filename):
    """Create extended client settings file"""
    
    if client_type == "automotive":
        questions = create_automotive_extended_questions()
    elif client_type == "fitness":
        questions = create_fitness_extended_questions()
    elif client_type == "entertainment":
        questions = create_entertainment_extended_questions()
    elif client_type == "education":
        questions = create_education_extended_questions()
    else:  # environment
        questions = create_environment_extended_questions()
    
    # Create DataFrame
    data = {
        'Client Name': [client_name] * len(questions),
        'Target Questions for Analysis': questions
    }
    df = pd.DataFrame(data)
    
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
            
            adjusted_width = min(max_length + 2, 80)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    num_questions = len(questions)
    print(f"✅ Created {output_filename} for '{client_name}' with {num_questions} questions")
    
    return output_filename

def main():
    """Create 5 extended client settings files"""
    
    print("Creating 5 Extended Client Settings files (80+ questions each)...")
    print("="*70)
    
    clients = [
        ("automotive", "AutoMotion Inc", "AutoMotion_Extended_Client_Settings.xlsx"),
        ("fitness", "FitLife Wellness", "FitLife_Extended_Client_Settings.xlsx"),
        ("entertainment", "StreamVibe Media", "StreamVibe_Extended_Client_Settings.xlsx"),
        ("education", "LearnForward Academy", "LearnForward_Extended_Client_Settings.xlsx"),
        ("environment", "EcoGreen Solutions", "EcoGreen_Extended_Client_Settings.xlsx")
    ]
    
    created_files = []
    
    for client_type, client_name, filename in clients:
        file_path = create_client_settings_file(client_type, client_name, filename)
        created_files.append(file_path)
        print()
    
    print("="*70)
    print("✅ All 5 extended client settings files created successfully!")
    print("\nFiles created:")
    for i, file_path in enumerate(created_files, 1):
        print(f"{i}. {file_path}")
    
    print("\n🎯 Extended Client Settings Summary:")
    print("Each file now contains 80+ questions covering:")
    print("✓ Standard demographics (Q-001 to Q-005)")
    print("✓ Industry-specific themes (Q-006 to Q-015)")
    print("✓ Extended domain questions (Q-016 to Q-086)")
    print("✓ Mix of rating scales, multiple choice, and free response")
    print("✓ Comprehensive coverage matching survey complexity")
    
    print("\n📊 Question Distribution:")
    print("• Demographics: 5 questions (consistent across all)")
    print("• Theme-specific: 10 questions (unique per industry)")
    print("• Extended coverage: 65+ questions (industry-focused)")
    print("• Total per file: 80+ questions")

if __name__ == "__main__":
    main()