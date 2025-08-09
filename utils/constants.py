import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 目录配置
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

RSS_HOST = os.getenv('RSS_HOST', '127.0.0.1')
RSS_PORT = os.getenv('RSS_PORT', '8000')

# RSS基础URL，如果未设置，则使用请求的URL
RSS_BASE_URL = os.environ.get('RSS_BASE_URL', None)

# RSS媒体文件的基础URL，用于生成媒体链接，如果未设置，则使用请求的URL
RSS_MEDIA_BASE_URL = os.getenv('RSS_MEDIA_BASE_URL', '')

RSS_ENABLED = os.getenv('RSS_ENABLED', 'false')

RULES_PER_PAGE = int(os.getenv('RULES_PER_PAGE', 20))

PUSH_CHANNEL_PER_PAGE = int(os.getenv('PUSH_CHANNEL_PER_PAGE', 10))

DEFAULT_TIMEZONE = os.getenv('DEFAULT_TIMEZONE', 'Asia/Shanghai')
PROJECT_NAME = os.getenv('PROJECT_NAME', 'TG Forwarder RSS')
# RSS相关路径配置
RSS_MEDIA_PATH = os.getenv('RSS_MEDIA_PATH', './rss/media')

# 转换为绝对路径
RSS_MEDIA_DIR = os.path.abspath(os.path.join(BASE_DIR, RSS_MEDIA_PATH) 
                              if not os.path.isabs(RSS_MEDIA_PATH) 
                              else RSS_MEDIA_PATH)

# RSS数据路径
RSS_DATA_PATH = os.getenv('RSS_DATA_PATH', './rss/data')
RSS_DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, RSS_DATA_PATH)
                            if not os.path.isabs(RSS_DATA_PATH)
                            else RSS_DATA_PATH)

# 默认AI模型
DEFAULT_AI_MODEL = os.getenv('DEFAULT_AI_MODEL', 'gpt-4o')
# Default AI summary prompt (English UI, behavior unchanged)
DEFAULT_SUMMARY_PROMPT = os.getenv(
    'DEFAULT_SUMMARY_PROMPT',
    'Please summarize the messages from the channel/group in the past 24 hours.'
)
# Default AI prompt (describe behavior in English, preserves original behavior intent)
DEFAULT_AI_PROMPT = os.getenv(
    'DEFAULT_AI_PROMPT',
    'Please respect the original meaning and keep the original formatting unchanged. Rewrite the following content in Simplified Chinese:'
)

# 分页配置
MODELS_PER_PAGE = int(os.getenv('AI_MODELS_PER_PAGE', 10))
KEYWORDS_PER_PAGE = int(os.getenv('KEYWORDS_PER_PAGE', 50))

# 按钮布局配置
SUMMARY_TIME_ROWS = int(os.getenv('SUMMARY_TIME_ROWS', 10))
SUMMARY_TIME_COLS = int(os.getenv('SUMMARY_TIME_COLS', 6))

DELAY_TIME_ROWS = int(os.getenv('DELAY_TIME_ROWS', 10))
DELAY_TIME_COLS = int(os.getenv('DELAY_TIME_COLS', 6))

MEDIA_SIZE_ROWS = int(os.getenv('MEDIA_SIZE_ROWS', 10))
MEDIA_SIZE_COLS = int(os.getenv('MEDIA_SIZE_COLS', 6))

MEDIA_EXTENSIONS_ROWS = int(os.getenv('MEDIA_EXTENSIONS_ROWS', 6))
MEDIA_EXTENSIONS_COLS = int(os.getenv('MEDIA_EXTENSIONS_COLS', 6))

LOG_MAX_SIZE_MB = 10
LOG_BACKUP_COUNT = 3

# 默认消息删除时间 (秒)
BOT_MESSAGE_DELETE_TIMEOUT = int(os.getenv("BOT_MESSAGE_DELETE_TIMEOUT", 300))

# 自动删除用户发送的指令消息
USER_MESSAGE_DELETE_ENABLE = os.getenv("USER_MESSAGE_DELETE_ENABLE", "false")

# 是否启用UFB
UFB_ENABLED = os.getenv("UFB_ENABLED", "false")

# Menu titles / descriptive texts (English)
AI_SETTINGS_TEXT = """
Current AI prompt:

`{ai_prompt}`

Current summary prompt:

`{summary_prompt}`
"""

# Media settings text
MEDIA_SETTINGS_TEXT = """
Media settings:
"""
PUSH_SETTINGS_TEXT = """
Push settings:
Please refer to the Apprise Wiki for configuration formats: https://github.com/caronc/apprise/wiki
For example: `ntfy://ntfy.sh/your_topic_name`
"""


# 为每个规则生成特定的路径
def get_rule_media_dir(rule_id):
    """获取指定规则的媒体目录"""
    rule_path = os.path.join(RSS_MEDIA_DIR, str(rule_id))
    # 确保目录存在
    os.makedirs(rule_path, exist_ok=True)
    return rule_path

def get_rule_data_dir(rule_id):
    """获取指定规则的数据目录"""
    rule_path = os.path.join(RSS_DATA_DIR, str(rule_id))
    # 确保目录存在
    os.makedirs(rule_path, exist_ok=True)
    return rule_path