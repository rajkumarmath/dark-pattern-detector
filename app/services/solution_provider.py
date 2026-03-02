# app/services/solution_provider.py
from typing import Dict, List, Optional
from datetime import datetime

class SolutionProvider:
    """
    Provides ethical design solutions for detected dark patterns
    """
    
    def __init__(self):
        self.solution_templates = {
            "forced_action": {
                "problem": "Forcing users to take actions they don't want",
                "solutions": [
                    {
                        "title": "Make actions optional",
                        "description": "Allow users to continue without forced actions",
                        "implementation": """
<!-- Instead of forcing sign-up -->
<div class="optional-signup">
  <p>Want to save your progress? Create an account (optional)</p>
  <button class="continue-as-guest">Continue as Guest</button>
  <button class="sign-up">Sign Up</button>
</div>
"""
                    },
                    {
                        "title": "Provide preview access",
                        "description": "Let users preview content before requiring action",
                        "implementation": "Show limited preview with clear upgrade path"
                    }
                ],
                "checklist": [
                    "Can users access core functionality without accounts?",
                    "Is there a 'skip' option clearly visible?",
                    "Are forced actions clearly explained?"
                ]
            },
            
            "confirmshaming": {
                "problem": "Using guilt or shame to manipulate choices",
                "solutions": [
                    {
                        "title": "Use neutral language",
                        "description": "Replace shaming language with neutral options",
                        "implementation": """
<!-- Instead of shaming -->
<div class="opt-out">
  <label>
    <input type="checkbox" checked> 
    No thanks, I don't want to save money ❌
  </label>
</div>

<!-- Use neutral language -->
<div class="opt-out">
  <label>
    <input type="checkbox"> 
    Receive exclusive offers (optional)
  </label>
  <p class="note">You can unsubscribe anytime</p>
</div>
"""
                    },
                    {
                        "title": "Equal visual weight",
                        "description": "Make all options visually equal",
                        "implementation": "Use same font size, color, and button style for all choices"
                    }
                ],
                "checklist": [
                    "Are all options presented neutrally?",
                    "Is there guilt-inducing language?",
                    "Are decline options easy to find?"
                ]
            },
            
            "hidden_costs": {
                "problem": "Revealing costs late in the process",
                "solutions": [
                    {
                        "title": "Show all costs upfront",
                        "description": "Display total price including all fees from the start",
                        "implementation": """
<!-- Instead of hiding fees -->
<div class="price">
  <span class="base-price">$49.99</span>
  <span class="fine-print">+ fees at checkout</span>
</div>

<!-- Show all costs upfront -->
<div class="price">
  <span class="total-price">$54.98</span>
  <div class="price-breakdown">
    <span>Base: $49.99</span>
    <span>Processing: $3.99</span>
    <span>Tax: $1.00</span>
  </div>
</div>
"""
                    },
                    {
                        "title": "Price breakdown tooltip",
                        "description": "Show detailed breakdown on hover/click",
                        "implementation": "Add ℹ️ icon with detailed cost breakdown"
                    }
                ],
                "checklist": [
                    "Is the full price visible on first page?",
                    "Are all fees explained?",
                    "Is there a price breakdown?"
                ]
            },
            
            "interface_interference": {
                "problem": "Hiding or obscuring user preferences",
                "solutions": [
                    {
                        "title": "Equal visibility",
                        "description": "Make all options equally visible",
                        "implementation": """
/* Instead of tiny unsubscribe link */
.unsubscribe-link {
  font-size: 8px;
  color: #999;
  position: absolute;
  bottom: -100px;
}

/* Make it accessible */
.unsubscribe-link {
  font-size: 14px;
  color: #666;
  margin: 20px 0;
  display: block;
  text-decoration: underline;
  cursor: pointer;
}
"""
                    },
                    {
                        "title": "Standard interactions",
                        "description": "Follow platform conventions for common actions",
                        "implementation": "Place unsubscribe in account settings, not hidden in footer"
                    }
                ],
                "checklist": [
                    "Are all options similarly styled?",
                    "Is unsubscribe easy to find?",
                    "Are settings logically organized?"
                ]
            },
            
            "obstruction": {
                "problem": "Creating barriers to user actions",
                "solutions": [
                    {
                        "title": "Streamline processes",
                        "description": "Make leaving as easy as joining",
                        "implementation": """
# Instead of requiring phone calls
def cancel_subscription():
    # Require phone call
    return "Call us during business hours"

# Provide online cancellation
def cancel_subscription(user_id):
    '''One-click cancellation'''
    # Verify user
    if authenticate(user_id):
        # Cancel immediately
        subscription.cancel()
        # Send confirmation
        send_email("Cancelled", user_id)
        return "✓ Subscription cancelled"
"""
                    },
                    {
                        "title": "Immediate confirmation",
                        "description": "Confirm actions instantly without delays",
                        "implementation": "Send confirmation email immediately, don't make users wait"
                    }
                ],
                "checklist": [
                    "Can users cancel online?",
                    "Is there unnecessary waiting?",
                    "Are forms unnecessarily long?"
                ]
            }
        }
        
        # General ethical design principles
        self.general_principles = [
            {
                "principle": "Transparency",
                "description": "Be clear about what users are agreeing to",
                "example": "Use plain language, avoid legalese"
            },
            {
                "principle": "User Control",
                "description": "Let users make informed choices",
                "example": "Provide clear opt-in/opt-out options"
            },
            {
                "principle": "Respect Time",
                "description": "Don't waste users' time with unnecessary steps",
                "example": "Streamline processes, avoid delays"
            },
            {
                "principle": "Visual Honesty",
                "description": "Don't use visual tricks to manipulate",
                "example": "Equal styling for all options"
            }
        ]
    
    def get_solutions(self, pattern_type: int, context: str = None) -> Dict:
        """Get comprehensive solutions for detected pattern"""
        pattern_names = ['none', 'forced_action', 'confirmshaming', 
                        'hidden_costs', 'interface_interference', 'obstruction']
        
        pattern_name = pattern_names[pattern_type]
        
        if pattern_type == 0:
            return {
                "has_issues": False,
                "message": "No dark patterns detected! Your design appears ethical.",
                "principles": self.general_principles,
                "suggestions": [
                    "Keep being transparent with users",
                    "Continue testing with real users",
                    "Document your ethical design choices"
                ]
            }
        
        template = self.solution_templates.get(pattern_name, {})
        
        # Customize based on context
        solutions = template.get("solutions", [])
        if context == "checkout" and pattern_name == "hidden_costs":
            solutions.append({
                "title": "Add price comparison",
                "description": "Show how your price compares to alternatives",
                "implementation": "Include competitor pricing or industry averages"
            })
        elif context == "cancellation" and pattern_name == "obstruction":
            solutions.append({
                "title": "Exit survey (optional)",
                "description": "Ask why they're leaving, but don't force it",
                "implementation": "Optional feedback form after cancellation"
            })
        
        # Generate implementation timeline
        timeline = {
            "immediate": [s["title"] for s in solutions[:2]],
            "short_term": [s["title"] for s in solutions[2:4]] if len(solutions) > 2 else [],
            "long_term": ["Conduct user testing", "Review all user flows", "Create design system"]
        }
        
        return {
            "has_issues": True,
            "pattern": pattern_name,
            "problem": template.get("problem", "Manipulative design pattern detected"),
            "solutions": solutions,
            "checklist": template.get("checklist", []),
            "timeline": timeline,
            "principles": self.general_principles,
            "resources": [
                "https://www.deceptive.design/",
                "https://ethicaldesign.org/",
                "https://humanebydesign.com/"
            ]
        }
    
    def generate_report(self, detection_results: Dict) -> str:
        """Generate comprehensive improvement report"""
        pattern_type = detection_results.get("pattern_type", 0)
        context = detection_results.get("context", "default")
        
        solutions = self.get_solutions(pattern_type, context)
        
        if not solutions["has_issues"]:
            return f"""
# ✅ Ethical Design Report
**Your design passes our ethical check!**

{solutions['message']}

## 🌟 Ethical Design Principles to Maintain:
{chr(10).join(f'- **{p["principle"]}**: {p["description"]}' for p in solutions["principles"])}

## 📈 Next Steps:
{chr(10).join(f'- {s}' for s in solutions["suggestions"])}

---
*Generated by Dark Pattern Detector - Making the web more ethical, one design at a time*
"""
        
        # Build improvement report
        report = f"""
# 🚨 Dark Pattern Improvement Report

## 📊 Detection Summary
- **Pattern Detected:** {solutions['pattern']}
- **Problem:** {solutions['problem']}
- **Risk Level:** {detection_results.get('risk_score', {}).get('level', 'unknown')}

## 🎯 Immediate Solutions (Do Today)
"""
        
        for i, s in enumerate(solutions['solutions'][:2]):
            report += f"""
### {i+1}. {s['title']}
{s['description']}

Implementation Example:
{s['implementation']}
"""
        
        report += """
## 📋 Implementation Checklist
"""
        for item in solutions['checklist']:
            report += f"- [ ] {item}\n"
        
        report += """
## 🗓️ Suggested Timeline
### Immediate (Next 24h)
"""
        for item in solutions['timeline']['immediate']:
            report += f"- {item}\n"
        
        report += """
### Short-term (This Week)
"""
        if solutions['timeline']['short_term']:
            for item in solutions['timeline']['short_term']:
                report += f"- {item}\n"
        else:
            report += "- Continue monitoring\n"
        
        report += """
### Long-term (Next Month)
"""
        for item in solutions['timeline']['long_term']:
            report += f"- {item}\n"
        
        report += """
## 🌟 Ethical Design Principles
"""
        for p in solutions['principles']:
            report += f"- **{p['principle']}**: {p['description']}\n"
        
        report += """
## 📚 Resources
"""
        for url in solutions['resources']:
            report += f"- {url}\n"
        
        report += """
---
*Remember: Ethical design builds trust and long-term user loyalty.*
"""
        return report