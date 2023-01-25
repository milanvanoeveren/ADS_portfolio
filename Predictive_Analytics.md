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
### Reinforcement Learning
Voor het opzetten van een goed Reinforcement Learning environment die bruikbaar is voor de agent zijn een paar dingen nodig [(Kanade, 2022)](Predictive_Analytics.md#Bronnen). De environment moet een state kunnen teruggeven, een reward/penalty moeten geven aan een action en het moet een action kunnen uitvoeren.

Voor het container project heb ik de environment opgezet. In de [Tweede versie van de environment](code/container/v2/Terminal.py) was de environment een soort game met een truck die kon rijden en containers kon plaatsen.
In de stukken code is te zien hoe ik de environment in de tweede versie had opgezet.

**Setup velden**
```python
def __init__(self, width, height, max_containers):
        self.fields = [[Field("container_field", max_containers) for j in range(height)] for i in range(width)]
        self.steps = 0

        width = len(self.fields)
        height = len(self.fields[0])

        for x in range(width):
            self.fields[x][0].type = "road_field"
            self.fields[x][height - 1].type = "road_field"

        for y in range(height):
            self.fields[0][y].type = "road_field"
            self.fields[width - 1][y].type = "road_field"

        self.containers_to_place = []
        for i in range(1, 24):
            self.containers_to_place.append(i)

        self.truck = Truck(0, 0)
```


**Validatie van mogelijke zetten**
```python
    def is_field_available_to_place_container(self, x, y):
        if (self.is_top_way_free(x, y) or self.is_bottom_way_free(x, y)) \
                and self.is_under_max_height(x, y) and self.fields[x][y].type == "container_field":
            return True
        return False

    def is_top_way_free(self, x, y):
        distance_to_top = y
        if distance_to_top != 0:
            for i in range(1, distance_to_top + 1):
                if len(self.fields[x][y - i].containers) > 0:
                    return False
        return True

    def is_bottom_way_free(self, x, y):
        distance_to_bottom = len(self.fields[x]) - 1 - y
        for i in range(1, distance_to_bottom + 1):
            if len(self.fields[x][y + i].containers) > 0:
                return False
        return True

    def is_under_max_height(self, x, y):
        if len(self.fields[x][y].containers) >= self.fields[x][y].max_height:
            return False
        return True

    def get_valid_moves(self, truck):
        valid_moves = []
        if self.valid_up(truck):
            valid_moves.append(0)
        if self.valid_down(truck):
            valid_moves.append(1)
        if self.valid_left(truck):
            valid_moves.append(2)
        if self.valid_right(truck):
            valid_moves.append(3)
        return valid_moves

    def valid_up(self, truck):
        if truck.y != 0 and len(self.fields[truck.x][truck.y - 1].containers) < self.fields[truck.x][truck.y - 1].max_height:
            return True
        return False

    def valid_down(self, truck):
        height = len(self.fields[0])
        if truck.y != height - 1 and len(self.fields[truck.x][truck.y + 1].containers) < self.fields[truck.x][truck.y + 1].max_height:
            return True
        return False

    def valid_left(self, truck):
        if truck.x != 0 and self.fields[truck.x - 1][truck.y].type == "road_field" and \
                len(self.fields[truck.x - 1][truck.y].containers) < self.fields[truck.x - 1][truck.y].max_height:
            return True
        return False

    def valid_right(self, truck):
        width = len(self.fields)
        if truck.x != width - 1 and self.fields[truck.x + 1][truck.y].type == "road_field" and \
                len(self.fields[truck.x + 1][truck.y].containers) < self.fields[truck.x + 1][truck.y].max_height:
            return True
        return False
```

**Loop om containers te plaatsen**
```python
    def do_random_move(self, truck):
        if truck.container is None and truck.x == 0 and truck.y == 0:
            print("Picking up new container..")
            self.pickup_new_container(truck)

        if self.is_field_available_to_place_container(truck.x, truck.y):
            if bool(random.getrandbits(1)):
                self.place_container(truck.x, truck.y, truck)
                return

        valid_moves = self.get_valid_moves(truck)
        valid_moves_str = str(valid_moves).replace("0", "up").replace("1", "down").replace("2", "left").replace("3", "right")
        print("Valid moves:", valid_moves_str)
        random.shuffle(valid_moves)

        move = valid_moves.pop()
        if move == 0:
            print("Moving up..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x) + "Y" + str(truck.y - 1))
            self.move_up(truck)
        if move == 1:
            print("Moving down..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x) + "Y" + str(truck.y + 1))
            self.move_down(truck)
        if move == 2:
            print("Moving left..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x - 1) + "Y" + str(truck.y))
            self.move_left(truck)
        if move == 3:
            print("Moving right..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x + 1) + "Y" + str(truck.y))
            self.move_right(truck)

while len(terminal.containers_to_place) > 0 or terminal.truck.container is not None:
    if terminal.truck.container is not None:
        terminal.do_random_move(terminal.truck)
        time.sleep(0.2)
    else:
        terminal.move_towards_container_spawn(terminal.truck)
        time.sleep(0.2)


print("\n=========================================================================")
print(f"        DONE PLACING ALL CONTAINERS IN {terminal.steps} STEPS")
print("=========================================================================")
```

**Visualisatie van de Environment**
![image](https://user-images.githubusercontent.com/123479172/214648378-ed9fabba-9a57-458f-8f3f-9dda7db9742f.png)

Na feedback van Tony dat we te complex zijn begonnen, heb ik de environment op een andere manier opgezet.
Tony gaf als feedback dat we moeten beginnen met alleen het voorspellen van de plek waar de container moet komen.
In de derde versie heb ik in plaats van de action left, right, up, down, pickup container en place container alleen de action place container (x, y) mogelijk gemaakt.
Ook ben ik in de derde versie begonnen met het koppelen van het environment aan de agent. 
In de stukken code hieronder is te zien welke methodes van de V3 Environment worden gebruikt door de agent.

**State**: De state bestond in de derde versie alleen maar uit een 0 of een 1 voor elk vakje, op basis van of er een container stond of niet.
```python
    def get_state(self, game):
        state = []
        for x in range(game.width):
            for y in range(game.height):
                if len(game.fields[x][y].containers) > 0:
                    state.append(1)
                else:
                    state.append(0)
```

**Berekening van de score**: in deze versie werd de berekening van de score gedaan over alle velden en niet over alleen de laatst geplaatste container.
```python
    def get_field_score(self, x, y):
        score = 0

        amount_of_containers = len(self.fields[x][y].containers)
        blocked_top = self.get_blocked_empty_fields_top(x, y)
        blocked_bottom = self.get_blocked_empty_fields_bottom(x, y)

        if self.fields[x][y].type == "road_field" and amount_of_containers > 0:
            score -= 60 * amount_of_containers
        elif amount_of_containers > self.fields[x][y].max_height:
            amount_above = amount_of_containers - self.fields[x][y].max_height
            score -= 30 * amount_above
        elif amount_of_containers > 0:
            score += 20

        score -= blocked_top * 15
        score -= blocked_bottom * 15

        return score

    def calculate_score(self):
        score = 0

        width = len(self.fields)
        height = len(self.fields[0])

        for x in range(width):
            for y in range(height):
                field_score = self.get_field_score(x, y)
                score += field_score

        self.score = score
        return score
```

**Play step**
```python
    def play_step(self, final_move):
        old_score = self.calculate_score()

        final_move_index = final_move.index(1)
        final_x = final_move_index // self.height
        final_y = final_move_index - final_x * self.height

        self.place_container(self.containers_to_place.pop(0), final_x, final_y)

        self.steps += 1

        self.frame_iteration += 1
        self.update_ui()

        new_score = self.calculate_score()

        reward = new_score-old_score,

        done = len(self.containers_to_place) == 0

        return reward, done, new_score
```

**Visualisatie van de Environment**
![image](https://user-images.githubusercontent.com/123479172/214648554-d6bde3bf-b214-41ec-9488-9cedae74bf72.png)

Na de derde versie kregen wij vooral de feedback dat ons model te traag was met trainen. 
In de nieuwe eindversie is de focus dan ook gelegd op het verkleinen van de trainingstijd. 
In de vorige versie werd bij elke zet opnieuw berekend of deze zet wel legaal was. 
Dit nam veel tijd in beslag, omdat dit bij elke zet voor elk vakje berekend moest worden. 
In de eindversie heb ik dit kunnen versnellen door een numpy array actions aan te maken, welke na elke zet geupdate werd. 
Hierdoor kon er gemakkelijk opgevraagd worden welke zetten legaal waren. Juriaan heeft zich in deze versie gefocust op het kunnen valideren van het model. 
Hij heeft in de Agent het mogelijk gemaakt om het model te laten stoppen met trainen en te kijken of het model niet overfit is.

In de stukken code hieronder is te zien hoe de laatste versie van het environment is opgezet:

**Setup van de environment**
```python
    def __init__(self, width, height, max_containers, given_set=None):
        self.width = width
        self.height = height
        self.max_containers = max_containers

        self.score = 0

        self.fields = None
        self.fields_z = None
        self.actions = None

        self.containers_to_place = None

        self.set = given_set

        self.reset(0)
```

**State**: de state van de eindversie bestaat uit:
- Voor elk vakje of je er een container mag plaatsen
- Voor elk vakje of er een container staat die voor hetzelfde schip is bedoeld als de volgende container die geplaatst gaat worden
- Voor elk vakje of er een container staat
```python
    def get_state(self):
        amount_of_fields = self.width * self.height

        actions = list(np.reshape(self.actions, amount_of_fields))
        container_list = []
        same_container = []

        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.max_containers):
                    field = self.fields[x][y][z]

                    if field != 0:
                        container_list.append(1)
                    else:
                        container_list.append(0)

                    if len(self.containers_to_place) == 0 or field != self.containers_to_place[0]:
                        same_container.append(0)
                    else:
                        same_container.append(1)

        state = actions + container_list + same_container

        return state
```

**Update legale actions**: In deze methode worden de legale actions geupdate
```python
    def update_action(self, x, y, z_top_container):
        blocked_fields = 0

        if z_top_container + 1 >= self.max_containers:
            self.actions[x][y] = 0

        if z_top_container == 0:
            row = self.fields[x][:][z_top_container]
            before_row, after_row = row[:y], row[y + 1:]

            # Before
            last_index_match = None
            for i, value in enumerate(reversed(before_row)):
                if value != 0:
                    last_index_match = len(before_row) - i - 1
                    break

            if last_index_match is not None:
                amount = len(before_row) - last_index_match
                for i in range(1, amount):
                    blocked_fields += 1
                    self.actions[x][y - i] = 0

            # After
            index_first_match = next((index for index, item in enumerate(after_row) if item != 0), None)
            if index_first_match:
                for i in range(1, index_first_match + 1):
                    blocked_fields += 1
                    self.actions[x][y + i] = 0

        return blocked_fields
```

**Reward functie**: De reward functie kijkt nu alleen naar de laatst geplaatste container en niet naar de hele opstelling
```python
    def get_reward(self, container_id, x, y):
        reward = 10

        z_top_container = self.fields_z[x][y] - 1

        # score for same ids under
        for i in reversed(range(z_top_container + 1)):
            if self.fields[x][y][i] == container_id and z_top_container != i:
                reward += 4
            else:
                reward -= 6

        before_row, after_row = [], []
        for i in range(self.height):
            if i < y:
                before_row.append(self.fields[x][i][z_top_container])
            if i > y:
                after_row.append(self.fields[x][i][z_top_container])

        for j in reversed(before_row):
            if j == container_id:
                reward += 5
            else:
                break

        for k in after_row:
            if k == container_id:
                reward += 5
            else:
                break

        return reward
```

**Play step**
```python
    def play_step(self, action):
        done = False
        reward = 0

        action_index = action.index(1)
        x, y = self.index_to_x_y(action_index)

        next_container = self.containers_to_place.pop(0)
        valid, placed = self.place_container(next_container, x, y)

        if placed:
            z_top_container = self.fields_z[x][y] - 1
            blocked_fields = self.update_action(x, y, z_top_container)
            reward -= blocked_fields * 5
        if valid:
            reward += self.get_reward(next_container, x, y)
        else:
            reward = -10

        self.score += reward

        if len(self.containers_to_place) == 0:
            done = True

        return reward, done, self.score
```

**Visualisatie van de Environment**
![image](https://user-images.githubusercontent.com/123479172/214648685-7b5fd82d-d2ab-4be3-8fb2-b4696dbf2a60.png)

Zoals te zien is, is de code veel compacter geworden en het environment kan veel efficiënter gebruikt worden dan bij de eerdere versies. De code is bijna 2 keer zo klein als de eerdere versies.
Ook heb ik de state binair gehouden, omdat dit voor de agent sneller te verwerken is.

## Training a model
### Foodboost
todo

### Reinforcement Learning
Voor het Reinforcement Learning gedeelte heb ik voor de finale versie van de code een script geschreven die de resultaten van het model met verschillende hyperparameters in een grafiek laat zien.
Hierdoor kunnen de beste hyperparamaters worden gekozen.
De code van het script voor het maken van de plot staat hieronder:

```python
df = pd.read_csv("tune_training.csv")
groups = df.groupby("tune_name")

fig = plt.figure(figsize=(10, 4))
ax = fig.add_subplot(111)

for name, group in groups:
    mean_scores = []
    i = 1
    for score in group["score"]:
        if i > 100:
            scores = group["score"][i-100:i]
        else:
            scores = group["score"][:i]
        scores_count = len(scores)
        scores_sum = sum(scores)
        mean_scores.append(scores_sum / scores_count)
        i += 1

    ax.plot(group["game_id"], mean_scores, label=f'{name}: {mean_scores[-1]}')
    
plt.show()
```

Uit de resultaten van deze test bleek dat een Learning Rate van 0.001 en een Batch Size van 128 het beste werkte. Vervolgens heb ik met de code van Jurriaan het model getraind en gevalideerd op basis van een train- en validatieset.

## Evaluating a model
### Foodboost
Voor het FoodBoost project hebben we een aantal verschillende modellen met elkaar vergeleken. 
Ik heb mij beziggehouden met het [DecisionTree model](code/foodboost/scripts/model.ipynb). Verder heeft de rest van de groep zich bezig gehouden met:
- KNN
- Random Forest
- KNN
- Naive Bayes

Verder had ik bij mijn Decision Tree model een loop gedaan over de verschillende max_depths van de decision tree, om te kijken welke waardes de beste resultaten geven.
De resultaten van mijn [DecisionTree model](code/foodboost/scripts/model.ipynb) zijn hieronder te vinden:

**Resultaten per max_depth**
![image](https://user-images.githubusercontent.com/123479172/214648093-e07f5c0b-07a4-42fa-bfc2-383d48ca68fb.png)

**Confusion Matrix**
![image](https://user-images.githubusercontent.com/123479172/214648172-c52b51be-35d0-47bf-8a4e-ada259a859b0.png)

## Visualizing the outcome of a model


# Bronnen
- Odemakinde, E. (2022, 14 november). Model-Based and Model-Free Reinforcement Learning: Pytennis Case Study. neptune.ai. https://neptune.ai/blog/model-based-and-model-free-reinforcement-learning-pytennis-case-study
- Kanade, V. (2022, September 29). What Is Reinforcement Learning? Working, Algorithms, and Uses. https://www.spiceworks.com/tech/artificial-intelligence/articles/what-is-reinforcement-learning/
