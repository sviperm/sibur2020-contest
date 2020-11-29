import re
from pathlib import Path

import pandas as pd
import pycountry

countries = [country.name.lower() for country in pycountry.countries]


def preprocess(company: str) -> str:
    company = company.lower()
    company = re.sub(r'[^\w\s]', '', company)

    legal_entities = ["ltd", "co", "inc", "bv", "scrl", "gmbh", "pvt", "ооо",
                      "industries", "industrial"]
    company = re.sub("|".join(legal_entities), '', company)

    company = re.sub("|".join(countries), '', company)

    company = company.strip()
    company = re.sub(r'\s{2,}', ' ', company)

    return company


if __name__ == "__main__":
    ROOT = Path(__file__).parents[1] / "data"
    train = pd.read_csv(ROOT.joinpath("train.csv"), index_col="pair_id")
    train['name_1'] = train['name_1'].apply(preprocess)
    train['name_2'] = train['name_2'].apply(preprocess)
    # train.to_csv(ROOT / 'train_cleared.csv')

    test = pd.read_csv(ROOT.joinpath("test.csv"), index_col="pair_id")
    test['name_1'] = test['name_1'].apply(preprocess)
    test['name_2'] = test['name_2'].apply(preprocess)
    # test.to_csv(ROOT / 'test_cleared.csv')
