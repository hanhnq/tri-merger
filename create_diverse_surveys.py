import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Standard demographic questions (same for all surveys)
STANDARD_DEMOGRAPHICS = {
    'Q-001': {
        'question': 'Please tell us your age and gender',
        'type': 'S/A',
        'requirement': 'Required',
        'options': [
            '1. Male 18-24', '2. Male 25-34', '3. Male 35-44', '4. Male 45-54',
            '5. Male 55-64', '6. Male 65+', '7. Female 18-24', '8. Female 25-34',
            '9. Female 35-44', '10. Female 45-54', '11. Female 55-64', '12. Female 65+'
        ]
    },
    'Q-002': {
        'question': 'What is your annual household income?',
        'type': 'S/A',
        'requirement': 'Optional',
        'options': [
            '1. Less than $25,000', '2. $25,000 - $40,000', '3. $40,000 - $60,000',
            '4. $60,000 - $80,000', '5. $80,000 - $100,000', '6. $100,000 - $150,000',
            '7. More than $150,000', '8. Prefer not to answer'
        ]
    },
    'Q-003': {
        'question': 'What is your highest level of education?',
        'type': 'S/A',
        'requirement': 'Required',
        'options': [
            '1. High school or less', '2. Some college/Associate degree', '3. Bachelor degree',
            '4. Master degree', '5. Doctorate/PhD', '6. Professional degree', '7. Other'
        ]
    },
    'Q-004': {
        'question': 'What is your employment status?',
        'type': 'S/A',
        'requirement': 'Required',
        'options': [
            '1. Full-time employed', '2. Part-time employed', '3. Self-employed',
            '4. Student', '5. Homemaker', '6. Retired', '7. Unemployed', '8. Other'
        ]
    },
    'Q-005': {
        'question': 'Which region do you live in?',
        'type': 'S/A',
        'requirement': 'Required',
        'options': [
            '1. North America', '2. South America', '3. Europe',
            '4. Asia Pacific', '5. Middle East', '6. Africa', '7. Other'
        ]
    }
}

def create_automotive_questions():
    """Create questions for automotive/car survey"""
    questions = []
    
    # Q-006: Car ownership
    questions.append(('Q-006', 'Required', 'How many vehicles does your household currently own?', 'S/A', [
        '1. None (I don\'t own a car)', '2. One vehicle', '3. Two vehicles',
        '4. Three vehicles', '5. Four or more vehicles'
    ]))
    
    # Q-007: Primary vehicle type
    questions.append(('Q-007', 'Required', 'What type is your primary vehicle?', 'S/A+FA', [
        '1. Sedan', '2. SUV', '3. Truck/Pickup', '4. Hatchback', '5. Coupe',
        '6. Convertible', '7. Minivan', '8. Motorcycle', '9. Electric vehicle',
        '10. Hybrid vehicle', '11. Other (Please specify)'
    ]))
    
    # Q-008: Brand preference
    questions.append(('Q-008', 'Optional', 'Which car brands do you prefer?', 'M/A', [
        '1. Toyota', '2. Honda', '3. Ford', '4. Chevrolet', '5. BMW',
        '6. Mercedes-Benz', '7. Audi', '8. Nissan', '9. Hyundai', '10. Kia',
        '11. Tesla', '12. Volkswagen', '13. Mazda', '14. Subaru'
    ]))
    
    # Q-009: Driving frequency
    questions.append(('Q-009', 'Required', 'How often do you drive?', 'S/A', [
        '1. Daily', '2. Several times a week', '3. Once a week',
        '4. A few times a month', '5. Rarely', '6. Never (I don\'t drive)'
    ]))
    
    # Q-010: Car buying factors
    questions.append(('Q-010', 'Required', 'What factors are most important when buying a car?', 'M/A+FA', [
        '1. Price/Affordability', '2. Fuel efficiency', '3. Safety ratings',
        '4. Reliability/Durability', '5. Brand reputation', '6. Resale value',
        '7. Performance/Power', '8. Technology features', '9. Comfort/Interior space',
        '10. Environmental impact', '11. Design/Appearance', '12. Warranty coverage',
        '13. Maintenance costs', '14. Other (Please specify)'
    ]))
    
    # Q-011: Service preferences
    questions.append(('Q-011', 'Optional', 'Where do you prefer to service your vehicle?', 'S/A', [
        '1. Dealership service center', '2. Independent mechanic', '3. Chain service center (Jiffy Lube, etc.)',
        '4. Do it myself', '5. Mobile service (comes to me)', '6. Don\'t service regularly'
    ]))
    
    # Q-012: Future purchase plans
    questions.append(('Q-012', 'Optional', 'When do you plan to buy your next vehicle?', 'S/A', [
        '1. Within 6 months', '2. 6 months to 1 year', '3. 1-2 years',
        '4. 2-5 years', '5. More than 5 years', '6. No plans to buy'
    ]))
    
    # Q-013: Electric vehicle interest
    questions.append(('Q-013', 'Optional', 'How interested are you in electric vehicles?', 'S/A', [
        '1. Very interested', '2. Somewhat interested', '3. Neutral',
        '4. Not very interested', '5. Not at all interested'
    ]))
    
    # Q-014: Biggest car concerns
    questions.append(('Q-014', 'Optional', 'What are your biggest concerns about car ownership?', 'M/A', [
        '1. High purchase cost', '2. Insurance costs', '3. Maintenance/repair costs',
        '4. Fuel costs', '5. Parking difficulties', '6. Traffic/commute stress',
        '7. Environmental impact', '8. Safety concerns', '9. Depreciation',
        '10. Registration/licensing fees'
    ]))
    
    # Q-015: Free response
    questions.append(('Q-015', 'Optional', 'What would make your driving experience better?', 'FA', [
        '(Please share your thoughts)'
    ]))
    
    return questions

