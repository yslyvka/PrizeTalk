# PrizeTalk Public Data Description
--------------------------------------------------------------------------------------------------------------------

Description of data from Booker Prize CSV (Booker Prize Dataset Final.csv):
Pulled from: https://www.kaggle.com/datasets/rowrowrowyourboat72/booker-prize-winners-1969-2023/data

Attributes and Data Types:
- SL. NO.: int - Serial number
- YEAR: int - Year of the award
- WINNER: string - Name of the winner
- NOVEL: string - Title of the winning novel
- LENGTH OF BOOK: int - Length of the book in pages
- LENGTH OF BOOK BIN: string - Binned length category (e.g., '300')
- GENDER: string - Gender of the winner ('M' or 'F')
- BIRTH YEAR: int - Birth year of the winner
- AGE WHEN WON: int - Age of the winner at the time of winning
- AGE BIN: string - Binned age category (e.g., '55')
- GENRE: string - Genre of the novel
- NATIONALITY AT TIME OF VICTORY: string - Nationality of the winner at the time of victory
- COUNTRY OF BIRTH: string - Country of birth of the winner
- PUBLISHER: string - Publisher of the novel
- ALMA MATER: string - Educational institution attended by the winner
- BOOK NO. THAT WON (Only fiction novels): int - Number of the book that won

--------------------------------------------------------------------------------------------------------------------

Description of data from Golden Globes CSV (Golden_Globes_Awards_Dataset.csv):
Pulled from: https://www.kaggle.com/datasets/dimitarmitkov/golden-globe-awards-1944-2024/data

Attributes and Data Types:
- (index): int - Row index
- nominee_type: string - Type of nominee ('tv-show', 'film', 'people')
- year: int - Year of the award
- winner: bool - Whether the nominee won (True/False)
- award: string - Name of the award
- title: string - Title of the work

--------------------------------------------------------------------------------------------------------------------

Description of data from Grammy CSV (Grammy Award Nominees and Winners 1958-2024.csv):
Pulled from: https://www.kaggle.com/code/mahmoudredagamail/grammy-award-nominees-and-winners-1958-2024/input

Attributes and Data Types:
- (index): int - Row index
- Year: int - Year of the award
- Ceremony: int - Ceremony number
- Award ID: int - Unique ID for the award category
- Award Type: string - Type of award ('Work' or 'Nominee')
- Award Name: string - Name of the award category
- Work: string - Work being considered (nullable)
- Nominee: string - Name of the nominee
- Winner: bool - Whether the nominee won (True/False)

--------------------------------------------------------------------------------------------------------------------

Description of data from Nobel Laureates CSV (nobel_laureates.csv):
Pulled from: https://nobelprize.readme.io/reference/getting-started

