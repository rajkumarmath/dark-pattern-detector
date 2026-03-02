# app/services/ethics_suggester.py
from typing import Dict, List

class EthicsSuggester:
    """
    Suggest ethical alternatives for detected patterns
    """
    
    def __init__(self):
        self.suggestions = {
            1: {  # Forced Action
                'title': 'Replace forced actions with optional choices',
                'alternatives': [
                    'Use "Accept optional cookies" with clear accept/decline',
                    'Offer limited preview without forcing signup',
                    'Provide core functionality without mandatory downloads'
                ],
                'example': 'Instead of: "You must accept to continue"\nUse: "Customize your cookie preferences" with visible options'
            },
            2: {  # Confirmshaming
                'title': 'Use neutral, respectful opt-out language',
                'alternatives': [
                    'Use "No, thank you" instead of shaming language',
                    'Present options as equal choices, not good/bad',
                    'Avoid guilt-tripping language in decline options'
                ],
                'example': 'Instead of: "No thanks, I don\'t want to save money"\nUse: "No, thank you" or "Maybe later"'
            },
            3: {  # Hidden Costs
                'title': 'Show all costs upfront',
                'alternatives': [
                    'Display total price including all fees on first page',
                    'Use tooltips for fee explanations',
                    'Break down costs clearly before checkout'
                ],
                'example': 'Instead of: "Total: $49.99 + fees"\nUse: "Total: $54.99 (includes $5 service fee)" shown early'
            },
            4: {  # Interface Interference
                'title': 'Make all options equally visible',
                'alternatives': [
                    'Use standard-sized buttons for all options',
                    'Place important options in expected locations',
                    'Avoid tiny, hard-to-click links'
                ],
                'example': 'Instead of: Tiny "Unsubscribe" link at bottom\nUse: Prominent "Manage subscription" in account settings'
            },
            5: {  # Obstruction
                'title': 'Streamline user-initiated actions',
                'alternatives': [
                    'Allow one-click cancellation online',
                    'Provide clear, simple forms for account deletion',
                    'Process requests within 24 hours'
                ],
                'example': 'Instead of: "Call during business hours to cancel"\nUse: "Click here to cancel" with confirmation email'
            }
        }
    
    def suggest_corrections(self, pattern_type: int, context: str = None) -> Dict:
        """
        Generate ethical design suggestions
        """
        if pattern_type == 0:
            return {
                'title': 'No corrections needed',
                'alternatives': ['Keep up the ethical design!'],
                'example': 'Your interface appears to be user-friendly and transparent.'
            }
        
        # Get base suggestion
        suggestion = self.suggestions.get(pattern_type, {
            'title': 'Review this pattern for ethical alternatives',
            'alternatives': ['Consider user-centered design principles'],
            'example': 'Test with real users to identify friction points'
        })
        
        # Context-specific enhancements
        if context == 'checkout' and pattern_type == 3:
            suggestion['alternatives'].append('Add a fee calculator before checkout')
        elif context == 'cancellation' and pattern_type == 5:
            suggestion['alternatives'].append('Provide immediate confirmation of cancellation')
        
        return suggestion