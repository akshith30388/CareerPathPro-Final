"""
Rule-based career recommendation engine.
Maps assessment career scores to specific career recommendations with roadmaps.
"""

CAREER_DATABASE = {
    'Technology': {
        'careers': [
            {
                'name': 'Software Developer',
                'description': 'Design, build, and maintain software applications. Work with various programming languages and frameworks to create digital solutions.',
                'skills': 'Python, JavaScript, Java, SQL, Git, Problem Solving, Algorithms, Data Structures',
                'roadmap': [
                    'Learn Python or JavaScript fundamentals',
                    'Study data structures and algorithms',
                    'Build 3-5 personal projects',
                    'Learn a web framework (Django/React/Node.js)',
                    'Learn version control with Git',
                    'Contribute to open-source projects',
                    'Apply for internships or entry-level positions',
                    'Build a strong GitHub portfolio',
                ]
            },
            {
                'name': 'Data Scientist',
                'description': 'Analyze large datasets to extract insights and build predictive models using statistical methods and machine learning.',
                'skills': 'Python, R, SQL, Machine Learning, Statistics, TensorFlow, Pandas, NumPy, Data Visualization',
                'roadmap': [
                    'Master Python and R programming',
                    'Study statistics and probability',
                    'Learn data manipulation with Pandas/NumPy',
                    'Study machine learning algorithms',
                    'Practice on Kaggle competitions',
                    'Learn TensorFlow/PyTorch for deep learning',
                    'Build end-to-end data science projects',
                    'Get certified (Google, IBM, or Coursera)',
                ]
            },
        ]
    },
    'Engineering': {
        'careers': [
            {
                'name': 'Civil Engineer',
                'description': 'Design and oversee construction of infrastructure projects including buildings, bridges, roads, and water systems.',
                'skills': 'AutoCAD, Structural Analysis, Project Management, Mathematics, Physics, Civil 3D',
                'roadmap': [
                    'Complete B.Tech/B.E in Civil Engineering',
                    'Learn AutoCAD and Civil 3D software',
                    'Intern at construction or consulting firms',
                    'Study structural analysis and design',
                    'Get PE (Professional Engineer) certification',
                    'Work on infrastructure projects',
                    'Pursue M.Tech for specialization',
                    'Join professional bodies like ASCE',
                ]
            },
            {
                'name': 'Mechanical Engineer',
                'description': 'Design and develop mechanical systems and products. Work in manufacturing, automotive, aerospace, and energy sectors.',
                'skills': 'SolidWorks, AutoCAD, Thermodynamics, Fluid Mechanics, CNC Programming, MATLAB',
                'roadmap': [
                    'Complete B.Tech in Mechanical Engineering',
                    'Learn CAD software (SolidWorks/AutoCAD)',
                    'Study thermodynamics and fluid mechanics',
                    'Intern at manufacturing companies',
                    'Learn FEA and simulation tools',
                    'Get Six Sigma or PMP certification',
                    'Specialize in robotics or automotive',
                    'Pursue research or industry roles',
                ]
            },
        ]
    },
    'Science': {
        'careers': [
            {
                'name': 'Research Scientist',
                'description': 'Conduct scientific research to advance knowledge in fields like biology, chemistry, physics, or environmental science.',
                'skills': 'Research Methodology, Data Analysis, Scientific Writing, Laboratory Skills, SPSS, R',
                'roadmap': [
                    'Complete B.Sc in relevant science field',
                    'Develop strong laboratory skills',
                    'Publish undergraduate research papers',
                    'Pursue M.Sc with research focus',
                    'Apply for PhD programs',
                    'Attend scientific conferences',
                    'Build network in academic community',
                    'Apply for research grants',
                ]
            },
            {
                'name': 'Biomedical Engineer',
                'description': 'Combine engineering principles with medical sciences to develop healthcare technologies and medical devices.',
                'skills': 'Biology, Engineering Principles, MATLAB, Medical Imaging, Biomaterials, Signal Processing',
                'roadmap': [
                    'Complete B.Tech in Biomedical Engineering',
                    'Learn medical device regulations',
                    'Study human anatomy and physiology',
                    'Intern at hospitals or med-tech companies',
                    'Learn signal processing and imaging',
                    'Get FDA/CE marking knowledge',
                    'Pursue specialization in prosthetics/imaging',
                    'Work with healthcare startups or hospitals',
                ]
            },
        ]
    },
    'Business': {
        'careers': [
            {
                'name': 'Business Analyst',
                'description': 'Bridge the gap between IT and business, analyzing processes and requirements to drive organizational improvements.',
                'skills': 'SQL, Excel, Power BI, Business Process Modeling, Communication, Problem Solving, JIRA',
                'roadmap': [
                    'Complete BBA or B.Tech with MBA',
                    'Learn Excel and data analysis',
                    'Study business process modeling (BPMN)',
                    'Learn SQL for data querying',
                    'Get CBAP or PMP certification',
                    'Work on business case studies',
                    'Learn Agile and Scrum methodology',
                    'Build domain expertise (Finance/Healthcare)',
                ]
            },
            {
                'name': 'Product Manager',
                'description': 'Lead product development teams to create customer-focused solutions. Define product vision, roadmap, and strategy.',
                'skills': 'Product Strategy, User Research, Data Analysis, Communication, JIRA, Figma, Agile',
                'roadmap': [
                    'Get experience in tech or business',
                    'Learn product management frameworks',
                    'Study user research and UX principles',
                    'Take PM courses (Google, Udacity, etc.)',
                    'Build side projects or contribute to startups',
                    'Learn data analysis for product decisions',
                    'Get AIPMM or Pragmatic certification',
                    'Apply for Associate PM programs',
                ]
            },
        ]
    },
    'Creative': {
        'careers': [
            {
                'name': 'UX/UI Designer',
                'description': 'Create user-centered designs for digital products. Focus on user research, wireframing, prototyping, and visual design.',
                'skills': 'Figma, Adobe XD, User Research, Prototyping, HTML/CSS, Usability Testing, Sketch',
                'roadmap': [
                    'Learn design principles and typography',
                    'Master Figma or Adobe XD',
                    'Study UX research methods',
                    'Build a design portfolio',
                    'Learn basic HTML/CSS for dev handoff',
                    'Get Google UX Design Certificate',
                    'Work on freelance design projects',
                    'Join design communities (Dribbble/Behance)',
                ]
            },
            {
                'name': 'Digital Marketer',
                'description': 'Plan and execute digital marketing campaigns across social media, SEO, email, and paid advertising channels.',
                'skills': 'SEO, Google Analytics, Social Media, Content Writing, Email Marketing, PPC, HubSpot',
                'roadmap': [
                    'Learn SEO and content marketing',
                    'Master Google Analytics and Ads',
                    'Build social media marketing skills',
                    'Get Google Digital Marketing Certificate',
                    'Run campaigns for small businesses',
                    'Learn email marketing tools (Mailchimp)',
                    'Study conversion rate optimization',
                    'Build personal brand online',
                ]
            },
        ]
    },
    'Healthcare': {
        'careers': [
            {
                'name': 'Healthcare Professional',
                'description': 'Provide medical care, treatment, and support to patients. Work in hospitals, clinics, or community health settings.',
                'skills': 'Medical Knowledge, Patient Care, Communication, Clinical Skills, Empathy, Medical Software',
                'roadmap': [
                    'Complete MBBS or B.Sc Nursing',
                    'Complete internship/residency',
                    'Get professional medical license',
                    'Develop specialization area',
                    'Stay updated with medical research',
                    'Pursue MD/MS for specialization',
                    'Get board certifications',
                    'Join medical professional bodies',
                ]
            },
        ]
    },
    'Education': {
        'careers': [
            {
                'name': 'Educator/Teacher',
                'description': 'Inspire and educate students at various levels. Design curriculum, teach courses, and mentor the next generation.',
                'skills': 'Subject Expertise, Communication, Curriculum Design, Classroom Management, EdTech Tools',
                'roadmap': [
                    'Complete degree in Education or subject',
                    'Get B.Ed (Bachelor of Education)',
                    'Complete teaching internship',
                    'Learn educational technology',
                    'Develop subject expertise',
                    'Get TET/CTET certification',
                    'Join professional teaching bodies',
                    'Pursue M.Ed for advancement',
                ]
            },
        ]
    },
}

