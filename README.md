# ADS_portfolio

## Over mij
- Naam: Milan van Oeveren
- Leeftijd: 21 jaar
- Beroep: Student
- Studie: HBO Informatica, Avans Den Bosch
- Studentnummer: 22135073
- Minor: Applied Data Science

## DataCamp Course Certificates
<details>
  <summary>Datacamp certifactes</summary>
  
  Ik heb met Jeroen afgesproken dat ik van de eerste 10 courses er maar 4 hoefde te maken en dat ik de laatste 4 over mocht slaan.
  Hieronder zijn mijn certificaten van de gemaakte DataCamp courses te vinden.
  
  ![datacamp_1-1](https://user-images.githubusercontent.com/123479172/214436578-f9bffb7b-e5a4-4a85-aada-5d6d001e5cdb.jpg)
  ![datacamp_2-1](https://user-images.githubusercontent.com/123479172/214436581-4a5b4757-aaa7-4435-b615-befb1ae28fbc.jpg)
  ![datacamp_3-1](https://user-images.githubusercontent.com/123479172/214436584-d3bd0129-e09d-4954-8c33-e0b02222d569.jpg)
  ![datacamp_4-1](https://user-images.githubusercontent.com/123479172/214436585-68c0fef6-aa4f-4609-82f9-58fe8358bac0.jpg)
  ![datacamp_5-1](https://user-images.githubusercontent.com/123479172/214436587-84ae4f0e-7fd7-4510-9b19-ba9719f1ffb7.jpg)
  ![datacamp_6-1](https://user-images.githubusercontent.com/123479172/214436590-94e5062f-e1fd-48fb-9195-188f09e304e5.jpg)
</details>

## Code
### Foodboost
#### Scripts
- [Dataset converter](code/foodboost/scripts/dataset_converter.py)
- [Ingredient filter](code/foodboost/scripts/ingredients.py)
- [Userdata Simulator](code/foodboost/scripts/simulate_users.ipynb)
- [DecisionTree model](code/foodboost/scripts/model.ipynb)

#### App
Voor het FoodBoost project heb ik ook een [app](code/foodboost/app) gemaakt waarin de user input makkelijk kan worden opgenomen om een voorspelling te maken en dit te visualiseren.
Wat ik hier precies voor heb gedaan is te vinden in [Predictive Analytics](Predictive_Analytics.md) en [Data Preprocessing](Data_Preprocessing.md).

De belangrijkste code van de backend van de app is hier te vinden:
- [App backend](code/foodboost/app/server/app.py)

### Container
Voor het container project had ik de grootste verantwoordelijkheid voor het schrijven van de code. De eindversie van de code is ontstaan na meerdere keren feedback te hebben gekregen van de docenten.
Ook wat ik hier precies voor heb gedaan is te vinden in [Predictive Analytics](Predictive_Analytics.md) en [Data Preprocessing](Data_Preprocessing.md).

#### Versie 1
Het eerste wat ik voor het container project had gedaan, was het proberen op te zetten van een omgeving waarin containers op een veld konden worden geplaatst.
In de eerste versie heb ik dit gedaan door een 2d array in een dataframe te zetten. Verder was er in deze eerste versie een methode opgesteld waarmee er kon worden gekeken of en container wel bereikbaar was via de lange zijde.

De code voor deze omgeving is hier te vinden: [V1 Environment](code/container/v1/environment.py)

#### Versie 2
In de tweede versie is er van de environment een soort game gemaakt. In deze versie is het mogelijk om met een truck rond te rijden en containers op te pakken en te plaatsen.
Ook heb ik een methode gemaakt die de game automatisch uitspeelt op basis van mogelijke moves. In deze environment worden de actions: left, right, up, down, pickup container en place container gebruikt. Ook worden alle handelingen hierin gevisualiseerd.

De code is hier te vinden: [V2 Environment](code/container/v2/Terminal.py)

#### Versie 3
Na de tweede versie hadden we de feedback gekregen om het proces van het plaatsen van de container te versimpelen. In deze versie heb ik in plaats van de action left, right, up, down, pickup container en place container alleen de action place container (x, y).
Jurriaan had een tutorial van Reinforcement Learning gevolgd om de game Snake na te maken. Ik heb vervolgens zijn agent en model gemerged met de environment die ik had gemaakt.

De code is hier te vinden:
- [V3 Agent](code/container/v3/Terminal_agent.py)
- [V3 Environment](code/container/v3/Terminal_game.py)
- [V3 Model](code/container/v3/Terminal_model.py)

#### Final
Na de derde versie kregen wij vooral de feedback dat ons model te traag was met trainen. In de nieuwe eindversie is de focus dan ook gelegd op het verkleinen van de trainingstijd.
In de vorige versie werd bij elke zet opnieuw berekend of deze zet wel legaal was. Dit nam veel tijd in beslag, omdat dit bij elke zet voor elk vakje berekend moest worden.
In de eindversie heb ik dit kunnen versnellen door een numpy array actions aan te maken, welke na elke zet geupdate werd. Hierdoor kon er gemakkelijk opgevraagd worden welke zetten legaal waren.
Juriaan heeft zich in deze versie gefocust op het kunnen valideren van het model. Hij heeft in de Agent het mogelijk gemaakt om het model te laten stoppen met trainen en te kijken of het model niet overfit is.

De code van de eindversie is hier te vinden:
- [Final Agent](code/container/final/agent.py)
- [Final Environment](code/container/final/terminal_env.py)
- [Final Model](code/container/final/dqn_model.py)


## Predictive Analytics
- [Selecting a model](Predictive_Analytics.md#selecting-a-model)
- [Configuring a model](Predictive_Analytics.md#configuring-a-model)
- [Training a model](Predictive_Analytics.md#training-a-model)
- [Evaluating a model](Predictive_Analytics.md#evaluating-a-model)
- [Visualizing the outcome of a model](Predictive_Analytics.md#visualizing-the-outcome-of-a-model)

## Data Preprocessing
- [Data exploration](Data_Preprocessing.md)
- [Data cleansing](Data_Preprocessing.md)
- [Data preparation](Data_Preprocessing.md)
- [Data explanation](Data_Preprocessing.md)
- [Data visualization](Data_Preprocessing.md)

## Communication
- [Presentations](Communication.md#presentations)
- [Writing paper](Communication.md#writing-paper)
