import logging
import sqlite3 as lite

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

conn = lite.connect('meta_data.db')
c = conn.cursor()
ce = c.execute

def create_table_project_list():
    ce("CREATE TABLE IF NOT EXISTS proj_list (proj_name VARCHAR(20), prod_code VARCHAR(20) start_date DATE end_date DATE)")

def create_table_project_crew_on_board():
    ce("CREATE TABLE IF NOT EXISTS pro_crew (proj_code VARCHAR(20), proj_unix UNIQUE)")

def create_tabe_project_pre_production():
    ce("CREATE TABLE IF NOT EXISTS pre_production (script VARCHAR(20), script_dateline VARCHAR(20), storyboard VARCHAR(20)"
       "storyboard_deadline VARCHAR(20), animatic2D VARCHAR(20), animatic2D_deadline VARCHAR(20), animatic3D VARCHAR(20),"
       "animatic3D_dealine VARCHAR(20))")

def create_table_project_production():
    ce("CREATE TABLE IF NOT EXISTS production_state (proj_code VARCHAR(20) time_long INT, unix_ppl REAL duty VARCHAR(20) "
       "period VARCHAR(20) shots INT, assets VARCHAR(20), asset_task VARCHAR(20))")

def create_table_assets_detail():
    ce("CREATE TABLE IF NOT EXISTS assets_task (proj_code VARCHAR(20) art VARCHAR(20) art_dateline VARCHAR(20) "
       "modeling VARCHAR(20), modeling_dateline VARCHAR(20) rigging VARCHAR(20), rigging_dateline VARCHAR(20)"
       "lookdev VARCHAR(20), lookdev_dateline TIMESTAMP)")

def create_table_shots_detail():
    ce("CREATE TABLE IF NOT EXISTS shots_task (proj_code VARCHAR(20), shot_code VARCHAR(20), anim VARCHAR(20)), "
       "anim_dateline VARCHAR(20), comp VARCHAR(20), comp_dateline VARCHAR(20), vfx VARCHAR(20), vfx_dateline VARCHAR(20)"
       "layout VARCHAR(20), layout_dateline VARCHAR(20), lighting VARCHAR(20), lighting_dateline(20), "
       "shot_dateline VARCHAR(20)")

def create_table_project_post_production():
    ce("CREATE TABLE IF NOT EXISTS pre_production (proj_code VARCHAR(20), shot_comping VARCHAR(20), "
       "shot_comp_deadline VARCHAR(20), master_comp VARCHAR(20), sound VARCHAR(20), sound_dateline VARCHAR(20), "
       "editing VARCHAR(20), deliverable_dateline VARCHAR(20))")

def create_table_project_config_software_path():
    ce("CREATE TABLE IF NOT EXISTS software_path (proj_code VARCHAR(20) maya_path VARCHAR(20), zbrush_path VARCHAR(20),"
       "houdini VARCHAR(20), photoshop VARCHAR(20), nukex VARCHAR(20), after_effects VARCHAR(20), premiere_pro VARCHAR(20)"
       "mari VARCHAR(20))")

def create_table_project_folder_path():
    ce("CREATE TABLE IF NOT EXISTS proj_path (prod_master VARCHAR(20), )")