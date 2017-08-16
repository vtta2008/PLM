import os, sys, logging

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

logger.info('create new variables')

key = 'PIPELINE_TOOL'
toolName = 'PipelineTool'
scrInstall = os.getenv('PROGRAMDATA')

toolPth = os.path.join(scrInstall, toolName)

if not os.path.exists(toolPth):
    os.mkdir(toolPth)

os.environ[key] = toolPth

#main UI
from ui import DesktopUI as desk
desk.initialize()