def create_fitness_questions():
    """Create questions for fitness/health survey"""
    questions = []
    
    # Q-006: Exercise frequency
    questions.append(('Q-006', 'Required', 'How often do you exercise or engage in physical activity?', 'S/A', [
        '1. Daily', '2. 5-6 times per week', '3. 3-4 times per week',
        '4. 1-2 times per week', '5. A few times per month', '6. Rarely', '7. Never'
    ]))
    
    # Q-007: Preferred activities
    questions.append(('Q-007', 'Required', 'What types of physical activities do you enjoy?', 'M/A+FA', [
        '1. Walking/Hiking', '2. Running/Jogging', '3. Swimming', '4. Cycling',
        '5. Weight training', '6. Yoga', '7. Pilates', '8. Dancing', '9. Team sports',
        '10. Martial arts', '11. Rock climbing', '12. Tennis/Racquet sports',
        '13. Group fitness classes', '14. Other (Please specify)'
    ]))
    
    # Q-008: Workout location
    questions.append(('Q-008', 'Optional', 'Where do you primarily work out?', 'S/A', [
        '1. At home', '2. Commercial gym/fitness center', '3. Outdoor spaces (parks, trails)',
        '4. Community center', '5. Workplace gym', '6. Private studio (yoga, pilates, etc.)',
        '7. Sports club', '8. I don\'t work out regularly'
    ]))
    
    # Q-009: Fitness goals
    questions.append(('Q-009', 'Optional', 'What are your primary fitness goals?', 'M/A', [
        '1. Weight loss', '2. Weight gain/muscle building', '3. General health maintenance',
        '4. Stress relief', '5. Improved cardiovascular health', '6. Increased strength',
        '7. Better flexibility', '8. Sport-specific training', '9. Injury prevention',
        '10. Social interaction', '11. Better sleep', '12. Mental health benefits'
    ]))
    
    # Q-010: Barriers to exercise
    questions.append(('Q-010', 'Optional', 'What prevents you from exercising more?', 'M/A+FA', [
        '1. Lack of time', '2. Lack of motivation', '3. Cost of gym/equipment',
        '4. Physical limitations/injuries', '5. Lack of knowledge', '6. Weather conditions',
        '7. Childcare responsibilities', '8. Work schedule', '9. Lack of energy',
        '10. No convenient facilities', '11. Self-consciousness', '12. Other (Please specify)'
    ]))
    
    # Q-011: Health tracking
    questions.append(('Q-011', 'Optional', 'Do you track your fitness or health metrics?', 'M/A', [
        '1. Steps/daily activity', '2. Heart rate', '3. Weight', '4. Body fat percentage',
        '5. Sleep quality', '6. Calories burned', '7. Workout duration', '8. Strength progress',
        '9. Flexibility improvements', '10. Mood/mental state', '11. I don\'t track anything'
    ]))
    
    # Q-012: Technology use
    questions.append(('Q-012', 'Optional', 'What fitness technology do you use?', 'M/A', [
        '1. Smartphone fitness apps', '2. Fitness tracker (Fitbit, etc.)', '3. Smartwatch',
        '4. Heart rate monitor', '5. Smart scale', '6. Online workout videos',
        '7. Virtual fitness classes', '8. Fitness gaming (Wii Fit, etc.)',
        '9. None of the above'
    ]))
    
    # Q-013: Nutrition focus
    questions.append(('Q-013', 'Optional', 'How important is nutrition in your fitness routine?', 'S/A', [
        '1. Extremely important - I carefully plan all meals', '2. Very important - I pay attention to what I eat',
        '3. Somewhat important - I try to eat healthy', '4. Not very important - I eat what I want',
        '5. Not important at all'
    ]))
    
    # Q-014: Professional guidance
    questions.append(('Q-014', 'Optional', 'Have you ever worked with fitness professionals?', 'M/A', [
        '1. Personal trainer', '2. Nutritionist/Dietitian', '3. Physical therapist',
        '4. Group fitness instructor', '5. Sports coach', '6. Yoga/Pilates instructor',
        '7. Online fitness coach', '8. None of the above'
    ]))
    
    # Q-015: Free response
    questions.append(('Q-015', 'Optional', 'What motivates you most to stay active and healthy?', 'FA', [
        '(Please share what keeps you motivated)'
    ]))
    
    return questions

