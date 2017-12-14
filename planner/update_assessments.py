
def cusp(course_code):
    """
    Takes a course code and returns a list containing dictionary objects which represent courses.
    All ye who enter, beware. There are list comprehensions abroad.
    """
    return [{'assessment_number': x[0], 'name': x[1], 'is_group': x[2], 'weight': x[3], 'due_string': x[4]} for x in [[x.text.strip() for x in x.find_all('td')][:-1] for x in BeautifulSoup(get_page('https://cusp.sydney.edu.au/students/view-unit-page/alpha/' + course_code), 'html.parser').find(string="Assessment Methods:").parent.next_element.next_element.next_element.next_element.next_element.find_all('tr')][1:]]
