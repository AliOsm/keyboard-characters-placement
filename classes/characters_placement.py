import numpy as np

from helpers import *
from classes.character import Character

class CharactersPlacement:
    def __init__(self, characters_set):
        self.fitness = -1
        self.characters_set = list()
        for character in characters_set:
            self.characters_set.append(Character(
                character=character['character'],
                button_id=character['button_id']
            ))
        self._order_fixed_characters()

    def randomize(self):
        np.random.shuffle(self.characters_set)
        self._order_fixed_characters()

    def calculate_fitness(self, keyboard_structure, searching_corpus):
        fitness = 0
        for line in searching_corpus:
            for character in line:
                button_id = self._order_of_character(character)

                if button_id == -1:
                    warning_log('Found unrecognized character \'%s\'' % character)
                    continue

                fitness += keyboard_structure.smallest_distance_from_button_to_finger(button_id)
            keyboard_structure.reset_fingers_locations()
        self.fitness = round(fitness, 2)
        return self.fitness

    def mutate(self, number_of_mutation_operations):
        for _ in range(number_of_mutation_operations):
            i = self._non_fixed_random_character()
            j = self._non_fixed_random_character()
            self.characters_set[i], self.characters_set[j] = self.characters_set[j], self.characters_set[i]

    def _order_fixed_characters(self):
        fixed_characters = list()

        for i in range(len(self.characters_set)):
            if self.characters_set[i].button_id != None:
                fixed_characters.append(self.characters_set[i])
        self.characters_set = [character for character in self.characters_set \
            if character.button_id == None]

        fixed_characters = list(sorted(fixed_characters, key=lambda character: character.button_id))

        for character in fixed_characters:
            self.characters_set.insert(character.button_id - 1, character)

    def _order_of_character(self, character):
        for i in range(len(self.characters_set)):
            if character == self.characters_set[i].character:
                return i
        return -1

    def _non_fixed_random_character(self):
        rand = np.random.randint(0, len(self.characters_set) - 1)
        while self.characters_set[rand].button_id != None:
            rand = np.random.randint(0, len(self.characters_set) - 1)
        return rand

    def __getitem__(self, idx):
        return self.characters_set[idx].character