def create_entertainment_questions():
    """Create questions for entertainment/media survey"""
    questions = []
    
    # Q-006: Entertainment time
    questions.append(('Q-006', 'Required', 'How many hours per day do you spend on entertainment?', 'S/A', [
        '1. Less than 1 hour', '2. 1-2 hours', '3. 2-4 hours',
        '4. 4-6 hours', '5. 6-8 hours', '6. More than 8 hours'
    ]))
    
    # Q-007: Preferred activities
    questions.append(('Q-007', 'Required', 'What are your favorite entertainment activities?', 'M/A+FA', [
        '1. Watching TV shows/series', '2. Watching movies', '3. Listening to music',
        '4. Playing video games', '5. Reading books/magazines', '6. Social media browsing',
        '7. Podcasts', '8. YouTube videos', '9. Live events (concerts, theater)',
        '10. Sports (watching)', '11. Board games/puzzles', '12. Arts and crafts',
        '13. Cooking/baking for fun', '14. Other (Please specify)'
    ]))
    
    # Q-008: Streaming services
    questions.append(('Q-008', 'Optional', 'Which streaming services do you subscribe to?', 'M/A', [
        '1. Netflix', '2. Amazon Prime Video', '3. Disney+', '4. Hulu',
        '5. HBO Max', '6. Apple TV+', '7. Paramount+', '8. Peacock',
        '9. YouTube Premium', '10. Spotify', '11. Apple Music', '12. None'
    ]))
    
    # Q-009: Gaming preferences
    questions.append(('Q-009', 'Optional', 'What types of games do you enjoy?', 'M/A', [
        '1. Action/Adventure games', '2. Role-playing games (RPGs)', '3. Strategy games',
        '4. Puzzle games', '5. Sports games', '6. Racing games', '7. Shooter games',
        '8. Simulation games', '9. Mobile games', '10. Board games', '11. I don\'t play games'
    ]))
    
    # Q-010: Music genres
    questions.append(('Q-010', 'Optional', 'What music genres do you listen to most?', 'M/A+FA', [
        '1. Pop', '2. Rock', '3. Hip-hop/Rap', '4. Country', '5. Jazz',
        '6. Classical', '7. Electronic/EDM', '8. R&B/Soul', '9. Folk/Acoustic',
        '10. Reggae', '11. Blues', '12. Heavy Metal', '13. World Music',
        '14. Other (Please specify)'
    ]))
    
    # Q-011: News consumption
    questions.append(('Q-011', 'Optional', 'How do you prefer to consume news and information?', 'M/A', [
        '1. Television news', '2. Online news websites', '3. Newspapers (print)',
        '4. Social media', '5. News podcasts', '6. Radio news', '7. News apps',
        '8. Email newsletters', '9. I don\'t follow news regularly'
    ]))
    
    # Q-012: Social media platforms
    questions.append(('Q-012', 'Optional', 'Which social media platforms do you use regularly?', 'M/A', [
        '1. Facebook', '2. Instagram', '3. Twitter/X', '4. TikTok', '5. LinkedIn',
        '6. YouTube', '7. Snapchat', '8. Pinterest', '9. Reddit', '10. Discord',
        '11. Twitch', '12. I don\'t use social media'
    ]))
    
    # Q-013: Content creation
    questions.append(('Q-013', 'Optional', 'Do you create any content online?', 'M/A', [
        '1. Social media posts', '2. Blog writing', '3. Video content', '4. Photography',
        '5. Music/Audio content', '6. Live streaming', '7. Podcasting', '8. Art/Design',
        '9. Writing reviews', '10. I don\'t create content'
    ]))
    
    # Q-014: Entertainment spending
    questions.append(('Q-014', 'Optional', 'How much do you spend monthly on entertainment?', 'S/A', [
        '1. Less than $25', '2. $25-50', '3. $50-100', '4. $100-200',
        '5. $200-300', '6. More than $300'
    ]))
    
    # Q-015: Free response
    questions.append(('Q-015', 'Optional', 'What new entertainment trends interest you most?', 'FA', [
        '(Tell us about entertainment trends that catch your attention)'
    ]))
    
    return questions

