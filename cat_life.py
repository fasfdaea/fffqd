import json
import os
import random


SAVE_FILE = "cat_save.json"


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def format_hours(hours):
    whole_hours = int(hours)
    if whole_hours != hours:
        unit = "часа"
    elif whole_hours % 10 == 1 and whole_hours % 100 != 11:
        unit = "час"
    elif 2 <= whole_hours % 10 <= 4 and not 12 <= whole_hours % 100 <= 14:
        unit = "часа"
    else:
        unit = "часов"
    return f"{hours:g} {unit}"


class Cat:
    """Максимально реалистичная симуляция жизни котика: сон, питание, туалет, уход, стресс и смерть."""

    def __init__(self, name="котэк", age=0.0, sex="male"):
        self.name = name
        self.sex = sex
        self.age = age
        self.day = 1
        self.time = 7.0
        self.hunger = 55
        self.thirst = 45
        self.energy = 80
        self.happiness = 78
        self.cleanliness = 72
        self.health = 100
        self.bladder = 35
        self.social = 60
        self.stress = 20
        self.weight = 4.5
        self.helper_cooldown = 0
        self.location = "дом"
        self.alive = True
        self.sleeping = False
        self.mood = "спокойный"
        self.last_event = "Котик проснулся и потянулся."
        self.log = []

    def _record_event(self, message):
        self.last_event = message
        self.log.append({"day": self.day, "time": self._format_time(), "message": message})

    def _format_time(self):
        hour = int(self.time)
        minute = int((self.time - hour) * 60)
        return f"{hour:02d}:{minute:02d}"

    def _update_mood(self):
        if not self.alive:
            self.mood = "ушёл в мир иной"
            return

        if self.sleeping:
            self.mood = "спит"
            return

        if self.health < 35:
            self.mood = "болен"
        elif self.hunger > 80:
            self.mood = "голодный"
        elif self.thirst > 80:
            self.mood = "испытывает жажду"
        elif self.energy < 25:
            self.mood = "усталый"
        elif self.stress > 70:
            self.mood = "стрессовый"
        elif self.happiness > 80:
            self.mood = "счастливый"
        elif self.cleanliness < 25:
            self.mood = "грязный"
        else:
            self.mood = "спокойный"

    def _apply_random_event(self):
        if not self.alive:
            return

        roll = random.random()
        if roll < 0.12:
            self.happiness = clamp(self.happiness + 8)
            self._record_event(f"{self.name} внезапно начал играть с бумажным клубком.")
        elif roll < 0.24:
            self.stress = clamp(self.stress + 15)
            self.happiness = clamp(self.happiness - 5)
            self._record_event(f"{self.name} испугался громкого звука и спрятался под диван.")
        elif roll < 0.32:
            self.cleanliness = clamp(self.cleanliness - 12)
            self._record_event(f"{self.name} завалился в пыль и стал слегка грязным.")
        elif roll < 0.40:
            self.hunger = clamp(self.hunger + 6)
            self._record_event(f"{self.name} принялся шуршать по кухне и искать еду.")
        elif roll < 0.48:
            self.social = clamp(self.social + 10)
            self._record_event(f"{self.name} подошёл к человеку и настойчиво попросил внимания.")

    def feed(self, amount=20, food="корм"):
        if not self.alive:
            return f"{self.name} уже не может есть."

        self.hunger = clamp(self.hunger - amount)
        self.thirst = clamp(self.thirst + 8)
        self.energy = clamp(self.energy + 6)
        self.happiness = clamp(self.happiness + 12)
        self.health = clamp(self.health + 4)
        self.weight = round(self.weight + 0.08, 2)
        self._record_event(f"{self.name} съел {food} и удовлетворённо замурчал.")
        return self.last_event

    def drink(self, amount=15):
        if not self.alive:
            return f"{self.name} больше не может пить."

        self.thirst = clamp(self.thirst - amount)
        self.happiness = clamp(self.happiness + 4)
        self.health = clamp(self.health + 3)
        self._record_event(f"{self.name} подошёл к миске с водой и выпил.")
        return self.last_event

    def play(self, minutes=30):
        if not self.alive:
            return f"{self.name} уже не может играть."
        if self.energy < 18:
            return f"{self.name} слишком устал, чтобы бегать."

        self.energy = clamp(self.energy - 12)
        self.hunger = clamp(self.hunger + 9)
        self.thirst = clamp(self.thirst + 7)
        self.happiness = clamp(self.happiness + 18)
        self.cleanliness = clamp(self.cleanliness - 7)
        self.stress = clamp(self.stress - 6)
        self._record_event(f"{self.name} играл {minutes} минут и носился по квартире.")
        return self.last_event

    def sleep(self, hours=6):
        if not self.alive:
            return f"{self.name} уже спит навсегда."

        self.sleeping = True
        self.location = "кровать"
        self.energy = clamp(self.energy + 15 * hours)
        self.hunger = clamp(self.hunger + 3 * hours)
        self.thirst = clamp(self.thirst + 2 * hours)
        self.happiness = clamp(self.happiness + 4)
        self.stress = clamp(self.stress - 10)
        self._record_event(f"{self.name} поспал {format_hours(hours)} и хорошо отдохнул.")
        self.sleeping = False
        return self.last_event

    def helper_visit(self):
        if not self.alive:
            return f"{self.name} уже не может общаться."
        if self.helper_cooldown > 0:
            return f"Помощник сможет прийти через {format_hours(self.helper_cooldown)}."

        helpers = [
            ("Вася", ("принёс", "поставил", "налил", "проверил", "погладил", "убрал", "помог")),
            ("Марина", ("принесла", "поставила", "налила", "проверила", "погладила", "убрала", "помогла")),
            ("дядя Петя", ("принёс", "поставил", "налил", "проверил", "погладил", "убрал", "помог")),
            ("соседка", ("принесла", "поставила", "налила", "проверила", "погладила", "убрала", "помогла")),
            ("друг кота", ("принёс", "поставил", "налил", "проверил", "погладил", "убрал", "помог")),
        ]
        helper, verbs = random.choice(helpers)

        event = random.choice([
            f"{helper} {verbs[0]} свежий корм и {verbs[1]} миску рядом.",
            f"{helper} {verbs[2]} воды и {verbs[3]}, всё ли в порядке.",
            f"{helper} {verbs[4]} {self.name}, и тот очень обрадовался.",
            f"{helper} {verbs[5]} лоток и {verbs[6]} навести порядок в комнате.",
        ])

        self.happiness = clamp(self.happiness + 12)
        self.health = clamp(self.health + 5)
        self.cleanliness = clamp(self.cleanliness + 10)
        self.stress = clamp(self.stress - 8)
        self.helper_cooldown = 6
        self._record_event(event)
        return event

    def pet(self):
        if not self.alive:
            return f"{self.name} не чувствует ласки."

        self.happiness = clamp(self.happiness + 15)
        self.stress = clamp(self.stress - 10)
        self.social = clamp(self.social + 12)
        self.energy = clamp(self.energy - 3)
        self._record_event(f"{self.name} мурлычет и прижимается к руке.")
        return self.last_event

    def groom(self):
        if not self.alive:
            return f"{self.name} не может ухаживать за собой."

        self.cleanliness = clamp(self.cleanliness + 25)
        self.happiness = clamp(self.happiness + 8)
        self.health = clamp(self.health + 4)
        self._record_event(f"{self.name} тщательно вылизывается и становится чистым.")
        return self.last_event

    def use_litter(self):
        if not self.alive:
            return f"{self.name} больше не может ходить в лоток."

        self.bladder = clamp(self.bladder - 45)
        self.cleanliness = clamp(self.cleanliness + 18)
        self.happiness = clamp(self.happiness + 2)
        self._record_event(f"{self.name} воспользовался лотком и чувствует облегчение.")
        return self.last_event

    def explore(self):
        if not self.alive:
            return f"{self.name} уже не может гулять."

        self.location = random.choice(["балкон", "двор", "подоконник", "комната", "коридор"])
        self.happiness = clamp(self.happiness + 10)
        self.energy = clamp(self.energy - 7)
        self.hunger = clamp(self.hunger + 5)
        self.thirst = clamp(self.thirst + 5)
        self.stress = clamp(self.stress - 4)
        self._record_event(f"{self.name} осторожно исследует {self.location}.")
        return self.last_event

    def _natural_decay(self, hours):
        self.hunger = clamp(self.hunger + hours * 2.4)
        self.thirst = clamp(self.thirst + hours * 2.8)
        self.energy = clamp(self.energy - hours * 2.2)
        self.cleanliness = clamp(self.cleanliness - hours * 0.9)
        self.bladder = clamp(self.bladder + hours * 4.2)
        self.social = clamp(self.social - hours * 0.5)
        self.happiness = clamp(self.happiness - hours * 0.6)

        if self.time >= 22 or self.time < 6:
            self.energy = clamp(self.energy + hours * 1.8)

    def tick(self, hours=1):
        if not self.alive:
            return self.status()

        was_sleeping = self.sleeping
        self.time += hours
        while self.time >= 24:
            self.time -= 24
            self.day += 1
            self.age += 0.1
        self.helper_cooldown = max(0, self.helper_cooldown - hours)

        self.sleeping = self.time >= 23 or self.time < 7
        if was_sleeping and not self.sleeping:
            self._record_event(f"{self.name} проснулся и потянулся на солнце.")

        self._natural_decay(hours)

        if self.bladder >= 80:
            was_sleeping = self.sleeping
            self.sleeping = False
            self.location = "ищет лоток"
            self.stress = clamp(self.stress + 10)
            self.happiness = clamp(self.happiness - 7)
            if was_sleeping:
                self._record_event(f"{self.name} проснулся и нервно ищет лоток.")
            else:
                self._record_event(f"{self.name} нервно ищет лоток.")
        if self.hunger >= 85:
            self.health = clamp(self.health - 5)
        if self.thirst >= 85:
            self.health = clamp(self.health - 6)
        if self.cleanliness <= 20:
            self.health = clamp(self.health - 5)
        if self.energy <= 10:
            self.health = clamp(self.health - 6)
            self.happiness = clamp(self.happiness - 10)
        if self.stress >= 80:
            self.health = clamp(self.health - 3)

        if random.random() < 0.07 and self.health < 60:
            self._record_event(f"{self.name} внезапно закашлялся и выглядит плохо.")
            self.health = clamp(self.health - 8)

        self._update_mood()

        if self.health <= 0 or self.hunger >= 100 or self.thirst >= 100 or self.energy <= 0:
            self.alive = False
            self._record_event(f"{self.name} не выдержал нагрузки и ушёл из жизни.")
            self.mood = "ушёл в мир иной"

        return self.status()

    def simulate_day(self):
        if not self.alive:
            return self.status()

        self._record_event(f"{self.name} начинает день #{self.day}.")

        if self.hunger > 88:
            self.feed(14)
        if self.thirst > 88:
            self.drink(12)
        if self.bladder > 80:
            self.use_litter()

        if self.time >= 6 and self.time < 8:
            self._record_event(f"{self.name} потянулся, зевнул и осмотрел комнату.")
        elif self.time >= 8 and self.time < 11:
            if self.hunger > 75:
                self.feed(12)
            if self.thirst > 75:
                self.drink(10)
            if self.energy > 35:
                self.explore()
        elif self.time >= 11 and self.time < 15:
            if self.energy < 32:
                self.sleep(2)
            if self.energy > 40:
                self.play(20)
            if self.bladder > 70:
                self.use_litter()
        elif self.time >= 15 and self.time < 19:
            if self.cleanliness < 45:
                self.groom()
            if self.stress > 55:
                self.pet()
        elif self.time >= 19 and self.time < 22:
            if self.hunger > 80:
                self.feed(10)
            if self.thirst > 80:
                self.drink(10)
            if self.energy > 35:
                self.explore()
        else:
            if self.energy < 50:
                self.sleep(4)

        self._apply_random_event()

        self.tick(6)
        self._update_mood()
        return self.status()

    def status(self):
        self._update_mood()
        return {
            "name": self.name,
            "alive": self.alive,
            "day": self.day,
            "time": self._format_time(),
            "age": round(self.age, 1),
            "mood": self.mood,
            "hunger": round(self.hunger, 1),
            "thirst": round(self.thirst, 1),
            "energy": round(self.energy, 1),
            "happiness": round(self.happiness, 1),
            "cleanliness": round(self.cleanliness, 1),
            "health": round(self.health, 1),
            "bladder": round(self.bladder, 1),
            "stress": round(self.stress, 1),
            "weight": round(self.weight, 2),
            "helper_cooldown": self.helper_cooldown,
            "location": self.location,
            "last_event": self.last_event,
        }

    def __str__(self):
        data = self.status()
        return (
            f"{data['name']} | день: {data['day']} | время: {data['time']} | "
            f"возраст: {data['age']} | настроение: {data['mood']} | "
            f"голод: {data['hunger']} | жажда: {data['thirst']} | "
            f"энергия: {data['energy']} | счастье: {data['happiness']} | "
            f"чистота: {data['cleanliness']} | здоровье: {data['health']} | "
            f"стресс: {data['stress']}"
        )

    def to_dict(self):
        return {
            "name": self.name,
            "sex": self.sex,
            "age": self.age,
            "day": self.day,
            "time": self.time,
            "hunger": self.hunger,
            "thirst": self.thirst,
            "energy": self.energy,
            "happiness": self.happiness,
            "cleanliness": self.cleanliness,
            "health": self.health,
            "bladder": self.bladder,
            "social": self.social,
            "stress": self.stress,
            "weight": self.weight,
            "helper_cooldown": self.helper_cooldown,
            "location": self.location,
            "alive": self.alive,
            "mood": self.mood,
            "last_event": self.last_event,
            "log": self.log,
        }

    @classmethod
    def from_dict(cls, data):
        cat = cls(name=data.get("name", "Барсик"), age=data.get("age", 0.0), sex=data.get("sex", "male"))
        cat.day = data.get("day", 1)
        cat.time = data.get("time", 7.0)
        cat.hunger = data.get("hunger", 55)
        cat.thirst = data.get("thirst", 45)
        cat.energy = data.get("energy", 80)
        cat.happiness = data.get("happiness", 78)
        cat.cleanliness = data.get("cleanliness", 72)
        cat.health = data.get("health", 100)
        cat.bladder = data.get("bladder", 35)
        cat.social = data.get("social", 60)
        cat.stress = data.get("stress", 20)
        cat.weight = data.get("weight", 4.5)
        cat.helper_cooldown = data.get("helper_cooldown", 0)
        cat.location = data.get("location", "дом")
        cat.alive = data.get("alive", True)
        cat.mood = data.get("mood", "спокойный")
        cat.last_event = data.get("last_event", "Котик проснулся и потянулся.")
        cat.log = data.get("log", [])
        return cat

    def save_state(self, path=SAVE_FILE):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, ensure_ascii=False, indent=2)
        return path

    @classmethod
    def load_state(cls, path=SAVE_FILE):
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return cls.from_dict(data)

    def render_ascii(self):
        if not self.alive:
            return """
           ___
        ( X_X )
         /|\\
         / \\
        """

        if self.sleeping:
            return """
             ___
           ( - - )
            |  |  
            / \\
           z z
            """

        mood = self.mood.lower()
        if "счаст" in mood or "спокой" in mood:
            face = "( ^.^ )"
        elif "голод" in mood or "бол" in mood or "устал" in mood:
            face = "( -.- )"
        elif "стресс" in mood or "гряз" in mood:
            face = "( o.o )"
        else:
            face = "( ^_~ )"

        return f"""
         /\\_/\\
        ({face})
         /| |\\
         / \\
        """

    def show(self):
        print(self.render_ascii())
        print(self)
        print(f"Последнее событие: {self.last_event}")


