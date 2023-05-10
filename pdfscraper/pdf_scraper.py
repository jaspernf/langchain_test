import re
from pyxpdf import Document
from pyxpdf.xpdf import TextOutput, TextControl, page_iterator

class PDFNode():
    def __init__(self, lines, row, page):
        self._lines = lines
        self.row = row
        self.page = page

    def add_step(self, step=0):
        self.row += step
        return self

    def split(self, expression=r"\s{2,}"):
        return [x for x in re.split(expression, self.value()) if self.value()]

    def value(self):
        for line in self._lines:
            if line['row'] == self.row:
                return line['data']
        return ''

class PDFTextMiner():

    def __init__(self, lines=None):
        """
        :param mode: physical, table
        """
        self.pdf_name = ''
        self.row = []
        if lines is None:
            self.lines = []
        else:
            self.lines = lines
            self.pdf_name = 'This is a self extracted line'
        self.text = None
        self.mode = ''

    def file_source(self):
        return self.pdf_name

    def get(self, pdf_loc, mode='physical', page='all'):
        """
        :param pdf_loc:location of the pdf file to scrape
        :param mode: string 'physical' or 'table' , this is for the layout of the output text
        :param page: string default 'all' all string on the page, 'start', 'last', '1-2' range,
        '1' single page
        :return:
        """
        self.mode = mode
        self.pdf_name = pdf_loc
        self._generate_base_values(page)

    def print_lines(self):
        for line in self.lines:
            print(line['row'], line['data'])

    def split_lines(self, start_row, end_row):
        """
        split PDFTextMiner self.lines
        :param start_row: integer, row_index
        :param end_row:  integer, row_index
        :return: return a lines array
        """
        new_lines = []
        started = False
        for line in self.lines:
            if line['row'] == start_row:
                started = True
            if started is True:
                new_lines.append(line)
            if line['row'] == end_row:
                break
        return new_lines

    def _generate_base_values(self, extract_page):
        def _append_lines(count):
            control = TextControl(mode=self.mode)
            data = page.text(control=control)
            for line in data.split('\n'):
                if len(line.strip()) > 1:
                    self.lines.append({
                        'row': count,
                        'data': line.split('\r')[0].strip(),
                        'page': page_count
                    })
                    count += 1
            return count

        text = ''
        doc = Document(self.pdf_name)
        count = 0
        last_page = 0
        for page_count, page in enumerate(doc):
            last_page = page_count

        page_number = None
        page_numbers = []
        if extract_page.isdigit() is True:
            if int(extract_page) > last_page:
                raise ValueError('No page found!')
            else:
                page_number = int(extract_page)
        if '-' in extract_page:
            page_numbers = extract_page.split('-')
            if page_numbers[0].isdigit() is True and page_numbers[1].isdigit() is True:
                if int(page_numbers[1]) > last_page:
                    raise ValueError('No page found!')
                else:
                    started = False
                    for page_count, page in enumerate(doc):
                        if page_count == int(page_numbers[0]):
                            started = True
                        if started is True:
                            count = _append_lines(count)
                        if page_count == int(page_numbers[1]):
                            break
        else:
            for page_count, page in enumerate(doc):
                if extract_page == 'last':
                    if page_count == last_page:
                        count = _append_lines(count)
                elif extract_page == 'all':
                    count = _append_lines(count)
                elif page_number is not None:
                    if page_count == page_number:
                        count = _append_lines(count)
                        break
                elif extract_page == 'start':
                    count = _append_lines(count)
                    break


    def _extract_lines(self, text, row, page):
        for line in text.split('\n'):
            if len(line.strip()) > 1:
                self.lines.append({
                    'row': row,
                    'data': line.split('\r')[0].strip(),
                    'page': page
                })

    def _find_text(self, keyword, **kwargs):
        """
        Search lines for keyword details regardless of case and spaces
        :param lines: list of strings
        :param keyword: keyword to search
        :param kwargs: all=check if get all lines found on a list,
                       check_first= check this page first
                       limit_to_page= limit search to (check_first) input
                       exact_text = search for exact string
                       no_space = Boolean, if false then it will seek text with space, default True
        :return: a string or a list of string
        """

        all = False if kwargs.get('all') is None else kwargs.get('all')
        limit_to_page = None if kwargs.get('limit_to_page') is None else kwargs.get('limit_to_page')
        exact_text = False if kwargs.get('limit_to_page') is None else kwargs.get('limit_to_page')
        no_space = True if kwargs.get('no_space') is None else kwargs.get('no_space')
        line_list = []
        cell = None
        for line in self.lines:
            if no_space is True:
                if exact_text is False:
                    if limit_to_page is None:
                        condition = keyword.lower().replace(' ', '') in line['data'].replace(' ', '').lower()
                    else:
                        condition = keyword.lower().replace(' ', '') in line['data'].replace(' ', '').lower() and limit_to_page == line['page']
                else:
                    if limit_to_page is None:
                        condition = keyword.lower().replace(' ', '') == line['data'].replace(' ', '').lower()
                    else:
                        condition = keyword.lower().replace(' ', '') == line['data'].replace(' ', '').lower() and limit_to_page == line['page']

            if no_space is False:
                if exact_text is False:
                    if limit_to_page is None:
                        condition = keyword.lower() in line['data'].lower()
                    else:
                        condition = keyword.lower() in line['data'].lower() and limit_to_page == line['page']
                else:
                    if limit_to_page is None:
                        condition = keyword.lower() == line['data'].lower()
                    else:
                        condition = keyword.lower() == line['data'].lower() and limit_to_page == line['page']


            if condition is True:
                if all is False:
                    try:
                        cell = PDFNode(self.lines, line['row'], line['page'])
                        return cell
                    except:
                        return ''
                else:
                    if line != '':
                        cell = PDFNode(self.lines, line['row'], line['page'])
                        line_list.append(cell)
        if all is False:
            return None
        else:
            return line_list

    def check_if_readable(self):
        for line in self.lines:
            if '' in line['data']:
                return False
        return True

    def find_node(self, to_search='', **kwargs):
        """
        Find line
        :param to_search: keyword to search
        :param kwargs: limit_to_page= limit search to (check_first) input
                       exact_text = search for exact string
                       no_space = Boolean, default True, search text with spaces or w/o space
        :return: PDFNode object
        """
        cell = self._find_text(to_search, all=False, **kwargs)
        if cell is not None:
            return cell

    def find_nodes(self, to_search='', **kwargs):
        """Find lines
        :param to_search: keyword to search
        :param kwargs: limit_to_page= limit search to (check_first) input
                       exact_text = search for exact string
                       no_space = Boolean, default True, search text with spaces or w/o space
        :return: list of PDFNode Object
        """
        cell = self._find_text(to_search, all=True, **kwargs)
        if cell is not None:
            return cell