def create_education_questions():
    """Create questions for education/learning survey"""
    questions = []
    
    # Q-006: Learning motivation
    questions.append(('Q-006', 'Required', 'What motivates you to learn new things?', 'M/A+FA', [
        '1. Career advancement', '2. Personal interest/curiosity', '3. Hobby development',
        '4. Staying current with technology', '5. Meeting job requirements', '6. Creative expression',
        '7. Social interaction', '8. Building confidence', '9. Solving everyday problems',
        '10. Intellectual challenge', '11. Other (Please specify)'
    ]))
    
    # Q-007: Learning methods
    questions.append(('Q-007', 'Required', 'How do you prefer to learn new skills?', 'M/A', [
        '1. Online courses (Coursera, Udemy, etc.)', '2. YouTube tutorials', '3. Books/eBooks',
        '4. In-person classes', '5. Workshops/Seminars', '6. One-on-one tutoring',
        '7. Practice/Trial and error', '8. Podcasts', '9. Mobile learning apps',
        '10. Peer learning/Study groups', '11. Professional conferences'
    ]))
    
    # Q-008: Subject interests
    questions.append(('Q-008', 'Optional', 'What subjects are you most interested in learning?', 'M/A+FA', [
        '1. Technology/Programming', '2. Languages', '3. Business/Finance', '4. Arts/Design',
        '5. Science/Engineering', '6. Health/Medicine', '7. History/Culture', '8. Psychology',
        '9. Cooking/Culinary arts', '10. Music/Instruments', '11. Sports/Fitness',
        '12. Photography/Videography', '13. Writing/Literature', '14. Other (Please specify)'
    ]))
    
    # Q-009: Learning time
    questions.append(('Q-009', 'Optional', 'How much time do you dedicate to learning weekly?', 'S/A', [
        '1. Less than 1 hour', '2. 1-3 hours', '3. 3-5 hours',
        '4. 5-10 hours', '5. 10-15 hours', '6. More than 15 hours'
    ]))
    
    # Q-010: Learning barriers
    questions.append(('Q-010', 'Optional', 'What prevents you from learning more?', 'M/A', [
        '1. Lack of time', '2. Cost of courses/materials', '3. Lack of motivation',
        '4. Difficulty finding quality resources', '5. Work/family responsibilities',
        '6. Learning style mismatch', '7. Technology barriers', '8. Language barriers',
        '9. Lack of support/guidance', '10. Fear of failure', '11. Information overload'
    ]))
    
    # Q-011: Certification value
    questions.append(('Q-011', 'Optional', 'How important are certificates/credentials to you?', 'S/A', [
        '1. Very important - I only take courses that offer certificates',
        '2. Important - I prefer courses with certificates', '3. Somewhat important',
        '4. Not very important', '5. Not important at all - I learn for knowledge only'
    ]))
    
    # Q-012: Learning environment
    questions.append(('Q-012', 'Optional', 'Where do you learn most effectively?', 'S/A', [
        '1. At home in quiet space', '2. At home with background noise', '3. Library/Study hall',
        '4. Coffee shops/Cafes', '5. Classroom/Formal setting', '6. Outdoors',
        '7. While commuting', '8. During breaks at work'
    ]))
    
    # Q-013: Learning technology
    questions.append(('Q-013', 'Optional', 'What devices do you use for learning?', 'M/A', [
        '1. Laptop/Desktop computer', '2. Smartphone', '3. Tablet', '4. E-reader',
        '5. Traditional books/printed materials', '6. Audio devices (headphones, speakers)',
        '7. Smart TV', '8. VR headset'
    ]))
    
    # Q-014: Skill application
    questions.append(('Q-014', 'Optional', 'How do you apply newly learned skills?', 'M/A', [
        '1. At my current job', '2. Personal projects', '3. Freelance work',
        '4. Volunteer activities', '5. Teaching others', '6. Side business/startup',
        '7. Creative hobbies', '8. Daily life improvements', '9. I struggle to apply them'
    ]))
    
    # Q-015: Free response
    questions.append(('Q-015', 'Optional', 'What would make online learning more effective for you?', 'FA', [
        '(Share your ideas for improving online learning experiences)'
    ]))
    
    return questions

