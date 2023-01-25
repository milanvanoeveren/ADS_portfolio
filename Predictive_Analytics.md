# Predictive Analytics

## Selecting a model
### Foodboost
Voor het FoodBoost project hebben we als groep allemaal een model gekozen die we gingen uitwerken. Ik heb mij bezig gehouden met het uitwerken van een KNN model.
Dit model is te vinden 

### Reinforcement Learning
Toen wij het container project hadden gekozen, hoorden we van Jeroen dat Reinforcement Learning hier bij zou kunnen werken.
Na onderzoek te hebben gedaan ben ik erachter gekomen dat wij voor dit project een model-free algoritme nodig hebben.
Een model-free algoritme leert namelijk de consequenties van zijn acties door ervaring [(Odemakinde, 2022)](Predictive_Analytics.md#Bronnen). Dit past goed bij ons project, omdat het algortime zelf gaat uitzoeken welke acties goed zijn, op basis van de ervaring.

Om een idee van Reinforcement learning te krijgen heb ik verschillende tutorials bekeken. Het grootste deel van deze tutorials gebruikten ook een model-free algoritme, namelijk Q-Learning.
Veel van deze tutorials gebruikte DQN, een variant van Q-Learning. DQN zal een actie meerdere keren uitvoeren en zal de strategie achter zijn acties aanpassen voor optimale rewards op basis van de uitkomsten.
Dit is perfect voor het container project, omdat het model dan zelf containers kan gaan plaatsen en op basis van de reward functie de gewichten kan gaan aanpassen om beter te leren en een hogeres score te behalen.

Jurriaan had ook een van deze tutorials gevolgd en had hier de code nog van. Dit was een tutorial van het spel Snake en deze gebruikte ook DQN. Op basis van dit project zijn we verder gaan werken met DQN. 

## Configuring a Model

## Training a model

## Evaluating a model

## Visualizing the outcome of a model


# Bronnen
Odemakinde, E. (2022, 14 november). Model-Based and Model-Free Reinforcement Learning: Pytennis Case Study. neptune.ai. https://neptune.ai/blog/model-based-and-model-free-reinforcement-learning-pytennis-case-study