# %%
import re
from pathlib import Path

import pandas as pd
import pycountry

countries = [country.name.lower() for country in pycountry.countries]
countries += ["ceska republika", "polska", "brasil", "international", "usa",
              "vietnam", "polynesie", "korea", "shanghai"]


def preprocess(company: str) -> str:
    company = company.lower()

    legal_entities = [r"ltd\.", r"co\.rporation", r"co\.", r"inc\.", r"b\.v\.",
                      r"s\.c\.r\.l\.", r"gmbh", r"pvt\.", r"s\.a\.",
                      r"de c\.v\.", r"c\.v\.", r"exp\.", r"llc", r"corp."
                      r"ооо", r"оао"]
    company_regexp = rf"({'|'.join(legal_entities)})[\W]*"
    company = re.sub(company_regexp, '', company)

    company = re.sub(r'[^\w\s]', ' ', company)

    popular_words = ["энтерпрайс",
                     "industries", "industrial", "industria",
                     "international", "global", "logistics", "private",
                     "corporation", "management", "consolidated", "trading"]

    popular_regexp = rf"({'|'.join(popular_words)})[\W]*"
    company = re.sub(popular_regexp, '', company)

    countries_regexp = rf"({'|'.join(countries)})[\W]*"
    company = re.sub(countries_regexp, '', company)

    company = company.strip()
    company = re.sub(r'\s{2,}', ' ', company)

    return company


if __name__ == "__main__":
    ROOT = Path(__file__).parents[1] / "data"
    train = pd.read_csv(ROOT.joinpath("train.csv"), index_col="pair_id")
    train['name_1'] = train['name_1'].apply(preprocess)
    train['name_2'] = train['name_2'].apply(preprocess)
    train.to_csv(ROOT / 'train_cleared.csv')

    test = pd.read_csv(ROOT.joinpath("test.csv"), index_col="pair_id")
    test['name_1'] = test['name_1'].apply(preprocess)
    test['name_2'] = test['name_2'].apply(preprocess)
    test.to_csv(ROOT / 'test_cleared.csv')

    # # %%
    # df = pd.concat([train['name_1'], train['name_2']]).drop_duplicates()
    # df = df.apply(lambda x: x.split(' '))

    # # %%
    # from itertools import chain
    # from collections import Counter

    # counts = Counter(chain.from_iterable(df.to_list()))
    # counts.most_common(100)