def create_environment_questions():
    """Create questions for environmental awareness survey"""
    questions = []
    
    # Q-006: Environmental concern
    questions.append(('Q-006', 'Required', 'How concerned are you about environmental issues?', 'S/A', [
        '1. Extremely concerned', '2. Very concerned', '3. Moderately concerned',
        '4. Slightly concerned', '5. Not concerned at all'
    ]))
    
    # Q-007: Environmental actions
    questions.append(('Q-007', 'Required', 'What environmentally-friendly actions do you take?', 'M/A+FA', [
        '1. Recycling', '2. Reducing energy consumption', '3. Using public transportation',
        '4. Buying eco-friendly products', '5. Composting', '6. Water conservation',
        '7. Reducing meat consumption', '8. Using renewable energy', '9. Minimizing waste',
        '10. Supporting green businesses', '11. Participating in environmental activism',
        '12. Planting trees/gardening', '13. Other (Please specify)'
    ]))
    
    # Q-008: Biggest environmental concerns
    questions.append(('Q-008', 'Optional', 'What environmental issues concern you most?', 'M/A', [
        '1. Climate change/Global warming', '2. Air pollution', '3. Water pollution',
        '4. Deforestation', '5. Ocean pollution/Plastic waste', '6. Loss of biodiversity',
        '7. Soil degradation', '8. Ozone depletion', '9. Nuclear waste',
        '10. Overpopulation', '11. Resource depletion'
    ]))
    
    # Q-009: Green products
    questions.append(('Q-009', 'Optional', 'When shopping, how important are eco-friendly options?', 'S/A', [
        '1. Always choose eco-friendly when available', '2. Usually choose eco-friendly',
        '3. Sometimes consider eco-friendly options', '4. Rarely consider environmental impact',
        '5. Never consider environmental impact'
    ]))
    
    # Q-010: Transportation choices
    questions.append(('Q-010', 'Optional', 'What transportation methods do you use regularly?', 'M/A', [
        '1. Personal car (gasoline)', '2. Personal car (hybrid)', '3. Personal car (electric)',
        '4. Public bus', '5. Train/Subway', '6. Bicycle', '7. Walking',
        '8. Rideshare (Uber/Lyft)', '9. Motorcycle/Scooter', '10. Work from home'
    ]))
    
    # Q-011: Energy usage
    questions.append(('Q-011', 'Optional', 'What steps do you take to reduce energy consumption?', 'M/A', [
        '1. LED light bulbs', '2. Programmable thermostat', '3. Energy-efficient appliances',
        '4. Unplugging devices when not in use', '5. Solar panels', '6. Insulation improvements',
        '7. Line drying clothes', '8. Shorter showers', '9. None of the above'
    ]))
    
    # Q-012: Information sources
    questions.append(('Q-012', 'Optional', 'Where do you get environmental news and information?', 'M/A', [
        '1. Traditional news media', '2. Environmental organizations\' websites', '3. Social media',
        '4. Scientific journals/publications', '5. Government websites', '6. Documentary films',
        '7. Podcasts', '8. Books/magazines', '9. School/University courses',
        '10. I don\'t actively seek environmental information'
    ]))
    
    # Q-013: Barriers to green living
    questions.append(('Q-013', 'Optional', 'What prevents you from being more environmentally conscious?', 'M/A+FA', [
        '1. Higher costs of green products', '2. Lack of convenient options', '3. Time constraints',
        '4. Lack of information', '5. Skepticism about effectiveness', '6. Lifestyle limitations',
        '7. Social/cultural barriers', '8. Government/policy limitations', '9. Technology limitations',
        '10. Nothing prevents me', '11. Other (Please specify)'
    ]))
    
    # Q-014: Future changes
    questions.append(('Q-014', 'Optional', 'What environmental changes do you plan to make this year?', 'M/A', [
        '1. Reduce single-use plastics', '2. Eat more plant-based meals', '3. Use alternative transportation',
        '4. Install renewable energy', '5. Start composting', '6. Buy from sustainable brands',
        '7. Reduce overall consumption', '8. Get involved in environmental advocacy',
        '9. Learn more about environmental issues', '10. No specific changes planned'
    ]))
    
    # Q-015: Free response
    questions.append(('Q-015', 'Optional', 'What would motivate you to take more environmental action?', 'FA', [
        '(Tell us what would encourage more environmentally-friendly behavior)'
    ]))
    
    return questions

