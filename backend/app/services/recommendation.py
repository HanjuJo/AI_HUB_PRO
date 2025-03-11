"""
AI 도구 추천 서비스
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.ai_tool import AITool, Category
from app.models.user import User


class RecommendationService:
    """
    AI 도구 추천 서비스 클래스
    """
    
    @staticmethod
    def recommend_by_category(db: Session, category_name: str, limit: int = 5) -> List[AITool]:
        """
        카테고리별 AI 도구 추천
        """
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            return []
        
        # 해당 카테고리에 속한 도구 중 상위 N개 반환
        tools = db.query(AITool).join(
            AITool.categories
        ).filter(
            Category.id == category.id
        ).limit(limit).all()
        
        return tools
    
    @staticmethod
    def recommend_by_use_case(db: Session, use_case: str, limit: int = 5) -> List[AITool]:
        """
        사용 사례별 AI 도구 추천
        """
        # 사용 사례와 관련된 키워드를 포함하는 도구 검색
        tools = db.query(AITool).filter(
            AITool.description.ilike(f"%{use_case}%")
        ).limit(limit).all()
        
        return tools
    
    @staticmethod
    def recommend_personalized(db: Session, user: User, limit: int = 5) -> List[AITool]:
        """
        사용자 맞춤형 AI 도구 추천
        """
        # 사용자가 이전에 사용한 도구 조합에서 카테고리 추출
        user_categories = set()
        for combination in user.tool_combinations:
            for tool in combination.tools:
                for category in tool.categories:
                    user_categories.add(category.id)
        
        # 사용자가 선호하는 카테고리에 속한 도구 추천
        if user_categories:
            tools = db.query(AITool).join(
                AITool.categories
            ).filter(
                Category.id.in_(list(user_categories))
            ).limit(limit).all()
            return tools
        
        # 사용자 정보가 없는 경우 인기 도구 추천
        return RecommendationService.recommend_popular(db, limit)
    
    @staticmethod
    def recommend_popular(db: Session, limit: int = 5) -> List[AITool]:
        """
        인기 AI 도구 추천
        """
        # 현재는 단순히 최신 도구를 반환
        # 향후 사용 통계 데이터를 기반으로 인기 도구 추천 로직 구현 가능
        tools = db.query(AITool).order_by(AITool.created_at.desc()).limit(limit).all()
        return tools
    
    @staticmethod
    def recommend_similar(db: Session, tool_id: int, limit: int = 3) -> List[AITool]:
        """
        유사한 AI 도구 추천
        """
        tool = db.query(AITool).filter(AITool.id == tool_id).first()
        if not tool:
            return []
        
        # 같은 카테고리에 속한 다른 도구 추천
        category_ids = [category.id for category in tool.categories]
        if not category_ids:
            return []
        
        similar_tools = db.query(AITool).join(
            AITool.categories
        ).filter(
            Category.id.in_(category_ids),
            AITool.id != tool_id
        ).limit(limit).all()
        
        return similar_tools
    
    @staticmethod
    def recommend_complementary(db: Session, tool_id: int, limit: int = 3) -> List[AITool]:
        """
        보완적인 AI 도구 추천 (함께 사용하면 좋은 도구)
        """
        tool = db.query(AITool).filter(AITool.id == tool_id).first()
        if not tool:
            return []
        
        # 같은 도구 조합에 포함된 다른 도구 추천
        complementary_tools = []
        for combination in tool.combinations:
            for combo_tool in combination.tools:
                if combo_tool.id != tool_id and combo_tool not in complementary_tools:
                    complementary_tools.append(combo_tool)
                    if len(complementary_tools) >= limit:
                        return complementary_tools
        
        # 충분한 도구를 찾지 못한 경우, 다른 카테고리의 도구 추천
        if len(complementary_tools) < limit:
            tool_category_ids = [category.id for category in tool.categories]
            remaining_limit = limit - len(complementary_tools)
            
            other_category_tools = db.query(AITool).join(
                AITool.categories
            ).filter(
                ~Category.id.in_(tool_category_ids),
                AITool.id != tool_id,
                ~AITool.id.in_([t.id for t in complementary_tools])
            ).limit(remaining_limit).all()
            
            complementary_tools.extend(other_category_tools)
        
        return complementary_tools
