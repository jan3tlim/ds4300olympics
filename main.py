"""
Olympics Analysis Using MongoDB

Contributions:
Amelia wrote the code to implement the API she wrote on  WomensRepAPI
Katie:
Janet:
"""

from womens_rep_api import WomensRepAPI
am_api = WomensRepAPI()


year_data = am_api.female_athletes_year()
print(year_data[:10])

season_data = am_api.female_athletes_seasons()
print(season_data)