def create_question_master_sheet(survey_type="automotive"):
    """Create question master sheet with standard demographics + diverse theme questions"""
    
    questions_data = []
    
    # Add standard demographic questions Q-001 to Q-005 (same for all surveys)
    for q_id, q_info in STANDARD_DEMOGRAPHICS.items():
        questions_data.append([q_id, q_info['requirement'], q_info['question'], q_info['type']])
        for option in q_info['options']:
            questions_data.append(['', '', option, ''])
        questions_data.append(['', '', '', ''])
    
    # Add theme-specific questions Q-006 to Q-015
    if survey_type == "automotive":
        theme_questions = create_automotive_questions()
    elif survey_type == "fitness":
        theme_questions = create_fitness_questions()
    elif survey_type == "entertainment":
        theme_questions = create_entertainment_questions()
    elif survey_type == "education":
        theme_questions = create_education_questions()
    else:  # environment
        theme_questions = create_environment_questions()
    
    # Add theme-specific questions to the data
    for q_id, requirement, question, q_type, options in theme_questions:
        questions_data.append([q_id, requirement, question, q_type])
        for option in options:
            questions_data.append(['', '', option, ''])
        questions_data.append(['', '', '', ''])
    
    # Add remaining questions Q-016 to Q-086 with varied content
    question_topics = [
        'satisfaction with customer service', 'likelihood to recommend', 'value for money assessment',
        'ease of use rating', 'quality perception', 'brand trust level', 'feature importance',
        'purchase decision factors', 'future usage intentions', 'improvement suggestions',
        'competitor comparison', 'price sensitivity', 'loyalty measurement', 'experience rating',
        'problem resolution', 'communication effectiveness', 'accessibility concerns', 
        'innovation expectations', 'social responsibility', 'sustainability importance'
    ]
    
    for q in range(16, 87):
        q_num = f'Q-{str(q).zfill(3)}'
        topic = question_topics[(q-16) % len(question_topics)]
        
        if q % 9 == 0:  # Free answer questions
            questions_data.extend([
                [q_num, 'Optional', f'Please share your detailed thoughts on {topic}', 'FA'],
                ['', '', '(Please provide your detailed response)', ''],
                ['', '', '', '']
            ])
        elif q % 6 == 0:  # Multi-answer with FA
            questions_data.append([q_num, 'Optional', f'Which aspects of {topic} are relevant to you?', 'M/A+FA'])
            aspects = ['Quality', 'Speed', 'Cost', 'Convenience', 'Reliability', 'Innovation', 'Support', 'Accessibility']
            for i, aspect in enumerate(aspects[:random.randint(6, 8)], 1):
                questions_data.append(['', '', f'{i}. {aspect}', ''])
            questions_data.append(['', '', f'{i+1}. Other (Please specify)', ''])
            questions_data.append(['', '', '', ''])
        elif q % 4 == 0:  # Multi-answer
            questions_data.append([q_num, 'Required' if q % 2 == 0 else 'Optional', 
                                 f'Select all factors that influence your opinion on {topic}', 'M/A'])
            factors = ['Personal experience', 'Word of mouth', 'Online reviews', 'Price comparison', 
                      'Brand reputation', 'Expert recommendations', 'Social media', 'Advertising']
            for i, factor in enumerate(factors[:random.randint(5, 7)], 1):
                questions_data.append(['', '', f'{i}. {factor}', ''])
            questions_data.append(['', '', '', ''])
        else:  # Single answer
            has_fa = q % 7 == 2
            questions_data.append([q_num, 'Required' if q % 2 == 0 else 'Optional', 
                                 f'How would you rate the importance of {topic}?', 'S/A+FA' if has_fa else 'S/A'])
            levels = ['Not important at all', 'Slightly important', 'Moderately important', 'Very important', 'Extremely important']
            for i, level in enumerate(levels, 1):
                questions_data.append(['', '', f'{i}. {level}', ''])
            if has_fa:
                questions_data.append(['', '', '6. Other perspective (Please explain)', ''])
            questions_data.append(['', '', '', ''])
    
    df = pd.DataFrame(questions_data, columns=['Question_ID', 'Requirement', 'Question_Text', 'Type'])
    return df

