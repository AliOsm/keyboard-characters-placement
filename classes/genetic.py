import os
import copy
import time
import math
import numpy as np

from helpers import *

class Genetic:
    def __init__(
        self,
        number_of_generations,
        number_of_characters_placements,
        number_of_accepted_characters_placements,
        number_of_randomly_injected_characters_placements,
        number_of_mutation_operations,
        corpus_path,
        searching_corpus_size,
        testing_corpus_size,
        maximum_line_length,
        keyboard_structure,
        initial_characters_placement
    ):
        self.number_of_generations = number_of_generations
        self.number_of_characters_placements = number_of_characters_placements
        self.number_of_accepted_characters_placements = number_of_accepted_characters_placements
        self.number_of_randomly_injected_characters_placements = number_of_randomly_injected_characters_placements
        self.number_of_mutation_operations = number_of_mutation_operations
        self.keyboard_structure = keyboard_structure
        self.initial_characters_placement = initial_characters_placement

        self.corpus = open(corpus_path, 'r').read().split('\n')
        np.random.shuffle(self.corpus)

        i = 0

        self.searching_corpus = list()
        while i < len(self.corpus):
            if len(self.searching_corpus) >= searching_corpus_size:
                break

            line = self._preprocess_line(self.corpus[i])
            i += 1

            if len(line) > maximum_line_length:
                continue

            self.searching_corpus.append(line)

        if len(self.searching_corpus) < searching_corpus_size:
            warning_log('Searching corpus size didn\'t reach %s, its current size is %s' %
                (searching_corpus_size, len(self.searching_corpus)))

        self.testing_corpus = list()
        while i < len(self.corpus):
            if len(self.testing_corpus) >= testing_corpus_size:
                break

            line = self._preprocess_line(self.corpus[i])
            i += 1

            if len(line) > maximum_line_length:
                continue

            self.testing_corpus.append(line)

        if len(self.testing_corpus) < testing_corpus_size:
            warning_log('Testing corpus size didn\'t reach %s, its current size is %s' %
                (testing_corpus_size, len(self.testing_corpus)))

        self.characters_placements = list()
        for _ in range(self.number_of_characters_placements):
            self.characters_placements.append(copy.deepcopy(self.initial_characters_placement))
            self.characters_placements[-1].randomize()

        self.time = -1

    def start(self):
        start_time = time.time()

        for generation in range(self.number_of_generations):
            info_log('Start generation number %s' % (generation + 1))

            info_log('Calculate fitness function for each characters placement')
            self.best_characters_placement = self.calculate_fitness_for_characters_placements()
            info_log('Best characters placement fitness value: %s' % self.best_characters_placement.fitness)

            info_log('Start natural selection and crossover')
            self.natural_selection_and_crossover()

            info_log('Start random injection')
            self.random_injection()

            info_log('Start mutating characters placements')
            self.mutate_characters_placements()

        self.time = round((time.time() - start_time) / 60, 2)
        info_log('Time taken for genetic algorithm is %s minutes' % (self.time))

    def calculate_fitness_for_characters_placements(self):
        best_fitness_value = 1e18
        best_characters_placement = None
        for i, characters_placement in enumerate(self.characters_placements):
            print('Calculating fitness function for characters placement #%s' % (i + 1), end='\r')
            characters_placement.calculate_fitness(self.keyboard_structure, self.searching_corpus)
            if characters_placement.fitness < best_fitness_value:
                best_fitness_value = characters_placement.fitness
                best_characters_placement = characters_placement
        return best_characters_placement

    def natural_selection_and_crossover(self):
        self.characters_placements = list(sorted(self.characters_placements, key=lambda characters_placement: characters_placement.fitness))

        temp_characters_placements = list()
        for i in range(self.number_of_accepted_characters_placements):
            temp_characters_placements.append(copy.deepcopy(self.characters_placements[i]))

        while len(temp_characters_placements) < self.number_of_characters_placements - self.number_of_randomly_injected_characters_placements:
            a, b = np.random.beta(a=0.5, b=2, size=2)

            a = math.floor(a * self.number_of_characters_placements)
            b = math.floor(b * self.number_of_characters_placements)

            assert(a != self.number_of_characters_placements)
            assert(b != self.number_of_characters_placements)

            temp_characters_placements.append(self._crossover(
                self.characters_placements[a],
                self.characters_placements[b]
            ))

            if len(temp_characters_placements) >= self.number_of_characters_placements - self.number_of_randomly_injected_characters_placements:
                break

            temp_characters_placements.append(self._crossover(
                self.characters_placements[b],
                self.characters_placements[a]
            ))

        self.characters_placements = temp_characters_placements

    def random_injection(self):
        for _ in range(self.number_of_randomly_injected_characters_placements):
            random_characters_placement = copy.deepcopy(self.characters_placements[0])
            random_characters_placement.randomize()
            self.characters_placements.append(random_characters_placement)

    def mutate_characters_placements(self):
        for characters_placement in self.characters_placements[self.number_of_accepted_characters_placements:]:
            characters_placement.mutate(self.number_of_mutation_operations)

    def save_searching_and_testing_corpus(self, dirpath):
        with open(os.path.join(dirpath, 'searching_corpus'), 'w') as file:
            file.write('\n'.join(self.searching_corpus))

        with open(os.path.join(dirpath, 'testing_corpus'), 'w') as file:
            file.write('\n'.join(self.testing_corpus))

    def _preprocess_line(self, line):
        return ''.join([character for character in line \
            if character in self.initial_characters_placement])

    def _crossover(self, a, b):
        new_characters_placement = copy.deepcopy(a)

        chosen_characters = list()
        for character in new_characters_placement.characters_set:
            if character.button_id != None or np.random.rand() >= 0.5:
                chosen_characters.append(character)

        needed_characters = list()
        for character in b.characters_set:
            if character not in chosen_characters:
                needed_characters.append(character)

        j = 0
        for i in range(len(new_characters_placement.characters_set)):
            if new_characters_placement.characters_set[i] in chosen_characters:
                continue

            new_characters_placement.characters_set[i] = copy.deepcopy(needed_characters[j])
            j += 1

        return new_characters_placement
