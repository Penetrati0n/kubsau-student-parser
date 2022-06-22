from bs4 import BeautifulSoup

class ParseService():

    @staticmethod
    def parse_students(group_page_raw: str) -> list:
        parsed_html = BeautifulSoup(group_page_raw, features='html.parser')
        # old site
        # students_elements = parsed_html.select('.content a')
        # new site
        students_elements = parsed_html.select('.page-content a')
        students = [se.text for se in students_elements]
        return students

    @staticmethod
    def parse_faculties(page_raw) -> dict:
        parsed_html = BeautifulSoup(page_raw, features='html.parser')
        faculties_elements = [o for o in parsed_html.select('.portfolio-faculty > option') if o.text != '']
        faculties = {}
        for fe in faculties_elements:
            faculties[fe.attrs['value']] = fe.text
        return faculties