def create_survey_data_sheet(num_respondents=150, survey_type="automotive"):
    """Create survey response data with proper binary structure"""
    
    np.random.seed(random.randint(1, 3000))
    data = {}
    
    # NO column with different ID ranges for each survey type
    base_ids = {
        'automotive': 800000,
        'fitness': 900000,
        'entertainment': 1000000,
        'education': 1100000,
        'environment': 1200000
    }
    base_id = base_ids.get(survey_type, 100000)
    data['NO'] = [base_id + i * 1567 for i in range(num_respondents)]
    
    # Standard demographic questions Q-001 to Q-005 (same structure for all)
    demo_questions = ['Q-001', 'Q-002', 'Q-003', 'Q-004', 'Q-005']
    demo_options = [12, 8, 7, 8, 7]
    demo_fa_questions = {'Q-003': 7, 'Q-004': 8}
    
    for q_id, num_opts in zip(demo_questions, demo_options):
        # Create binary columns
        for opt in range(1, num_opts + 1):
            data[f'{q_id}_{opt}'] = [0] * num_respondents
        
        # Add FA column if needed
        if q_id in demo_fa_questions:
            fa_opt = demo_fa_questions[q_id]
            data[f'{q_id}_{fa_opt}_SA'] = [None] * num_respondents
        
        # Fill data
        for idx in range(num_respondents):
            chosen = np.random.randint(1, num_opts + 1)
            data[f'{q_id}_{chosen}'][idx] = 1
            
            # Fill FA if applicable
            if q_id in demo_fa_questions and chosen == demo_fa_questions[q_id]:
                if q_id == 'Q-003':
                    data[f'{q_id}_{fa_opt}_SA'][idx] = random.choice([
                        'Trade school', 'Online certification', 'Military training'
                    ])
                elif q_id == 'Q-004':
                    data[f'{q_id}_{fa_opt}_SA'][idx] = random.choice([
                        'Freelancer', 'Consultant', 'Gig worker', 'Entrepreneur'
                    ])
    
    # Theme-specific questions Q-006 to Q-015 (different for each survey type)
    if survey_type == "automotive":
        # Automotive-specific data structure
        # Q-006: Vehicle ownership (5 options)
        for i in range(1, 6):
            data[f'Q-006_{i}'] = [0] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 6)
            data[f'Q-006_{chosen}'][idx] = 1
            
        # Q-007: Vehicle type (11 options with FA)
        for i in range(1, 12):
            data[f'Q-007_{i}'] = [0] * num_respondents
        data['Q-007_11_SA'] = [None] * num_respondents
        for idx in range(num_respondents):
            chosen = np.random.randint(1, 12)
            data[f'Q-007_{chosen}'][idx] = 1
            if chosen == 11:
                data['Q-007_11_SA'][idx] = random.choice(['RV', 'ATV', 'Boat'])
        
        # Continue with other automotive questions...
        # Q-008: Brand preferences (multi-answer)
        for i in range(1, 15):
            data[f'Q-008_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.8, 0.2])
    
    # Add similar detailed implementations for other survey types...
    # For brevity, I'll add a simplified version for the remaining types
    
    # Generate data for Q-006 to Q-015 based on survey type
    q006_to_q015_configs = {
        'automotive': [(5, False), (11, True), (14, False), (6, False), (14, True), (6, False), (6, False), (5, False), (10, False), (None, True)],
        'fitness': [(7, False), (14, True), (8, False), (12, False), (12, True), (11, False), (9, False), (8, False), (10, False), (None, True)],
        'entertainment': [(6, False), (14, True), (12, False), (11, False), (14, True), (9, False), (12, False), (10, False), (6, False), (None, True)],
        'education': [(11, True), (11, False), (14, True), (6, False), (11, False), (5, False), (8, False), (8, False), (9, False), (None, True)],
        'environment': [(5, False), (13, True), (11, False), (5, False), (10, False), (9, False), (10, False), (11, True), (10, False), (None, True)]
    }
    
    configs = q006_to_q015_configs.get(survey_type, q006_to_q015_configs['automotive'])
    
    for q_idx, (num_opts, has_fa) in enumerate(configs, start=6):
        q_str = f'Q-{str(q_idx).zfill(3)}'
        
        if num_opts is None:  # Free answer question
            data[q_str] = [random.choice([
                'Positive experience overall', 'Some areas need improvement', 
                'Very satisfied with the service', 'Good quality and value',
                'Professional and helpful', None, None, None
            ]) for _ in range(num_respondents)]
        elif q_idx in [8, 10, 12]:  # Multi-answer questions
            for i in range(1, num_opts + 1):
                data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.7, 0.3])
            if has_fa:
                data[f'{q_str}_{num_opts}_FA'] = [random.choice([
                    'Additional option', 'Custom requirement', None, None
                ]) for _ in range(num_respondents)]
        else:  # Single answer questions
            for i in range(1, num_opts + 1):
                data[f'{q_str}_{i}'] = [0] * num_respondents
            
            if has_fa:
                data[f'{q_str}_{num_opts}_SA'] = [None] * num_respondents
            
            for idx in range(num_respondents):
                chosen = np.random.randint(1, num_opts + 1)
                data[f'{q_str}_{chosen}'][idx] = 1
                if has_fa and chosen == num_opts:
                    data[f'{q_str}_{num_opts}_SA'][idx] = random.choice([
                        'Custom answer', 'Special case', 'Other option'
                    ])
    
    # Q-016 to Q-086: Generate based on the pattern established in question master
    for q in range(16, 87):
        q_str = f'Q-{str(q).zfill(3)}'
        
        if q % 9 == 0:  # Free answer
            data[q_str] = [random.choice([
                'Excellent service and support', 'Could be more user-friendly', 'Great value for money',
                'Professional and reliable', 'Innovative features', 'Room for improvement',
                None, None, None
            ]) for _ in range(num_respondents)]
        elif q % 6 == 0:  # Multi-answer with FA
            num_subs = random.randint(6, 8)
            for i in range(1, num_subs + 2):
                data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.75, 0.25])
            data[f'{q_str}_{num_subs+1}_FA'] = [random.choice([
                'Additional consideration', 'Custom need', None, None
            ]) for _ in range(num_respondents)]
        elif q % 4 == 0:  # Multi-answer
            num_subs = random.randint(5, 7)
            for i in range(1, num_subs + 1):
                data[f'{q_str}_{i}'] = np.random.choice([0, 1], num_respondents, p=[0.7, 0.3])
        else:  # Single answer
            has_fa = q % 7 == 2
            num_opts = 5  # Importance scale
            
            for i in range(1, num_opts + 1):
                data[f'{q_str}_{i}'] = [0] * num_respondents
            
            if has_fa:
                data[f'{q_str}_6_FA'] = [None] * num_respondents
                actual_opts = 6
            else:
                actual_opts = num_opts
            
            for idx in range(num_respondents):
                if has_fa:
                    chosen = np.random.randint(1, 7)  # 1-6 for options, 6 can trigger FA
                    if chosen <= 5:
                        data[f'{q_str}_{chosen}'][idx] = 1
                    else:  # chosen == 6, FA case
                        data[f'{q_str}_6_FA'][idx] = random.choice([
                            'Different perspective', 'Unique consideration', 'Alternative view'
                        ])
                else:
                    chosen = np.random.randint(1, num_opts + 1)
                    data[f'{q_str}_{chosen}'][idx] = 1
    
    # Add timestamp
    base_dates = {
        'automotive': datetime(2025, 1, 10, 9, 0, 0),
        'fitness': datetime(2025, 2, 5, 10, 30, 0),
        'entertainment': datetime(2025, 2, 20, 14, 15, 0),
        'education': datetime(2025, 3, 5, 11, 45, 0),
        'environment': datetime(2025, 3, 20, 16, 0, 0)
    }
    base_date = base_dates.get(survey_type, datetime(2025, 1, 1, 9, 0, 0))
    
    data['Response_DateTime'] = [base_date + timedelta(
        days=random.randint(0, 25),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    ) for _ in range(num_respondents)]
    
    # Create DataFrame with proper column ordering
    df = pd.DataFrame(data)
    cols = ['NO'] + [col for col in sorted(df.columns) if col.startswith('Q-')] + ['Response_DateTime']
    df = df[cols]
    
    return df

