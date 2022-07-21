import re


class SuperHero:
    """A Class to hold super hero information necessary to be displayed

    Attributes
    ----------
    full_name : str
        the full name of the super hero
    occupation : list
        the occupation list of the super hero
    alter_egos : list
        the alter ego list of the super hero
    aliases : list
        the alias list of the super hero
    place_of_birth : str
        the place of birth of the super hero
    picture : str
        url that point to a picture of the super hero

    Methods
    -------
    from_api(hero)
        Initialize super hero from API object
    """
    def __init__(
        self,
        full_name,
        occupation,
        alter_egos,
        aliases,
        place_of_birth,
        picture
    ):
        """
        Parameters
        ----------
        full_name : str
            the full name of the super hero
        occupation : list
            the occupation list of the super hero
        alter_egos : list
            the alter ego list of the super hero
        aliases : list
            the alias list of the super hero
        place_of_birth : str
            the place of birth of the super hero
        picture : str
            url that point to a picture of the super hero
        """
        self.full_name = full_name
        self.alter_egos = alter_egos
        self.aliases = aliases
        self.place_of_birth = place_of_birth
        self.picture = picture
        self.occupation = occupation

    @classmethod
    def from_api(cls, hero):
        """Initialize super hero from API object

        Parameters
        ----------
        hero : dict
            Dictionary with raw information provided by the superhero-api

        Returns
        -------
        SuperHero
            initialized object
        """
        biography = hero['biography']
        full_name = biography['fullName']

        return cls(
            full_name if full_name != '' else hero['name'],
            re.split('; |, ', hero['work']['occupation']),
            biography['alterEgos'],
            biography['aliases'],
            biography['placeOfBirth'],
            hero['images']['md']
        )
