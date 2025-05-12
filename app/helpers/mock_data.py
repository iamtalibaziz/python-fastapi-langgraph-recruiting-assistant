def resume_node_mock_data() -> dict:
    return {'name': 'John', 'email': 'john.test@gmail.com', 'phone': '+91240343093', 'experience': 'Over 8+ years of experience with JavaScript, Node.js, MongoDB, Express.js, Nest.js, TypeScript, ES6, React.js and Redux, jQuery, MySQL, Ajax, Socket.IO, Redis. Experienced in developing large Application. Experienced in implementing Payment system using Stripe. Experienced in writing complex database queries.', 'skills': ['JavaScript', 'Node.js', 'MongoDB', 'Express.js', 'Nest.js', 'TypeScript', 'ES6', 'React.js and Redux', 'jQuery', 'MySQL', 'Ajax', 'Socket.IO', 'Redis', 'Python', 'FastAPI', 'Generative AI'], 'qualifications': ['MCA from Sikkim Manipal University (January, 2014)'], 'certifications': [], 'publications': [], 'projects': []}

def jd_node_mock_data() -> dict:
    return {'experience': '5 years', 'skills': ['JavaScript', 'Python', 'AI', 'Generative AI', 'MySQL'], 'qualifications': ['B.Tech', 'MCA']}

def compare_node_mock_data() -> dict:
    return {
            "fit_score": "Strong Fit",
            "comparison_matrix": {
                "skills_matched": ["JavaScript", "Python", "Generative AI", "MySQL"],
                "experience": "Over 8+ years"
            },
            "explanation": "The candidate has over 8 years of experience, exceeding the required 5 years. They possess strong expertise in 4 out of 5 required skills (JavaScript, Python, Generative AI, MySQL) and meet the qualification requirement with an MCA. This makes them a strong fit for the position."
        }