def create_survey_file(survey_name, survey_type, num_respondents):
    """Create a complete survey Excel file"""
    
    print(f"Creating {survey_name}...")
    
    question_master = create_question_master_sheet(survey_type)
    survey_data = create_survey_data_sheet(num_respondents, survey_type)
    
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
    """Create 5 diverse survey files"""
    
    print("Creating 5 Internet Survey Excel files with diverse content...")
    print("="*75)
    
    surveys = [
        ("Automotive_Vehicle_Survey_2025", "automotive", 152),
        ("Fitness_Health_Survey_2025", "fitness", 168),
        ("Entertainment_Media_Survey_2025", "entertainment", 144),
        ("Education_Learning_Survey_2025", "education", 161),
        ("Environmental_Awareness_Survey_2025", "environment", 137)
    ]
    
    created_files = []
    
    print("Standardized demographic questions Q-001 to Q-005:")
    print("  Q-001: Age and Gender")
    print("  Q-002: Annual Household Income") 
    print("  Q-003: Education Level")
    print("  Q-004: Employment Status")
    print("  Q-005: Geographic Region")
    print("\nUnique theme-specific questions Q-006 onwards for each survey")
    print()
    
    for survey_name, survey_type, num_resp in surveys:
        file_path = create_survey_file(survey_name, survey_type, num_resp)
        created_files.append(file_path)
        print()
    
    print("="*75)
    print("✅ All 5 diverse survey files created successfully!")
    print("\nFiles created:")
    for i, file_path in enumerate(created_files, 1):
        print(f"{i}. {file_path}")
    
    print("\n🎯 Key features:")
    print("✓ Standardized Q-001 to Q-005 demographics across all surveys")
    print("✓ Completely different themes and questions Q-006+ for each survey")
    print("✓ Diverse question types: S/A, M/A, M/A+FA, S/A+FA, FA")
    print("✓ Realistic survey topics: Automotive, Fitness, Entertainment, Education, Environment")
    print("✓ Proper binary column structure for all Single Answer questions")
    print("✓ Unique respondent counts and timestamps for each survey")
    print("✓ Q-016 to Q-086 with varied topics and question formats")

if __name__ == "__main__":
    main()