Attributes and Data Types:
This CSV contains detailed information about Nobel laureates in a flattened JSON format. Key attributes include:
- id: int - Unique identifier for the laureate
- fileName: string - Filename identifier
- gender: string - Gender of the laureate
- sameAs: string - Wikidata/Wikipedia links (JSON array)
- links: string - API links (JSON array)
- nobelPrizes: string - Nobel prizes won (JSON array)
- knownName.en: string - Known name in English
- knownName.se: string - Known name in Swedish
- givenName.en: string - Given name in English
- givenName.se: string - Given name in Swedish
- familyName.en: string - Family name in English
- familyName.se: string - Family name in Swedish
- fullName.en: string - Full name in English
- fullName.se: string - Full name in Swedish
- birth.date: string - Birth date
- birth.place.city.en: string - Birth city in English
- birth.place.city.no: string - Birth city in Norwegian
- birth.place.city.se: string - Birth city in Swedish
- birth.place.country.en: string - Birth country in English
- birth.place.country.no: string - Birth country in Norwegian
- birth.place.country.se: string - Birth country in Swedish
- birth.place.cityNow.en: string - Current birth city name in English
- birth.place.cityNow.no: string - Current birth city name in Norwegian
- birth.place.cityNow.se: string - Current birth city name in Swedish
- birth.place.cityNow.sameAs: string - Wikidata links for current city
- birth.place.cityNow.latitude: float - Latitude of birth place
- birth.place.cityNow.longitude: float - Longitude of birth place
- birth.place.countryNow.en: string - Current birth country in English
- birth.place.countryNow.no: string - Current birth country in Norwegian
- birth.place.countryNow.se: string - Current birth country in Swedish
- birth.place.countryNow.sameAs: string - Wikidata links for current country
- birth.place.countryNow.latitude: float - Latitude of birth country
- birth.place.countryNow.longitude: float - Longitude of birth country
- birth.place.continent.en: string - Continent in English
- birth.place.continent.no: string - Continent in Norwegian
- birth.place.continent.se: string - Continent in Swedish
- birth.place.locationString.en: string - Location string in English
- birth.place.locationString.no: string - Location string in Norwegian
- birth.place.locationString.se: string - Location string in Swedish
- wikipedia.slug: string - Wikipedia slug
- wikipedia.english: string - English Wikipedia URL
- wikidata.id: string - Wikidata ID
- wikidata.url: string - Wikidata URL
- death.date: string - Death date
- death.place.city.en: string - Death city in English
- death.place.city.no: string - Death city in Norwegian
- death.place.city.se: string - Death city in Swedish
- death.place.country.en: string - Death country in English
- death.place.country.no: string - Death country in Norwegian
- death.place.country.se: string - Death country in Swedish
- death.place.country.sameAs: string - Wikidata links for death country
- death.place.cityNow.en: string - Current death city name in English
- death.place.cityNow.no: string - Current death city name in Norwegian
- death.place.cityNow.se: string - Current death city name in Swedish
- death.place.cityNow.sameAs: string - Wikidata links for current death city
- death.place.cityNow.latitude: float - Latitude of death place
- death.place.cityNow.longitude: float - Longitude of death place
- death.place.countryNow.en: string - Current death country in English
- death.place.countryNow.no: string - Current death country in Norwegian
- death.place.countryNow.se: string - Current death country in Swedish
- death.place.countryNow.sameAs: string - Wikidata links for current death country
- death.place.countryNow.latitude: float - Latitude of death country
- death.place.countryNow.longitude: float - Longitude of death country
- death.place.continent.en: string - Death continent in English
- death.place.continent.no: string - Death continent in Norwegian
- death.place.continent.se: string - Death continent in Swedish
- death.place.locationString.en: string - Death location string in English
- death.place.locationString.no: string - Death location string in Norwegian
- death.place.locationString.se: string - Death location string in Swedish
- knownName.no: string - Known name in Norwegian
- givenName.no: string - Given name in Norwegian
- familyName.no: string - Family name in Norwegian
- fullName.no: string - Full name in Norwegian
- acronym: string - Acronym (for organizations)
- orgName.en: string - Organization name in English
- orgName.no: string - Organization name in Norwegian
- orgName.se: string - Organization name in Swedish
- founded.date: string - Founded date
- founded.place.city.en: string - Founded city in English
- founded.place.city.no: string - Founded city in Norwegian
- founded.place.city.se: string - Founded city in Swedish
- founded.place.country.en: string - Founded country in English
- founded.place.country.no: string - Founded country in Norwegian
- founded.place.country.se: string - Founded country in Swedish
- founded.place.country.sameAs: string - Wikidata links for founded country
- founded.place.cityNow.en: string - Current founded city name in English
- founded.place.cityNow.no: string - Current founded city name in Norwegian
- founded.place.cityNow.se: string - Current founded city name in Swedish
- founded.place.cityNow.sameAs: string - Wikidata links for current founded city
- founded.place.countryNow.en: string - Current founded country in English
- founded.place.countryNow.no: string - Current founded country in Norwegian
- founded.place.countryNow.se: string - Current founded country in Swedish
- founded.place.countryNow.sameAs: string - Wikidata links for current founded country
- founded.place.continent.en: string - Founded continent in English
- founded.place.continent.no: string - Founded continent in Norwegian
- founded.place.continent.se: string - Founded continent in Swedish
- founded.place.locationString.en: string - Founded location string in English
- founded.place.locationString.no: string - Founded location string in Norwegian
- founded.place.locationString.se: string - Founded location string in Swedish
- nativeName: string - Native name
- penName: string - Pen name
- penNameOf.fullName: string - Full name of pen name
- foundedCountry.en: string - Founded country in English
- foundedCountry.no: string - Founded country in Norwegian
- foundedCountry.se: string - Founded country in Swedish
- foundedCountryNow.en: string - Current founded country in English
- foundedCountryNow.no: string - Current founded country in Norwegian
- foundedCountryNow.se: string - Current founded country in Swedish
- foundedContinent.en: string - Founded continent in English

--------------------------------------------------------------------------------------------------------------------

Description of data from Nobel Prizes CSV (nobel_prizes.csv):
Pulled from: https://nobelprize.readme.io/reference/getting-started

Attributes and Data Types:
- awardYear: int - Year of the award
- dateAwarded: string - Date the award was awarded (YYYY-MM-DD)
- prizeAmount: int - Prize amount in original currency
- prizeAmountAdjusted: int - Prize amount adjusted for inflation
- links: string - API links (JSON array)
- laureates: string - Laureates information (JSON array)
- category.en: string - Category in English
- category.no: string - Category in Norwegian
- category.se: string - Category in Swedish
- categoryFullName.en: string - Full category name in English
- categoryFullName.no: string - Full category name in Norwegian
- categoryFullName.se: string - Full category name in Swedish
- topMotivation.en: string - Top motivation in English
- topMotivation.se: string - Top motivation in Swedish

--------------------------------------------------------------------------------------------------------------------

Description of data from Oscars CSV (oscars.csv):
Pulled from: https://github.com/DLu/oscar_data?tab=readme-ov-file

Attributes and Data Types:
- Ceremony: int - Ordinal for which ceremony the nomination was for (starting at 1)
- Year: string - Year(s) from which the films are honored (e.g., '1927/28')
- Class: string - Broad grouping for categories (e.g., 'Acting', 'Directing')
- CanonicalCategory: string - Standardized category name
- Category: string - Precise category name according to Oscars.org
- Film: string - Title of the film (pipe-separated if multiple)
- FilmId: string - IMDb Title ID (pipe-separated if multiple, starting with 'tt')
- Name: string - Precise text used for who is being nominated
- Nominees: string - Names of nominees without extra text (pipe-separated if multiple)
- NomineeIds: string - IMDb Name IDs or Company IDs for nominated entities (pipe-separated if multiple)
- Winner: bool - True if the award was won
- Detail: string - Detail about the nomination (e.g., character name, song title)
- Note: string - Additional information
- Citation: string - Official text of the award statement (for Scientific/Technical/Honorary awards)

--------------------------------------------------------------------------------------------------------------------