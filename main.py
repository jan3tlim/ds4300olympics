"""
Olympics Analysis Using MongoDB

Contributions:
Amelia wrote the code to implement the API she wrote on  WomensRepAPI
Katie:
Janet:
"""

from womens_rep_api import WomensRepAPI
am_api = WomensRepAPI()

def main():
    year_data = am_api.female_athletes_year()
    print(year_data[:10])

    plot_female_athletes_year = am_api.plot_female_athletes_year()

    plot_female_athletes_seasons = am_api.plot_female_athletes_seasons()

    season_data = am_api.female_athletes_seasons()
    print(season_data)

if __name__ == "__main__":
    main()

