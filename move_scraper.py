#!/usr/bin/python3
"""
Scrapes Serebii.net for Pokémon statistics.
"""
import argparse
import bs4
import json
import logging
import re
import requests

OUTPUT_FILE = 'moves_enriched.json'

def scrape_move():
    moves = []
    with open('moves.json', 'r') as file1:
        data = json.load(file1)
    total = len(data.keys())
    for i,move in enumerate(data.keys()):
        print(move, f"{100*(i/total)}%")
        moves.append(extract_statistics(move))

    save_to_json(moves)

def extract_statistics(move_id) -> object:
    url = 'https://serebii.net/attackdex-sv/{}.shtml'.format(str(move_id).zfill(3))
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')

    try:
        all_divs = soup.find_all('table', attrs={'class': 'dextable'})

        table1 = all_divs[0].findAll('td')
        table2 = all_divs[1].findAll('td')

        extracted_move = {
            "name": table1[3].text.lower().replace(' ',''),
            "effect": table1[16].text,
            "effect_probability": table1[17].text,
            "base_crit": table1[21].text,
            "priority": table1[22].text,
            "pokemon_hit": table1[23].text,
            "physical_contact": table2[5].text,
            "sound": table2[6].text,
            "punch": table2[7].text,
            "biting": table2[8].text,
            "slicing": table2[15].text,
            "bullet_type": table2[16].text,
            "wind": table2[17].text,
            "powder": table2[18].text,
            "gravity_affected": table2[25].text,
            "defrosts": table2[26].text,
            "reflectable": table2[27].text,
            "protect_blocked": table2[28].text,

        }
    except Exception:
        return {
            "name": move_id,
            'problem': 'revisar'
        }

    return extracted_move


def save_to_json(data: list):
    """
    Save data to file.
    """
    with open(OUTPUT_FILE, mode='w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=4)


if __name__ == '__main__':
    try:
        scrape_move()
    except Exception as ex:
        logging.error(ex)
        raise
