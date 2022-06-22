import os, dotenv
dotenv.load_dotenv()

from services.group_service import GroupService
from services.scrap_service import ScrapService
from services.parse_service import ParseService
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=6)
def scheduled_job():
    group_service = GroupService(dsn=os.getenv('DefaulConnection'))
    main_page_raw = ScrapService.scrap_main_page()
    faculties = ParseService.parse_faculties(main_page_raw)
    groups = []
    for f in faculties:
        groups += ScrapService.scrap_faculty_groups(f)
    group_service.add_groups([(g['name'].upper(), g['uuid']) for g in groups])
    print('Successfull update groups in database!')

sched.start()
