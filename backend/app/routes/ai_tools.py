from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.models import db
from app.models.ai_tool import AITool, Category

ai_tools_bp = Blueprint('ai_tools', __name__, url_prefix='/api/tools')

@ai_tools_bp.route('/', methods=['GET'])
def get_all_tools():
    """Get all AI tools with optional filtering by category"""
    category = request.args.get('category')
    
    if category:
        category_obj = Category.query.filter_by(name=category).first()
        if not category_obj:
            return jsonify({'error': 'Category not found'}), 404
        tools = category_obj.tools
    else:
        tools = AITool.query.all()
    
    return jsonify({
        'tools': [tool.to_dict() for tool in tools]
    }), 200

@ai_tools_bp.route('/<int:tool_id>', methods=['GET'])
def get_tool(tool_id):
    """Get a specific AI tool by ID"""
    tool = AITool.query.get_or_404(tool_id)
    
    return jsonify(tool.to_dict()), 200

@ai_tools_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    }), 200

@ai_tools_bp.route('/search', methods=['GET'])
def search_tools():
    """Search for AI tools by name or description"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    tools = AITool.query.filter(
        (AITool.name.ilike(f'%{query}%')) | 
        (AITool.description.ilike(f'%{query}%'))
    ).all()
    
    return jsonify({
        'tools': [tool.to_dict() for tool in tools]
    }), 200

# Admin routes for managing tools
@ai_tools_bp.route('/', methods=['POST'])
@login_required
def create_tool():
    """Create a new AI tool (admin only)"""
    # TODO: Add admin check
    
    data = request.get_json()
    
    # Check required fields
    if not data or not data.get('name') or not data.get('url'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create new tool
    new_tool = AITool(
        name=data['name'],
        description=data.get('description', ''),
        url=data['url'],
        image_url=data.get('image_url'),
        pricing_type=data.get('pricing_type', 'free'),
        pricing_details=data.get('pricing_details'),
        features=data.get('features')
    )
    
    # Add categories
    if data.get('categories'):
        for category_name in data['categories']:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
            new_tool.categories.append(category)
    
    db.session.add(new_tool)
    db.session.commit()
    
    return jsonify(new_tool.to_dict()), 201

@ai_tools_bp.route('/<int:tool_id>', methods=['PUT'])
@login_required
def update_tool(tool_id):
    """Update an existing AI tool (admin only)"""
    # TODO: Add admin check
    
    tool = AITool.query.get_or_404(tool_id)
    data = request.get_json()
    
    if data.get('name'):
        tool.name = data['name']
    
    if data.get('description'):
        tool.description = data['description']
    
    if data.get('url'):
        tool.url = data['url']
    
    if data.get('image_url'):
        tool.image_url = data['image_url']
    
    if data.get('pricing_type'):
        tool.pricing_type = data['pricing_type']
    
    if data.get('pricing_details'):
        tool.pricing_details = data['pricing_details']
    
    if data.get('features'):
        tool.features = data['features']
    
    # Update categories
    if data.get('categories'):
        # Clear existing categories
        tool.categories = []
        
        # Add new categories
        for category_name in data['categories']:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
            tool.categories.append(category)
    
    db.session.commit()
    
    return jsonify(tool.to_dict()), 200

@ai_tools_bp.route('/<int:tool_id>', methods=['DELETE'])
@login_required
def delete_tool(tool_id):
    """Delete an AI tool (admin only)"""
    # TODO: Add admin check
    
    tool = AITool.query.get_or_404(tool_id)
    
    db.session.delete(tool)
    db.session.commit()
    
    return jsonify({'message': 'Tool deleted successfully'}), 200
