# demo_data.py - Sample medical knowledge for demo
MEDICAL_KNOWLEDGE = {
    'symptoms': {
        'fever': {
            'hindi': 'बुखार',
            'english': 'fever',
            'recommendations': [
                'Take rest and drink plenty of fluids',
                'Use paracetamol for high fever',
                'Consult doctor if fever persists for more than 3 days'
            ],
            'emergency': False
        },
        'chest_pain': {
            'hindi': 'छाती में दर्द',
            'english': 'chest pain',
            'recommendations': [
                'SEEK IMMEDIATE MEDICAL ATTENTION',
                'Call emergency services',
                'Do not ignore chest pain'
            ],
            'emergency': True
        },
        'headache': {
            'hindi': 'सिरदर्द',
            'english': 'headache',
            'recommendations': [
                'Rest in a dark, quiet room',
                'Apply cold compress',
                'Stay hydrated',
                'Consult doctor if severe or persistent'
            ],
            'emergency': False
        },
        'stomach_pain': {
            'hindi': 'पेट दर्द',
            'english': 'stomach pain',
            'recommendations': [
                'Avoid solid food temporarily',
                'Drink clear fluids',
                'Apply warm compress',
                'See doctor if pain is severe'
            ],
            'emergency': False
        }
    },
    
    'responses': {
        'hindi': {
            'greeting': 'नमस्ते! मैं आपका AI डॉक्टर हूं। आपकी क्या समस्या है?',
            'emergency': '⚠️ यह एक आपातकालीन स्थिति हो सकती है! तुरंत डॉक्टर से मिलें!',
            'general': 'आपके लक्षणों के आधार पर, मैं निम्नलिखित सुझाव देता हूं:'
        },
        'english': {
            'greeting': 'Hello! I am your AI doctor assistant. What health concern can I help you with?',
            'emergency': '⚠️ This could be an emergency situation! Please seek immediate medical attention!',
            'general': 'Based on your symptoms, here are my recommendations:'
        }
    }
}

LANGUAGE_CODES = {
    'hindi': 'hi',
    'english': 'en',
    'marathi': 'mr',
    'tamil': 'ta',
    'telugu': 'te'
}
