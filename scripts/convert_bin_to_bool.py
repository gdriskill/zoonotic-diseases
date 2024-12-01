import pandas as pd

virus_df = pd.read_csv("../data/divide_and_conquer/final_virus_features.csv")
virus_columns_to_convert=["rna","rt","double_stranded","negative_sense","positive_sense","enveloped","circular","segmented","cytoplasm", "direct","direct_sexual","direct_vertical","indirect","fecal_oral","ingestion","inhalation","environment","vector","release_budding","release_lysis","release_other","CE_clathrin","CE_receptor","ce_glycoprotiens","ce_other"]

virus_df[virus_columns_to_convert] = virus_df[virus_columns_to_convert].astype(bool)

virus_df.to_csv("../data/divide_and_conquer/final_virus_features_bool.csv", index=False)


#hosts
hosts_df = pd.read_csv("../data/divide_and_conquer/final_mammal_features.csv")
hosts_columns_to_convert=[
   "nocturnal","diurnal","migratory","forest","savanna","shrubland","grassland",
   "wetlands","rocky","desert","cave_subterranean","marine_neritic","marine_oceanic",
   "marine_intertidal","marine_coastal","artifical"
]

hosts_df[hosts_columns_to_convert] = hosts_df[hosts_columns_to_convert].astype(bool)

hosts_df.to_csv("../data/divide_and_conquer/final_mammal_features_bool.csv", index=False)

