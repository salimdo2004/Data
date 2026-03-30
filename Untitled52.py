# Generated from: Untitled52.ipynb
# Converted at: 2026-03-30T12:41:04.133Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

# <a href="https://colab.research.google.com/github/salimdo2004/Data/blob/main/Untitled52.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
# Configuration du style des graphiques avec seaborn
import seaborn as sns
sns.set_style("darkgrid")

datas = pd.read_csv("ssa-names-2022-MAY-complete (1).csv")
datas

datas.head()

datas.columns

# Afficher toutes les années présentes dans la base de données
print(datas['Year'].unique())

# Filtrer les données entre 1910 et 2021
data = datas[(datas['Year'] >= 1910) & (datas['Year'] <= 2021)]

# Vérifier les premières lignes du nouveau dataset filtré
print(data.head())

pieces = []
# Création d'une liste d'années
years = range(1910, 2021)
# Boucle pour récupérer les données année par année
for year in years:
     # Sélection des données correspondant à l'année
    frame = datas[datas['Year'] == year]
    pieces.append(frame)
# Concaténation de toutes les années dans un seul dataframe
data = pd.concat(pieces)

print(data.head())

data.head()

# Création d'un graphique pour le nombre total de naissances des 10 dernières années
plt.figure(figsize=(15,8))
# Calcul du nombre total de naissances par année
births = data.groupby("Year")["Count"].sum()
# Calcul du nombre total de naissances par année
sns.barplot(
     x=births.index[-10:],   # les 10 dernières années
    y=births.values[-10:],  # nombre de naissances
    palette="viridis"
)

plt.ylabel("Number of Births")
plt.xlabel("Year")
plt.title("Number of births (Last 10 Years)")

plt.show()

data.shape

# Création d'un tableau pivot pour voir les naissances par sexe et par année
total_births = data.pivot_table(values="Count", index="Year",
                                 columns="Sex", aggfunc=sum)

# Affichage des dernières lignes
total_births.tail()

# Graphique montrant les naissances par sexe au fil des années
total_births.plot(figsize=(12,6))
plt.title("Births by Sex per Year")
plt.ylabel("Number of Births")
plt.show()

# Fonction pour calculer la proportion de chaque prénom par rapport au total des naissances
def add_prop(group):
    group['prop'] = group.Count/ group.Count.sum()
    return group
# Application de la fonction sur chaque groupe (année, sexe)
names = data.groupby(['Year', 'Sex']).apply(add_prop)

names

# Réinitialiser l'index
names = names.reset_index(drop=True)
# Vérifier que la somme des proportions est égale à 1
names.groupby(['Year', 'Sex'])['prop'].sum()

# Fonction pour récupérer les 1000 prénoms les plus populaires
def get_top_1000(group):
    return group.sort_values(by="Count", ascending=False)[:1000]

# Regrouper par année et sexe
grouped = names.groupby(['Year', 'Sex'])
# Appliquer la fonction
top1000 = grouped.apply(get_top_1000)
# Réinitialiser l'index
top1000.reset_index(inplace=True, drop=True)

# Afficher quelques lignes spécifiques
top1000.take([1000, 2000, 30000, 13444])

# Afficher les 10 prénoms les plus utilisés dans toute la base
top1000.groupby(["Name", "Sex"])["Count"].sum().sort_values(ascending=False).head(10)

# Séparer les prénoms masculins et féminins
boys = top1000[top1000.Sex == "M"]
girls = top1000[top1000.Sex == "F"]

# Création d'un pivot pour analyser les prénoms au fil des années
total_births = top1000.pivot_table(values="Count", index="Year",
                                   columns="Name", aggfunc=sum)
total_births

# Informations sur le dataframe
total_births.info()

# Sélection de quelques prénoms pour analyse
subset = total_births[['John', 'Harry', 'Mary', 'James']]

# Création d'un graphique montrant l'évolution de ces prénoms
import matplotlib.pyplot as plt

