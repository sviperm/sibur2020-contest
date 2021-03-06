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
                      r"s\.c\.r\.l\.", r"gmbh", r"pvt\.", r"imp\.",
                      #   r"s\.a\.",
                      r"de c\.v\.", r"c\.v\.", r"exp\.", r"llc", r"corp\.",
                      r"ltda",
                      r"ооо", r"оао"]

    company_regexp = rf"({'|'.join(legal_entities)})[\W]*"

    company = re.sub(company_regexp, '', company)

    company = re.sub(r'[^\w&\s]', '', company)

    popular_words = ["энтерпрайс", "ооо",
                     "ltda", "de sa de cv",
                     "industries", "industrial", "industria", "imperial",
                     "international", "global", "logistics", "logistic",
                     "private", "corporation", "management", "consolidated",
                     "trading", ]

    popular_regexp = rf"({'|'.join(popular_words + countries)})[\W]+"
    company = re.sub(popular_regexp, '', company)

    # countries_regexp = rf"({'|'.join(countries)})[\W]*"
    # company = re.sub(countries_regexp, '', company)

    company = company.strip()
    company = re.sub(r'\s&$', '', company)
    company = re.sub(r'\s{2,}', ' ', company)

    return company


# %%
if __name__ == "__main__":
    # text = "Dongguan Silk Imp.& Exp.Co. Ltd.Of Guangdong"
    # print(preprocess(text))
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
    # ROOT = Path(__file__).parents[1] / "data"
    # train = pd.read_csv(ROOT.joinpath("train_cleared.csv"), index_col="pair_id")
    # column = pd.concat([train['name_1'], train['name_2']]).reset_index(drop=True).drop_duplicates()

    # def fun(text):
    #     try:
    #         return str(text).split(' ')
    #     except Exception:
    #         return text

    # column = column.apply(fun)

    # # %%
    # from itertools import chain
    # from collections import Counter

    # counts = Counter(chain.from_iterable(column.to_list()))
    # counts.most_common(100)
