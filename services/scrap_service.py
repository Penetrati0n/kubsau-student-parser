import requests

class ScrapService():
    MAIN_PAGE_URL = 'https://kubsau.ru/education/portfolio/'
    FACULTY_GROUPS_URL = 'https://kubsau.ru/local/components/portfolio/faculty-list/GroupList.php'
    GROUP_URL = 'https://kubsau.ru/education/portfolio/groups/{}/'

    @staticmethod
    def scrap_main_page() -> str:
        try:
            return requests.get(ScrapService.MAIN_PAGE_URL, verify=False).text
        except:
            return ''

    @staticmethod
    def scrap_faculty_groups(uuid: str) -> list:
        try:
            payload = {
                'id': (None, uuid)
            }
            response = requests.post(ScrapService.FACULTY_GROUPS_URL, files=payload, verify=False)
            return [{'name': el['GROUP_NAME'], 'uuid': el['GROUP_ID']} for el in response.json()]
        except:
            return []

    @staticmethod
    def scrap_group(uuid: str) -> str:
        try:
            return requests.get(ScrapService.GROUP_URL.format(uuid), verify=False).text
        except:
            return ''
