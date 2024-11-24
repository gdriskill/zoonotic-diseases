import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

# Read the data with the one hot encoding
df = pd.read_csv('../ordinal_encoding/combined_output.csv')

# 
one_hot_columns = [
    "Order_Amarillovirales", "Order_Articulavirales", "Order_Blubervirales", "Order_Bunyavirales", 
    "Order_Chitovirales", "Order_Cirlivirales", "Order_Cremevirales", "Order_Durnavirales", 
    "Order_Geplafuvirales", "Order_Ghabrivirales", "Order_Hepelivirales", "Order_Herpesvirales", 
    "Order_Jingchuvirales", "Order_Martellivirales", "Order_Mononegavirales", "Order_Nidovirales", 
    "Order_Nodamuvirales", "Order_Ortervirales", "Order_Orthopolintovirales", "Order_Piccovirales", 
    "Order_Picornavirales", "Order_Reovirales", "Order_Rivendellvirales", "Order_Rowavirales", 
    "Order_Sepolyvirales", "Order_Stellavirales", "Order_Tolivirales", "Order_Tymovirales", 
    "Order_Zurhausenvirales", "Order_nan", "Family_Adenoviridae", "Family_Adintoviridae", 
    "Family_Alloherpesviridae", "Family_Anelloviridae", "Family_Astroviridae", "Family_Birnaviridae", 
    "Family_Bornaviridae", "Family_Caliciviridae", "Family_Chrysoviridae", "Family_Chuviridae", 
    "Family_Circoviridae", "Family_Coronaviridae", "Family_Demerecviridae", "Family_Flaviviridae", 
    "Family_Genomoviridae", "Family_Hantaviridae", "Family_Hepadnaviridae", "Family_Hepeviridae", 
    "Family_Kolmioviridae", "Family_Nairoviridae", "Family_Naryaviridae", "Family_Nodaviridae", 
    "Family_Nyamiviridae", "Family_Orthoherpesviridae", "Family_Orthomyxoviridae", "Family_Papillomaviridae", 
    "Family_Paramyxoviridae", "Family_Partitiviridae", "Family_Parvoviridae", "Family_Peribunyaviridae", 
    "Family_Phenuiviridae", "Family_Picobirnaviridae", "Family_Picornaviridae", "Family_Pneumoviridae", 
    "Family_Polyomaviridae", "Family_Poxviridae", "Family_Retroviridae", "Family_Rhabdoviridae", 
    "Family_Schitoviridae", "Family_Sedoreoviridae", "Family_Smacoviridae", "Family_Spinareoviridae", 
    "Family_Togaviridae", "Family_Totiviridae", "Family_Tymoviridae", "Family_nan", "Genus_Aalivirus", 
    "Genus_Alphachrysovirus", "Genus_Alphacoronavirus", "Genus_Alphainfluenzavirus", "Genus_Alpharetrovirus", 
    "Genus_Alphavirus", "Genus_Anativirus", "Genus_Aphthovirus", "Genus_Atadenovirus", "Genus_Avastrovirus", 
    "Genus_Aveparvovirus", "Genus_Aviadenovirus", "Genus_Avibirnavirus", "Genus_Avihepadnavirus", 
    "Genus_Avihepatovirus", "Genus_Avihepevirus", "Genus_Avipoxvirus", "Genus_Avisivirus", "Genus_Bandavirus", 
    "Genus_Bavovirus", "Genus_Betacoronavirus", "Genus_Brevihamaparvovirus", "Genus_Chaphamaparvovirus", 
    "Genus_Chapparvovirus", "Genus_Circovirus", "Genus_Crahelivirus", "Genus_Cyclovirus", "Genus_Cyvirus", 
    "Genus_Dalvirus", "Genus_Deltacoronavirus", "Genus_Deltavirus", "Genus_Dependoparvovirus", 
    "Genus_Enquatrovirus", "Genus_Enterovirus", "Genus_Etapapillomavirus", "Genus_Felixounavirus", 
    "Genus_Gallivirus", "Genus_Gammacoronavirus", "Genus_Gammapolyomavirus", "Genus_Gammaretrovirus", 
    "Genus_Gemycircularvirus", "Genus_Gemyduguivirus", "Genus_Gemygorvirus", "Genus_Gemykibivirus", 
    "Genus_Gemykrogvirus", "Genus_Gemykroznavirus", "Genus_Gemytondvirus", "Genus_Gruhelivirus", 
    "Genus_Grusopivirus", "Genus_Gyrovirus", "Genus_Hapavirus", "Genus_Harkavirus", "Genus_Hepacivirus", 
    "Genus_Hepatovirus", "Genus_Huchismacovirus", "Genus_Ichthamaparvovirus", "Genus_Iltovirus", 
    "Genus_Justusliebigvirus", "Genus_Khurdivirus", "Genus_Kobuvirus", "Genus_Kunsagivirus", 
    "Genus_Lambdatorquevirus", "Genus_Ludopivirus", "Genus_Lyssavirus", "Genus_Mardivirus", "Genus_Mastadenovirus", 
    "Genus_Megrivirus", "Genus_Metaavulavirus", "Genus_Metapneumovirus", "Genus_Morbillivirus", "Genus_Mosavirus", 
    "Genus_Nacovirus", "Genus_Nauglamirvirus", "Genus_Norovirus", "Genus_Nyavirus", "Genus_Orbivirus", 
    "Genus_Orivirus", "Genus_Orthoavulavirus", "Genus_Orthobornavirus", "Genus_Orthobunyavirus", 
    "Genus_Orthoflavivirus", "Genus_Orthohantavirus", "Genus_Orthohepadnavirus", "Genus_Orthonairovirus", 
    "Genus_Orthoreovirus", "Genus_Oscivirus", "Genus_Paraavulavirus", "Genus_Parechovirus", "Genus_Paslahepevirus", 
    "Genus_Passerivirus", "Genus_Pegivirus", "Genus_Phapecoctavirus", "Genus_Phlebovirus", "Genus_Picobirnavirus", 
    "Genus_Poecivirus", "Genus_Porprismacovirus", "Genus_Protoparvovirus", "Genus_Pygoscepivirus", 
    "Genus_Quaranjavirus", "Genus_Rotavirus", "Genus_Sapelovirus", "Genus_Siadenovirus", "Genus_Sicinivirus", 
    "Genus_Sunrhavirus", "Genus_Tequintavirus", "Genus_Thetapapillomavirus", "Genus_Treisepsilonpapillomavirus", 
    "Genus_Treiszetapapillomavirus", "Genus_Tremovirus", "Genus_Tupavirus", "Genus_Uukuvirus", "Genus_nan", 
    "envelope", "circular", "double_stranded", "rna", "segmented", "positive_sense", "negative_sense", 
    "envelope_na", "circular_na", "double_stranded_na", "rna_na", "segmented_na", "positive_na", 
    "negative_na", "GA_missing", "size_missing", "gc_missing", "genes_missing", 
    "cytoplasm", "cytoplasm_na", "budding", "lysis", "budding_na", "lysis_na", "other_release", 
    "other_release_na", "CE_clathrin", "CE_receptor", "CE_glycoproteins", "CE_clathrin_na", "CE_receptor_na", 
    "CE_glycoproteins_na", "other_entry", "other_entry_na"
]

ordinal_encoder = OrdinalEncoder()

for column in one_hot_columns:
    # Fit and transform the one-hot encoded column to ordinal values
    df[column] = ordinal_encoder.fit_transform(df[column].values.reshape(-1, 1))

# Step 4: Save the updated DataFrame back to a CSV (optional)
df.to_csv('updated_file.csv', index=False)

# Check the result
print(df.head())