# Sélection des prénoms
subset = total_births[['John', 'Harry', 'Mary', 'James']]

# Création du graphique
ax = subset.plot(
    subplots=True,
    figsize=(18,10),
    grid=True,
    linewidth=2,
    title="Evolution of Births per Year for Selected Names"
)

# Personnalisation des axes
plt.xticks(range(1880, 2021, 10), rotation=45)
plt.xlabel("Year")
plt.ylabel("Number of Births")

# Ajustement de l'affichage
plt.tight_layout()

# Affichage
plt.show()

# Analyse de la diminution de l'utilisation des prénoms populaires

table = top1000.pivot_table(values='prop', index='Year',
                            columns='Sex', aggfunc=sum)
# Graphique de la proportion cumulée des 1000 prénoms populaires
_ = table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2019, 23),
           figsize=(15, 10))

# Graphique de la proportion cumulée des 1000 prénoms populaires
df = boys[boys.Year == 2010]
df.prop.sum()

# Calcul de la somme cumulative des proportions
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
prop_cumsum[:10]

# Trouver combien de prénoms représentent 50% des naissances
prop_cumsum.values.searchsorted(0.5)

# Analyse pour l'année 1900
df = boys[boys.Year == 1900]

in1900 = df.sort_values(by="prop", ascending=False).prop.cumsum()

# Nombre de prénoms nécessaires pour atteindre 50% des naissances

in1900.values.searchsorted(0.5) + 1

# Fonction pour calculer le nombre de prénoms nécessaires pour atteindre un certain seuil

def get_quantile_count(group, q=0.5):
    group = group.sort_values(by="prop", ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1

# Application pour chaque année et chaque sexe
diversity = top1000.groupby(['Year', 'Sex']).apply(get_quantile_count)
print(diversity)

# Transformer la table
diversity = diversity.unstack("Sex")

diversity.head()

# Graphique montrant la diversité des prénoms
diversity.plot(title="Number of popular names to be in top 50%", figsize=(15, 8))
_ = plt.xticks(range(1880, 2019, 23))

# Extraction de la dernière lettre des prénoms

get_last_letter = lambda x: x[-1]
last_letters = names.Name.map(get_last_letter)
last_letters.name = 'last_letter'


# Création d'un tableau pivot basé sur la dernière lettre

table = names.pivot_table(values="Count", index=last_letters,
                          columns=['Sex', 'Year'], aggfunc=sum)
table

# Sélection de certaines années pour analyse

subtable = table.reindex(columns=[1910, 1960, 2000, 2018], level="Year")

subtable.head()

# Normalisation des données

subtable.sum()


letter_prop = subtable / subtable.sum()
letter_prop.fillna(0, inplace=True)
letter_prop.head()

# Graphique de la distribution des dernières lettres

fig, axes = plt.subplots(2, 1, figsize=(15, 10))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female')
plt.tight_layout(pad=1.5)

# Analyse de certaines lettres finales
letter_prop = table / table.sum()
dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T
dny_ts.head()

# Graphique de l'évolution de ces lettres
dny_ts.plot(figsize=(12, 8))
_ = plt.xticks(range(1880, 2019, 23))

# Recherche des prénoms similaires à "Lesley"
all_names = pd.Series(top1000.Name.unique())

lesley_like = all_names[all_names.str.lower().str.contains('lesl')]
lesley_like

# Filtrer ces prénoms dans le dataset

filtered = top1000[top1000.Name.isin(lesley_like)]
filtered


# Nombre total de naissances pour ces prénoms
filtered.groupby('Name').Count.sum()

# Tableau pivot pour analyser l'évolution par sexe
table = filtered.pivot_table(values='Count', index='Year',
                             columns='Sex', aggfunc='sum')
table

# Calcul de la proportion par sexe
table = table.div(table.sum(1), axis=0)
table.tail()

# Graphique montrant la transition du prénom Lesley entre masculin et féminin
_ = table.plot(style={'M': 'k-', 'F': 'k--'}, figsize=(12, 8))
