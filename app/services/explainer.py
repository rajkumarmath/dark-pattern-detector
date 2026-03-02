# app/services/explainer.py
from typing import List, Dict

class Explainer:
    """
    Generate human-readable explanations for detected dark patterns
    """
    
    def __init__(self):
        self.pattern_explanations = {
            1: {
                'name': 'Forced Action',
                'description': 'Forces users to take an action to continue',
                'why_manipulative': [
                    'Removes user choice and autonomy',
                    'Creates artificial barriers to content',
                    'Exploits user\'s desire to proceed',
                    'Forces unnecessary account creation'
                ]
            },
            2: {
                'name': 'Confirmshaming',
                'description': 'Guilts users into choosing option they don\'t want',
                'why_manipulative': [
                    'Uses emotional manipulation',
                    'Makes users feel bad for choosing no',
                    'Frames decline as the "wrong" choice',
                    'Exploits social pressure'
                ]
            },
            3: {
                'name': 'Hidden Costs',
                'description': 'Reveals unexpected costs late in the process',
                'why_manipulative': [
                    'Deceives users about true cost',
                    'Wastes user\'s time entering information',
                    'Creates sunk cost fallacy - users already invested',
                    'Often appears only at final checkout step'
                ]
            },
            4: {
                'name': 'Interface Interference',
                'description': 'Hides or obscures options users might want',
                'why_manipulative': [
                    'Makes preferred options difficult to find',
                    'Exploits UI conventions and expectations',
                    'Frustrates users into giving up',
                    'Uses visual tricks to guide choices'
                ]
            },
            5: {
                'name': 'Obstruction',
                'description': 'Creates hurdles to complete user-initiated actions',
                'why_manipulative': [
                    'Wastes user time deliberately',
                    'Makes leaving or canceling difficult',
                    'Tests user persistence',
                    'Creates friction for unwanted actions'
                ]
            }
        }
    
    def generate_explanation(self, pattern_type: int, 
                            risk_score: float,
                            manipulative_phrases: List[str]) -> str:
        """
        Generate detailed explanation of why it's manipulative
        """
        if pattern_type == 0:
            return "No dark patterns detected. The interface appears ethical and user-friendly."
        
        pattern_info = self.pattern_explanations.get(pattern_type, {
            'name': 'Unknown Pattern',
            'description': 'Pattern detected but not fully classified',
            'why_manipulative': ['This pattern may manipulate user behavior']
        })
        
        explanation = f"⚠️ **{pattern_info['name']} Detected**\n\n"
        explanation += f"**What:** {pattern_info['description']}\n\n"
        explanation += "**Why it's manipulative:**\n"
        
        for point in pattern_info['why_manipulative']:
            explanation += f"• {point}\n"
        
        if manipulative_phrases:
            explanation += f"\n**Key manipulative phrases:** {', '.join(manipulative_phrases[:3])}\n"
        
        # Determine risk level emoji
        if risk_score >= 70:
            risk_emoji = "🔴"
            risk_text = "High"
        elif risk_score >= 40:
            risk_emoji = "🟡"
            risk_text = "Medium"
        else:
            risk_emoji = "🟢"
            risk_text = "Low"
        
        explanation += f"\n**Risk Level:** {risk_emoji} {risk_text} ({risk_score:.1f}/100)\n"
        
        return explanation