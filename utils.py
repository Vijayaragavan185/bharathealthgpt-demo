# utils.py - Working utility functions
import re
from typing import List, Dict, Tuple
from googletrans import Translator
from demo_data import MEDICAL_KNOWLEDGE, LANGUAGE_CODES

class SimpleMedicalAI:
    def __init__(self):
        self.translator = Translator()
        self.medical_data = MEDICAL_KNOWLEDGE
    
    def detect_symptoms(self, text: str, language: str = 'english') -> List[Dict]:
        """Detect symptoms in user input"""
        text_lower = text.lower()
        detected_symptoms = []
        
        for symptom, data in self.medical_data['symptoms'].items():
            # Check in both English and local language
            if (data['english'].lower() in text_lower or 
                data.get(language, '').lower() in text_lower or
                symptom.lower() in text_lower):
                
                detected_symptoms.append({
                    'symptom': symptom,
                    'local_name': data.get(language, data['english']),
                    'english_name': data['english'],
                    'emergency': data['emergency'],
                    'recommendations': data['recommendations']
                })
        
        return detected_symptoms
    
    def generate_response(self, user_input: str, language: str = 'english') -> Dict:
        """Generate medical response based on input"""
        try:
            # Translate to English if needed
            if language != 'english':
                translated_input = self.translator.translate(user_input, dest='en').text
            else:
                translated_input = user_input
            
            # Detect symptoms
            symptoms = self.detect_symptoms(translated_input, language)
            
            # Check for emergency
            emergency_flag = any(symptom['emergency'] for symptom in symptoms)
            
            # Generate response
            if not symptoms:
                response = self.get_general_response(language)
            else:
                response = self.create_medical_response(symptoms, language, emergency_flag)
            
            return {
                'response': response,
                'symptoms': symptoms,
                'emergency': emergency_flag,
                'language': language,
                'confidence': 0.85 if symptoms else 0.6
            }
            
        except Exception as e:
            return {
                'response': f"Sorry, I encountered an error: {str(e)}",
                'symptoms': [],
                'emergency': False,
                'language': language,
                'confidence': 0.0
            }
    
    def create_medical_response(self, symptoms: List[Dict], language: str, emergency: bool) -> str:
        """Create detailed medical response"""
        responses = self.medical_data['responses'].get(language, self.medical_data['responses']['english'])
        
        if emergency:
            response = responses['emergency'] + "\n\n"
        else:
            response = responses['general'] + "\n\n"
        
        # Add recommendations for each symptom
        for i, symptom in enumerate(symptoms, 1):
            response += f"{i}. {symptom['local_name']} ({symptom['english_name']}):\n"
            for rec in symptom['recommendations'][:3]:  # Limit to 3 recommendations
                response += f"   • {rec}\n"
            response += "\n"
        
        # Add disclaimer
        if language == 'hindi':
            response += "\n⚠️ अस्वीकरण: यह केवल AI सुझाव है। कृपया योग्य डॉक्टर से सलाह लें।"
        else:
            response += "\n⚠️ Disclaimer: This is AI-generated advice. Please consult a qualified doctor."
        
        return response
    
    def get_general_response(self, language: str) -> str:
        """Get general response when no symptoms detected"""
        if language == 'hindi':
            return "मुझे आपके लक्षण स्पष्ट रूप से समझ नहीं आए। कृपया अपनी समस्या विस्तार से बताएं जैसे: बुखार, सिरदर्द, पेट दर्द आदि।"
        else:
            return "I couldn't clearly identify specific symptoms. Please describe your health concern in more detail, such as: fever, headache, stomach pain, etc."

# Simple symptom checker for demo
class SymptomChecker:
    def __init__(self):
        self.common_symptoms = {
            'fever': ['fever', 'बुखार', 'temperature'],
            'headache': ['headache', 'सिरदर्द', 'head pain'],
            'cough': ['cough', 'खांसी', 'कफ'],
            'stomach_pain': ['stomach pain', 'पेट दर्द', 'abdominal pain'],
            'nausea': ['nausea', 'जी मिचलाना', 'vomiting']
        }
    
    def check_symptoms(self, selected_symptoms: List[str], language: str = 'english') -> str:
        """Generate advice based on selected symptoms"""
        if not selected_symptoms:
            return "Please select at least one symptom."
        
        advice = []
        emergency = False
        
        for symptom in selected_symptoms:
            if symptom.lower() == 'chest pain':
                emergency = True
                break
        
        if emergency:
            if language == 'hindi':
                return "⚠️ आपातकाल! तुरंत अस्पताल जाएं या 102 पर कॉल करें!"
            else:
                return "⚠️ EMERGENCY! Please go to hospital immediately or call emergency services!"
        
        # General advice based on symptoms
        if 'fever' in [s.lower() for s in selected_symptoms]:
            if language == 'hindi':
                advice.append("बुखार के लिए: आराम करें, तरल पदार्थ पिएं, पैरासिटामोल ले सकते हैं")
            else:
                advice.append("For fever: Rest, drink fluids, take paracetamol if needed")
        
        if 'headache' in [s.lower() for s in selected_symptoms]:
            if language == 'hindi':
                advice.append("सिरदर्द के लिए: अंधेरे कमरे में आराम करें, ठंडी पट्टी लगाएं")
            else:
                advice.append("For headache: Rest in dark room, apply cold compress")
        
        if not advice:
            if language == 'hindi':
                advice.append("सामान्य सलाह: पर्याप्त आराम करें, पानी पिएं, यदि समस्या बनी रहे तो डॉक्टर से मिलें")
            else:
                advice.append("General advice: Get adequate rest, stay hydrated, consult doctor if symptoms persist")
        
        return "\n".join(advice)
