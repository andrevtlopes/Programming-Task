from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle


class PDF:
    """A Class to print out superhero information to PDF

    Attributes
    ----------
    data : str
        the normalized data to be used in printing out the PDF
    file_name : str
        the name of the file
    title : str
        the title of the PDF

    Methods
    -------
    create_pdf()
        Print out information to the PDF file
    """
    def __init__(self, file_name, title, super_heroes):
        """
        Parameters
        ----------
        file_name : list
            the name of the file
        title : list
            the title of the PDF
        super_heroes : list
            the super heroes list
        """
        self.data = {}
        self.file_name = file_name
        self.title = title

        self._prepare_data(super_heroes)
        self._bottom = 11 * inch
        self._page_items = 0
        self._font = 'Helvetica'
        self._right_info = 2*inch + inch/2
        self._right_image = inch

    def _prepare_data(self, super_heroes):
        """Prepare data from the api to be used in the PDF output

        Parameters
        ----------
        super_heroes : list
            the super heroes list
        """
        for super_hero in super_heroes:
            group = super_hero.occupation[0]
            if group not in self.data:
                self.data.update({group: [super_hero]})
            else:
                self.data[group].append(super_hero)

    def _draw_paragraph(
        self,
        msg,
        x,
        y,
        max_width=5*inch,
        max_height=11*inch
    ):
        """Draw a paragraph on PDF canvas

        Parameters
        ----------
        msg : str
            message to be written
        x : int
            position in the x axis from the left of the page
        y : int
            position in the y axis from the bottom of the page
        max_width : int, optional
            max width of the paragraph
        max_height : int, optional
            max height of the paragraph
        """
        message_style = ParagraphStyle('Normal')
        message = Paragraph(msg, style=message_style)
        _, h = message.wrap(max_width, max_height)
        y -= h
        message.drawOn(self.canvas, x, y)
        self._bottom = self._bottom - h - 12

    def _draw_info_paragraph(self, title, msg):
        """Draw hero paragraph information on pdf canvas

        Parameters
        ----------
        title : str
            the title of the super hero information
        msg : str
            message to be written
        """
        message = msg.replace('\n', '<br />')
        message = '<b>{}:</b> {}'.format(title, message)
        self._draw_paragraph(
            message,
            self._right_info,
            self._bottom
        )

    def _draw_heading(self, msg, font_size):
        """Draw heading on canvas

        Parameters
        ----------
        msg : str
            message to be written
        font_size : str
            font size of the heading
        """
        self.canvas.setFont(self._font, font_size)
        self.canvas.drawString(inch, self._bottom, msg)
        self._bottom -= inch/2

    def _print_list(self, s):
        """Print list or string for the pdf document format

        Parameters
        ----------
        s : list, str
            list to be printed on PDF

        Returns
        -------
        str
            list in string format or the initial string
        """
        if(isinstance(s, str)):
            return s
        else:
            return ', '.join(s)

    def _shared_occupation(self, key):
        """Returns if the occupation is shared between more than 2 heroes

        Parameters
        ----------
        key : str
            key from the data dictionary representing the occupation

        Returns
        -------
        bool
            If the occupation is shared between more than 2 heroes
        """
        return len(self.data[key]) > 1 and key != '-'

    def create_pdf(self):
        """Create the super heroes PDF from information provided"""
        self.canvas = Canvas(self.file_name + '.pdf')
        self._draw_heading(self.title, 18)

        for key in self.data:
            self._right_info = 2*inch + inch/2
            self._right_image = inch

            if (self._shared_occupation(key)):
                self._right_info += inch/2
                self._right_image += inch/2
                self._draw_heading(key, 16)
                self._page_items += 1

            heroes = self.data[key]
            for hero in heroes:
                self._page_items += 1

                image_bottom = self._bottom - 640/5
                self.canvas.setFont(self._font, 11)
                self.canvas.drawImage(
                    hero.picture,
                    self._right_image,
                    image_bottom + 20,
                    width=480/5,
                    height=640/5
                )

                self._draw_info_paragraph(
                    'Full name',
                    hero.full_name,
                )
                self._draw_info_paragraph(
                    'Alter Egos',
                    self._print_list(hero.alter_egos),
                )
                self._draw_info_paragraph(
                    'Aliases',
                    self._print_list(hero.aliases),
                )
                self._draw_info_paragraph(
                    'Place of Birth',
                    hero.place_of_birth,
                )

                self._bottom = image_bottom

                if (self._shared_occupation(key) and hero == heroes[-1]):
                    self.canvas.drawString(
                        inch, self._bottom, '_'*80)
                    self._bottom -= inch/4

                self._bottom -= inch/4

                if self._page_items == 5:
                    # Reset bottom and create new page on PDF
                    self.canvas.showPage()
                    self._page_items = 0
                    self._bottom = 11 * inch

        self.canvas.save()
        print("Created Superheroes PDF '{}.pdf'".format(self.file_name))
