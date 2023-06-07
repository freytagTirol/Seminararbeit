import re


class KeywordAnalysis:

    @staticmethod
    def analyze_mda_text(mda_text):
        # Define keywords and their weights for analyzing risk factors
        keyword_weights = {
            'legal': 1.0,
            'regulatory': 0.9,
            'contract': 0.8,
            'violation': 0.7,
            'intellectual property': 0.6,
            'liability': 0.5,
            'litigation': 0.4,
            'environmental': 0.3,
            'antitrust': 0.2,
            'sanctions': 0.2,
            'cybersecurity': 0.2,
            'risk': 1.2,
            'workplace': 1.1,
            'debt': 1.0,
            'losses': 0.9,
            'redundancies': 0.8,
            'workforce reduction': 0.8,
            'data breaches': 0.7,
            'market': 0.6,
            'economic': 0.5,
            'regulations': 0.4,
            'product': 0.6,
            'violations': 0.5,
            'lawsuits': 0.5,
            'governance': 0.4,
            'trading': 0.4,
            'pressures': 0.4,
            'disruptions': 0.5,
            'reputation': 0.6,
            'defects': 0.5,
            'accidents': 0.4,
            'disputes': 0.5,
            'fraud': 0.6,
        }

        # Calculate the likelihood score of future litigation based on keyword matches
        likelihood_score = 0
        for keyword, weight in keyword_weights.items():
            matches = re.findall(r'\b' + re.escape(keyword) + r'\b', mda_text, flags=re.IGNORECASE)
            likelihood_score += len(matches) * weight

        # Determine the likelihood category based on the score
        if likelihood_score <= 2.5:
            likelihood_category = 1  # Low likelihood
        elif likelihood_score <= 12.5:
            likelihood_category = 2  # Moderate likelihood
        elif likelihood_score <= 17.5:
            likelihood_category = 3  # Medium likelihood
        elif likelihood_score <= 25.0:
            likelihood_category = 4  # High likelihood
        else:
            likelihood_category = 5  # Very high likelihood

        # Check for keywords indicating the company will face future litigation
        if likelihood_category >= 3:
            return 1, likelihood_category
        else:
            return 0, likelihood_category
