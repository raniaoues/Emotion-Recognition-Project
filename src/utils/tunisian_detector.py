"""
Tunisian Arabic dialect detection utilities
"""
import re
from typing import List, Dict, Set

class TunisianDialectDetector:
    """Detect Tunisian Arabic dialect in text"""
    
    def __init__(self):
        # Tunisian-specific words and expressions
        self.tunisian_words = {
            # Common Tunisian words
            'برشا', 'ياسر', 'فما', 'كان', 'علاش', 'وقتاش', 'فين', 'شنوة',
            'هكا', 'هكة',  'توا',
            'نقلك', 'نحكيلك',
            'زعمة', 'يزي',
             'تعرف', 'تشوف'
            'مالا', 'علاه', 'كيفاش', 'وين', 'منين', 'لوين',
            'حاجة', 'شي', 'والو', 'ماكان', 'ماعندي',
            'عندي', 'عندك', 'عندو', 'عندها', 'عندنا', 'عندكم',
            'مشي', 'ماشي', 'موش', 'مانيش', 'ماهوش', 'ماهيش',
            'باهي', 'يعيشك',
            'فرحان' 'خايف',
        }
        
        # Tunisian expressions and phrases
        self.tunisian_expressions = {
            'ربي يعطيك الصحة', 'الله يعطيك الصحة', 'يعيشك',
            'ما شاء الله', 'الله يبارك', 'ربي يخليك',
            'كيف راك', 'كيفك', 'لباس', 'شنوة أخبارك',
            'برافو عليك', 'مبروك', 'الله يوفقك', 'بالتوفيق'
        }
        
        # Tunisian cities and regions
        self.tunisian_locations = {
            'تونس', 'صفاقس', 'سوسة', 'القيروان', 'بنزرت', 'قابس',
            'أريانة', 'منوبة', 'نابل', 'زغوان', 'باجة', 'جندوبة',
            'الكاف', 'سليانة', 'القصرين', 'سيدي بوزيد', 'قفصة',
            'توزر', 'قبلي', 'مدنين', 'تطاوين', 'المهدية', 'المنستير'
        }
        
        # Common Tunisian cultural references
        self.cultural_references = {
            'الجوي', 'فرحات', 'لطفي بوشناق', 'صابر الرباعي',
            'أمل بوشوشة', 'إليسا', 'حمزة نمرة', 'بلقيس',
            'الترجي', 'النجم الساحلي', 'الأفريقي', 'النادي الصفاقسي'
        }
    
    def calculate_tunisian_score(self, text: str) -> float:
        """Calculate how likely the text is Tunisian (0-1 score)"""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if not words:
            return 0.0
        
        score = 0.0
        total_checks = 0
        
        # Check for Tunisian words
        tunisian_word_count = sum(1 for word in words if word in self.tunisian_words)
        score += (tunisian_word_count / len(words)) * 0.4
        total_checks += 0.4
        
        # Check for Tunisian expressions
        expression_found = any(expr in text_lower for expr in self.tunisian_expressions)
        if expression_found:
            score += 0.3
        total_checks += 0.3
        
        # Check for Tunisian locations
        location_found = any(loc in text for loc in self.tunisian_locations)
        if location_found:
            score += 0.2
        total_checks += 0.2
        
        # Check for cultural references
        culture_found = any(ref in text for ref in self.cultural_references)
        if culture_found:
            score += 0.1
        total_checks += 0.1
        
        return min(score, 1.0)
    
    def is_tunisian(self, text: str, threshold: float = 0.3) -> bool:
        """Determine if text is likely Tunisian"""
        return self.calculate_tunisian_score(text) >= threshold
    
    def get_tunisian_indicators(self, text: str) -> Dict[str, List[str]]:
        """Get specific Tunisian indicators found in text"""
        indicators = {
            'words': [],
            'expressions': [],
            'locations': [],
            'cultural_refs': []
        }
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Find Tunisian words
        indicators['words'] = [word for word in words if word in self.tunisian_words]
        
        # Find expressions
        indicators['expressions'] = [expr for expr in self.tunisian_expressions if expr in text_lower]
        
        # Find locations
        indicators['locations'] = [loc for loc in self.tunisian_locations if loc in text]
        
        # Find cultural references
        indicators['cultural_refs'] = [ref for ref in self.cultural_references if ref in text]
        
        return indicators