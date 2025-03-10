from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models import db
from app.models.ai_tool import AITool, Category
from app.models.tool_combination import ToolCombination
from app.models.youtube_data import YoutubeData

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/combinations', methods=['GET'])
@login_required
def get_user_combinations():
    """Get all tool combinations for the current user"""
    combinations = ToolCombination.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'combinations': [combo.to_dict() for combo in combinations]
    }), 200

@dashboard_bp.route('/combinations', methods=['POST'])
@login_required
def create_combination():
    """Create a new tool combination for the current user"""
    data = request.get_json()
    
    # Check required fields
    if not data or not data.get('name') or not data.get('content_type') or not data.get('tool_ids'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create new combination
    new_combination = ToolCombination(
        name=data['name'],
        description=data.get('description', ''),
        content_type=data['content_type'],
        user_id=current_user.id
    )
    
    # Add tools to combination
    for tool_id in data['tool_ids']:
        tool = AITool.query.get(tool_id)
        if tool:
            new_combination.tools.append(tool)
    
    db.session.add(new_combination)
    db.session.commit()
    
    return jsonify(new_combination.to_dict()), 201

@dashboard_bp.route('/combinations/<int:combination_id>', methods=['GET'])
@login_required
def get_combination(combination_id):
    """Get a specific tool combination by ID"""
    combination = ToolCombination.query.get_or_404(combination_id)
    
    # Check if the combination belongs to the current user
    if combination.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    return jsonify(combination.to_dict()), 200

@dashboard_bp.route('/combinations/<int:combination_id>', methods=['PUT'])
@login_required
def update_combination(combination_id):
    """Update an existing tool combination"""
    combination = ToolCombination.query.get_or_404(combination_id)
    
    # Check if the combination belongs to the current user
    if combination.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    if data.get('name'):
        combination.name = data['name']
    
    if data.get('description'):
        combination.description = data['description']
    
    if data.get('content_type'):
        combination.content_type = data['content_type']
    
    # Update tools
    if data.get('tool_ids'):
        # Clear existing tools
        combination.tools = []
        
        # Add new tools
        for tool_id in data['tool_ids']:
            tool = AITool.query.get(tool_id)
            if tool:
                combination.tools.append(tool)
    
    db.session.commit()
    
    return jsonify(combination.to_dict()), 200

@dashboard_bp.route('/combinations/<int:combination_id>', methods=['DELETE'])
@login_required
def delete_combination(combination_id):
    """Delete a tool combination"""
    combination = ToolCombination.query.get_or_404(combination_id)
    
    # Check if the combination belongs to the current user
    if combination.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    db.session.delete(combination)
    db.session.commit()
    
    return jsonify({'message': 'Combination deleted successfully'}), 200

@dashboard_bp.route('/recommend', methods=['POST'])
@login_required
def recommend_tools():
    """Recommend AI tools based on content type"""
    data = request.get_json()
    
    # Check required fields
    if not data or not data.get('content_type'):
        return jsonify({'error': 'Content type is required'}), 400
    
    content_type = data['content_type']
    
    # Get categories related to the content type
    relevant_categories = []
    if content_type == 'shorts':
        relevant_categories = ['video editing', 'thumbnail', 'script writing', 'idea generation']
    elif content_type == 'long-form':
        relevant_categories = ['video editing', 'thumbnail', 'script writing', 'research', 'analytics']
    elif content_type == 'podcast':
        relevant_categories = ['audio editing', 'script writing', 'transcription', 'idea generation']
    else:
        relevant_categories = ['idea generation', 'content creation']
    
    # Get tools for each category
    recommended_tools = {}
    for category_name in relevant_categories:
        category = Category.query.filter_by(name=category_name).first()
        if category:
            recommended_tools[category_name] = [tool.to_dict() for tool in category.tools]
    
    return jsonify({
        'content_type': content_type,
        'recommendations': recommended_tools
    }), 200

@dashboard_bp.route('/trending', methods=['GET'])
@login_required
def get_trending_data():
    """Get trending YouTube data for the dashboard"""
    trending_keywords = YoutubeData.query.filter_by(is_trending=True).order_by(YoutubeData.popularity_score.desc()).limit(10).all()
    
    return jsonify({
        'trending_keywords': [keyword.to_dict() for keyword in trending_keywords]
    }), 200
