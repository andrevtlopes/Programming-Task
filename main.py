#!/usr/bin/env python3
"""
Programming task
Consume an API and transform the relevant data into
PDF output
"""

__author__ = "André Lopes"
__version__ = "1.0"
__license__ = "MIT"

from requests.exceptions import HTTPError
from superhero_client import SuperHeroClient
from superhero import SuperHero
from pdf import PDF


def main():
    """ Main entry point of the app """
    client = SuperHeroClient()
    super_heroes = []
    hero_id = 0
    while (len(super_heroes) < 10):
        hero_id += 1
        try:
            # get biography to check publisher
            biography = client.get_biography(hero_id)

            # check biography response
            if (not biography):
                continue

            if (biography['publisher'] == 'DC Comics'):
                # get all information once publisher is right
                hero = client.get_super_hero(hero_id)

                # check hero response
                if (not hero):
                    continue

                super_hero = SuperHero.from_api(hero)
                super_heroes.append(super_hero)

        except HTTPError as err:
            print(err)

    PDF(
        'super_heroes',
        'The Super Heroes API - DC Comics',
        super_heroes
    ).create_pdf()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
