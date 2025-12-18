import os

import pandas as pd
from dtale import show

# Load each directory, sorted directory needed for looping purposes (each folder has the same named, same number of files)
bilanco_directory = "/home/gun/Documents/Bilançolar/"
sorted_directory = sorted(os.listdir(bilanco_directory))
kar_zarar_directory = "/home/gun/Documents/KarZararTabloları/"
nakit_akis_directory = "/home/gun/Documents/NakitAkışTabloları/"

for file in sorted_directory:
    print(file)
    df = pd.read_excel(f"{bilanco_directory}{file}")
    df = df.set_index("Finansal Durum Tablosu (Bilanço)")
    transform_df = df.T  # Transforming the dataframe for ease of calculations between column in the future
    transform_df.index.name = "Period"
    previous_periods_df = transform_df.shift(-4)
    average_df = (transform_df + previous_periods_df) / 2
    average_df = average_df.iloc[:-4]

    kz_df = pd.read_excel(f"{kar_zarar_directory}{file}")
    kz_df = kz_df.set_index("Kar Zarar Tablosu")

    # Skipping every Q1 period for quarterly measurements
    skip_column = [i for i in range(len(kz_df.columns)) if (i + 2) % 4 == 0]
    kar_zarar_ceyreklik_df = kz_df.copy()
    for i in range(len(kz_df.columns) - 1):
        if i not in skip_column:
            kar_zarar_ceyreklik_df.iloc[:, i] = kz_df.iloc[:, i] - kz_df.iloc[:, i + 1]

    kar_zarar_ceyreklik_df_transformed = kar_zarar_ceyreklik_df.T
    kar_zarar_ceyreklik_df_transformed.index.name = "Period"
    kar_zarar_ceyreklik_df_transformed = kar_zarar_ceyreklik_df_transformed.iloc[:-1]

    # Calculating cumulative sum for each column to find yearly data
    kar_zarar_yillik_df = (
        kar_zarar_ceyreklik_df_transformed
        + kar_zarar_ceyreklik_df_transformed.shift(-1)
        + kar_zarar_ceyreklik_df_transformed.shift(-2)
        + kar_zarar_ceyreklik_df_transformed.shift(-3)
    )
    kar_zarar_yillik_df = kar_zarar_yillik_df[:-3]

    na_df = pd.read_excel(f"{nakit_akis_directory}{file}")
    na_df = na_df.set_index("Nakit Akış Tablosu")

    nakit_akis_ceyreklik_df = na_df.copy()
    for i in range(len(na_df.columns) - 1):
        if i not in skip_column:
            nakit_akis_ceyreklik_df.iloc[:, i] = na_df.iloc[:, i] - na_df.iloc[:, i + 1]

    nakit_akis_ceyreklik_df_transformed = nakit_akis_ceyreklik_df.T
    nakit_akis_ceyreklik_df_transformed.index.name = "Period"
    nakit_akis_ceyreklik_df_transformed = nakit_akis_ceyreklik_df_transformed.iloc[:-1]

    nakit_akis_yillik_df = (
        nakit_akis_ceyreklik_df_transformed
        + nakit_akis_ceyreklik_df_transformed.shift(-1)
        + nakit_akis_ceyreklik_df_transformed.shift(-2)
        + nakit_akis_ceyreklik_df_transformed.shift(-3)
    )
    nakit_akis_yillik_df = nakit_akis_yillik_df[:-3]

    # show(average_df, subprocess=False, open_browser=True)
    # show(nakit_akis_ceyreklik_df_transformed, subprocess=False, open_browser=True)
    # show(nakit_akis_yillik_df, subprocess=False, open_browser=True)
    # show(kar_zarar_ceyreklik_df_transformed, subprocess=False, open_browser=True)
    # show(kar_zarar_yillik_df, subprocess=False, open_browser=True)

    average_df.to_excel(f"/home/gun/Documents/DüzenlenmişBilanço/{file}", index=True)
    # kar_zarar_ceyreklik_df_transformed.to_excel(f"/home/gun/Documents/KarZararTablolarıÇeyreklik/{file}", index=True)
    # kar_zarar_yillik_df.to_excel(f"/home/gun/Documents/KarZararTablolarıYıllık/{file}", index=True)
    # nakit_akis_ceyreklik_df_transformed.to_excel(f"/home/gun/Documents/NakitAkışTablolarıÇeyreklik/{file}", index=True)
    # nakit_akis_yillik_df.to_excel(f"/home/gun/Documents/NakitAkışTablolarıYıllık/{file}", index=True)