class TamagotchiGame:
    """Управляет меню, действиями игрока и сохранением питомца."""

    def __init__(self, save_file=SAVE_FILE):
        self.save_file = save_file
        self.cat = None

    def create_new_cat(self):
        name = input("Как назовём котика? ").strip()
        if not name:
            name = "Барсик"
            print(f"Пустое имя, поэтому котика назовём {name}.")
        self.cat = Cat(name)

    def restart_game(self):
        self.create_new_cat()
        self.cat.save_state(self.save_file)
        print(f"Новая игра началась! Знакомься, это {self.cat.name}.")

    def load_or_create_cat(self):
        saved_cat = Cat.load_state(self.save_file)
        if saved_cat is None:
            print("Сохранение не найдено. Начинаем новую игру!")
            self.create_new_cat()
            return

        while True:
            answer = input("Найдено сохранение. Загрузить его? (Д/н, Enter — загрузить): ").strip().lower()
            if answer in ("", "д", "да", "y", "yes"):
                self.cat = saved_cat
                print("Сохранение загружено.")
                return
            if answer in ("н", "нет", "n", "no"):
                self.create_new_cat()
                print("Начинаем новую игру.")
                return
            print("Введи «д» для загрузки или «н» для новой игры.")

    def show_menu(self):
        self.cat.show()
        print("\nВыбери действие:")
        if self.cat.sleeping:
            print("Котик спит и пока не может выполнять действия.")
            print("7. Подождать час")
            print("11. Подождать до пробуждения")
            print("10. Начать заново")
            print("0. Выйти и сохранить")
            return

        print("1. Покормить")
        print("2. Напоить")
        print("3. Погладить")
        print("4. Поиграть")
        print("5. Уложить спать")
        print("6. Почистить")
        print("7. Подождать час")
        if self.cat.helper_cooldown > 0:
            print(f"8. Помощник будет доступен через {format_hours(self.cat.helper_cooldown)}")
        else:
            print("8. Позвать помощника")
        print("9. Отвести кота к лотку")
        print("10. Начать заново")
        print("11. Подождать до пробуждения")
        print("0. Выйти и сохранить")

    def wait_until_awake(self):
        if not self.cat.sleeping:
            return f"{self.cat.name} уже бодрствует."

        elapsed_hours = 0
        while self.cat.alive and self.cat.sleeping:
            self.cat.tick(1)
            elapsed_hours += 1

        if not self.cat.alive:
            return f"{self.cat.name} умер во время сна."
        return f"Сон пропущен. {self.cat.name} проснулся через {format_hours(elapsed_hours)}."

    def perform_action(self, choice):
        if self.cat.sleeping and choice not in ("7", "10", "11", "0"):
            print("Котик спит. Подожди, пока он проснётся.")
            return False
        if choice == "8" and self.cat.helper_cooldown > 0:
            print(self.cat.helper_visit())
            return False

        actions = {
            "1": lambda: self.cat.feed(18),
            "2": lambda: self.cat.drink(12),
            "3": self.cat.pet,
            "4": lambda: self.cat.play(20),
            "5": lambda: self.cat.sleep(3),
            "6": self.cat.groom,
            "7": lambda: "Прошёл час.",
            "8": self.cat.helper_visit,
            "9": self.cat.use_litter,
            "11": self.wait_until_awake,
        }

        if choice not in actions:
            print("Неверный ввод. Попробуй ещё раз.\n")
            return False

        print(actions[choice]())
        if choice == "8":
            print("Помощник пришёл и помог котику.")

        if choice != "11":
            self.cat.tick(1)
        self.cat.save_state(self.save_file)
        if not self.cat.alive:
            print("\nКотик умер. Игра окончена.")
        return True

    def run(self):
        print("\n=== Кот-Тамагочи ===")
        print("Сохранение обновляется после каждого действия.\n")
        try:
            self.load_or_create_cat()

            if not self.cat.alive:
                self.cat.show()
                print("В сохранении котик уже умер.")
                print("1. Начать новую игру")
                print("0. Выйти, не меняя сохранение")
                while True:
                    choice = input("Твой выбор: ").strip()
                    if choice == "1":
                        self.restart_game()
                        break
                    if choice == "0":
                        print("Игра завершена. Старое сохранение оставлено без изменений.")
                        return
                    print("Выбери 1, чтобы начать заново, или 0, чтобы выйти.")

            while self.cat.alive:
                self.show_menu()
                choice = input("\nТвой выбор: ").strip()

                if choice == "10":
                    answer = input("Начать новую игру и заменить это сохранение? (д/н): ").strip().lower()
                    if answer in ("д", "да", "y", "yes"):
                        self.restart_game()
                    continue

                if choice == "0":
                    self.cat.save_state(self.save_file)
                    print("Игра сохранена. Возвращайся скорей!")
                    return

                if self.perform_action(choice):
                    print("\n--- Прошёл час ---\n")

            self.cat.save_state(self.save_file)
        except KeyboardInterrupt:
            if self.cat is not None:
                self.cat.save_state(self.save_file)
                print("\nИгра остановлена. Прогресс сохранён.")
            else:
                print("\nЗапуск отменён. Существующее сохранение не изменено.")


def run_tamagotchi():
    game = TamagotchiGame()
    game.run()


if __name__ == "__main__":
    run_tamagotchi()
