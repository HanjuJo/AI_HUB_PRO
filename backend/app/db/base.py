# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.ai_tool import AITool, Category  # noqa
from app.models.tool_combination import ToolCombination  # noqa
from app.models.youtube_data import YoutubeData, YoutubeChannel, RecommendedChannel  # noqa