# Default recommendation when no strong signal
DEFAULT_CAREERS = ['Technology', 'Business']


def generate_recommendations(user, assessment_result):
    """
    Generate career recommendations based on assessment results.
    Uses rule-based engine with career score mapping.
    """
    from .models import CareerRecommendation

    # Delete old recommendations for this result
    CareerRecommendation.objects.filter(assessment_result=assessment_result).delete()

    career_scores = assessment_result.career_scores
    percentage = assessment_result.percentage

    if not career_scores:
        # Use score-based defaults
        if percentage >= 70:
            top_categories = ['Technology', 'Science']
        elif percentage >= 50:
            top_categories = ['Business', 'Engineering']
        else:
            top_categories = ['Creative', 'Education']
    else:
        # Sort careers by score
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        top_categories = [c[0] for c in sorted_careers[:3]]
        if not top_categories:
            top_categories = DEFAULT_CAREERS

    recommendations_created = []
    seen_careers = set()

    for category in top_categories:
        if category in CAREER_DATABASE:
            careers = CAREER_DATABASE[category]['careers']
            for career_data in careers[:2]:  # Max 2 per category
                if career_data['name'] not in seen_careers:
                    # Calculate confidence score
                    base_score = career_scores.get(category, 0)
                    total_answers = sum(career_scores.values()) if career_scores else 1
                    confidence = min(95, max(40, (base_score / max(total_answers, 1)) * 100 + percentage * 0.3))

                    rec = CareerRecommendation.objects.create(
                        student=user,
                        assessment_result=assessment_result,
                        recommended_career=career_data['name'],
                        confidence_score=round(confidence, 1),
                        description=career_data['description'],
                        skills_required=career_data['skills'],
                        roadmap=career_data['roadmap'],
                    )
                    recommendations_created.append(rec)
                    seen_careers.add(career_data['name'])

                    if len(recommendations_created) >= 5:
                        return recommendations_created

    # Ensure at least 2 recommendations
    if len(recommendations_created) < 2:
        for category in DEFAULT_CAREERS:
            if category in CAREER_DATABASE and category not in [c for c in top_categories]:
                for career_data in CAREER_DATABASE[category]['careers'][:1]:
                    if career_data['name'] not in seen_careers:
                        CareerRecommendation.objects.create(
                            student=user,
                            assessment_result=assessment_result,
                            recommended_career=career_data['name'],
                            confidence_score=40.0,
                            description=career_data['description'],
                            skills_required=career_data['skills'],
                            roadmap=career_data['roadmap'],
                        )

    return recommendations_created

