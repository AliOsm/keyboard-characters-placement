import os
import json
import argparse

from helpers import *
from classes.keyboard_structure import KeyboardStructure
from classes.characters_placement import CharactersPlacement
from classes.genetic import Genetic

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--genetic-config', default='genetic_config.json')
  args = parser.parse_args()

  info_log('Load genetic config file: %s' % args.genetic_config)
  with open(args.genetic_config, 'r') as file:
  	genetic_config = json.load(file)

  info_log('Construct keyboard structure')
  keyboard_structure = KeyboardStructure(
  	name=genetic_config['keyboard_structure']['name'],
  	width=genetic_config['keyboard_structure']['width'],
  	height=genetic_config['keyboard_structure']['height'],
  	buttons=genetic_config['keyboard_structure']['buttons'],
  	hands=genetic_config['hands']
  )

  info_log('Construct initial characters placement')
  initial_characters_placement = CharactersPlacement(characters_set=genetic_config['characters_set'])

  info_log('Start genetic algorithm')

  genetic = Genetic(
    genetic_config['number_of_generations'],
    genetic_config['number_of_characters_placements'],
    genetic_config['number_of_accepted_characters_placements'],
    genetic_config['number_of_mutation_operations'],
    genetic_config['searching_corpus_path'],
    genetic_config['searching_corpus_size'],
    genetic_config['maximum_line_length'],
    keyboard_structure,
    initial_characters_placement
  )
  genetic.start()
  genetic.save_searching_corpus(os.path.dirname(args.genetic_config))

  info_log('Visualize best characters placement found by genetic algorithm')
  keyboard_structure.visualize(
    dirpath=os.path.dirname(args.genetic_config),
    characters_placement=genetic.best_characters_placement,
    save=True
  )
