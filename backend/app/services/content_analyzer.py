from typing import List, Dict, Any
import re
from textblob import TextBlob
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# NLTK 리소스 다운로드
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ContentAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def analyze_seo(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """SEO 분석을 수행합니다."""
        seo_score = 0
        suggestions = []
        
        # 제목 길이 확인 (10-60자)
        title_length = len(content["title"])
        if title_length < 10:
            suggestions.append({
                "category": "seo",
                "suggestion": "제목이 너무 짧습니다. 10자 이상으로 작성하세요.",
                "priority": 1
            })
        elif title_length > 60:
            suggestions.append({
                "category": "seo",
                "suggestion": "제목이 너무 깁니다. 60자 이하로 작성하세요.",
                "priority": 2
            })
        else:
            seo_score += 25
        
        # 메타 설명 확인 (50-160자)
        if content.get("meta_description"):
            meta_length = len(content["meta_description"])
            if meta_length < 50:
                suggestions.append({
                    "category": "seo",
                    "suggestion": "메타 설명이 너무 짧습니다. 50자 이상으로 작성하세요.",
                    "priority": 2
                })
            elif meta_length > 160:
                suggestions.append({
                    "category": "seo",
                    "suggestion": "메타 설명이 너무 깁니다. 160자 이하로 작성하세요.",
                    "priority": 2
                })
            else:
                seo_score += 25
        else:
            suggestions.append({
                "category": "seo",
                "suggestion": "메타 설명을 추가하세요.",
                "priority": 1
            })
        
        # 키워드 분석
        if content.get("keywords"):
            keywords = content["keywords"].split(",")
            if len(keywords) < 3:
                suggestions.append({
                    "category": "seo",
                    "suggestion": "키워드를 3개 이상 추가하세요.",
                    "priority": 2
                })
            elif len(keywords) > 10:
                suggestions.append({
                    "category": "seo",
                    "suggestion": "키워드가 너무 많습니다. 10개 이하로 조정하세요.",
                    "priority": 3
                })
            else:
                seo_score += 25
        else:
            suggestions.append({
                "category": "seo",
                "suggestion": "키워드를 추가하세요.",
                "priority": 1
            })
        
        # 본문 길이 확인
        description_length = len(content["description"])
        if description_length < 300:
            suggestions.append({
                "category": "seo",
                "suggestion": "본문이 너무 짧습니다. 300자 이상으로 작성하세요.",
                "priority": 2
            })
        else:
            seo_score += 25
        
        return {
            "score": seo_score,
            "suggestions": suggestions
        }
    
    def analyze_readability(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """가독성 분석을 수행합니다."""
        readability_score = 0
        suggestions = []
        
        text = content["description"]
        
        # 문장 분석
        sentences = sent_tokenize(text)
        avg_sentence_length = sum(len(word_tokenize(s)) for s in sentences) / len(sentences)
        
        if avg_sentence_length > 20:
            suggestions.append({
                "category": "readability",
                "suggestion": f"문장이 평균 {avg_sentence_length:.1f}단어로 너무 깁니다. 더 짧은 문장으로 나누세요.",
                "priority": 2
            })
        else:
            readability_score += 33
        
        # 단락 분석
        paragraphs = text.split("\n\n")
        avg_paragraph_length = sum(len(word_tokenize(p)) for p in paragraphs) / len(paragraphs)
        
        if avg_paragraph_length > 100:
            suggestions.append({
                "category": "readability",
                "suggestion": "단락이 너무 깁니다. 더 작은 단락으로 나누세요.",
                "priority": 2
            })
        else:
            readability_score += 33
        
        # 텍스트 감성 분석
        blob = TextBlob(text)
        if blob.sentiment.polarity < 0:
            suggestions.append({
                "category": "readability",
                "suggestion": "텍스트의 톤이 부정적입니다. 더 긍정적인 톤으로 수정하세요.",
                "priority": 3
            })
        else:
            readability_score += 34
        
        return {
            "score": readability_score,
            "suggestions": suggestions
        }
    
    def analyze_engagement(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """참여도 분석을 수행합니다."""
        engagement_score = 0
        suggestions = []
        
        text = content["description"]
        
        # 질문 수 확인
        questions = len(re.findall(r'\?', text))
        if questions < 2:
            suggestions.append({
                "category": "engagement",
                "suggestion": "독자와의 상호작용을 위해 더 많은 질문을 추가하세요.",
                "priority": 2
            })
        else:
            engagement_score += 33
        
        # 콜투액션(CTA) 확인
        cta_patterns = r'click|subscribe|follow|share|comment|like|register|sign up|learn more'
        cta_count = len(re.findall(cta_patterns, text.lower()))
        if cta_count < 2:
            suggestions.append({
                "category": "engagement",
                "suggestion": "행동 유도(CTA)를 더 추가하세요.",
                "priority": 2
            })
        else:
            engagement_score += 33
        
        # 미디어 요소 확인
        media_patterns = r'!\[.*?\]|<img|<video|<iframe'
        media_count = len(re.findall(media_patterns, text))
        if media_count < 1:
            suggestions.append({
                "category": "engagement",
                "suggestion": "이미지나 비디오를 추가하여 콘텐츠를 더 풍부하게 만드세요.",
                "priority": 2
            })
        else:
            engagement_score += 34
        
        return {
            "score": engagement_score,
            "suggestions": suggestions
        }
    
    def analyze_technical(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """기술적 분석을 수행합니다."""
        technical_score = 0
        suggestions = []
        
        # HTML 태그 확인
        if content.get("content_type") in ["blog", "social"]:
            soup = BeautifulSoup(content["description"], 'html.parser')
            
            # 헤딩 태그 확인
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if not headings:
                suggestions.append({
                    "category": "technical",
                    "suggestion": "섹션을 구분하기 위해 헤딩 태그를 사용하세요.",
                    "priority": 2
                })
            else:
                technical_score += 25
            
            # 링크 텍스트 확인
            links = soup.find_all('a')
            generic_link_texts = ['click here', 'here', 'link', 'this link']
            has_generic_links = any(link.text.lower() in generic_link_texts for link in links)
            if has_generic_links:
                suggestions.append({
                    "category": "technical",
                    "suggestion": "일반적인 링크 텍스트 대신 설명적인 링크 텍스트를 사용하세요.",
                    "priority": 3
                })
            else:
                technical_score += 25
            
            # 이미지 alt 텍스트 확인
            images = soup.find_all('img')
            missing_alt = [img for img in images if not img.get('alt')]
            if missing_alt:
                suggestions.append({
                    "category": "technical",
                    "suggestion": "모든 이미지에 대체 텍스트를 추가하세요.",
                    "priority": 2
                })
            else:
                technical_score += 25
        else:
            technical_score += 75
        
        # 파일 크기 확인
        content_length = len(content["description"].encode('utf-8'))
        if content_length > 100000:  # 100KB
            suggestions.append({
                "category": "technical",
                "suggestion": "콘텐츠 크기가 너무 큽니다. 최적화가 필요합니다.",
                "priority": 2
            })
        else:
            technical_score += 25
        
        return {
            "score": technical_score,
            "suggestions": suggestions
        }
    
    def analyze_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """전체 콘텐츠 분석을 수행합니다."""
        seo_analysis = self.analyze_seo(content)
        readability_analysis = self.analyze_readability(content)
        engagement_analysis = self.analyze_engagement(content)
        technical_analysis = self.analyze_technical(content)
        
        all_suggestions = (
            seo_analysis["suggestions"] +
            readability_analysis["suggestions"] +
            engagement_analysis["suggestions"] +
            technical_analysis["suggestions"]
        )
        
        return {
            "seo_score": seo_analysis["score"],
            "readability_score": readability_analysis["score"],
            "engagement_score": engagement_analysis["score"],
            "technical_score": technical_analysis["score"],
            "suggestions": sorted(all_suggestions, key=lambda x: x["priority"])
        }
