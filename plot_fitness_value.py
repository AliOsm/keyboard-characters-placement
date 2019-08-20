import matplotlib.pyplot as plt

def fitness_values_extractor(logs_file_path):
    with open(logs_file_path, 'r') as file:
        lines = file.readlines()

    fitness_values = list()
    for line in lines:
        if 'fitness value' in line.lower():
            fitness_values.append(float(line.split(': ')[-1]))
    fitness_values = fitness_values[:-1]

    fitness_values = [fitness_value for i, fitness_value in enumerate(fitness_values) \
                        if i == 0 or (i + 1) % 5 == 0]

    return fitness_values

if __name__ == '__main__':
    searches_to_plot = [
        {
            'display_name': 'Letters Only',
            'logs_file_path': 'searched_characters_placements/letters_only_dir/logs',
            'marker': 'o'
        },
        {
            'display_name': 'Letters and Punctuations',
            'logs_file_path': 'searched_characters_placements/letters_and_punctuations_dir/logs',
            'marker': 's'
        },
        {
            'display_name': 'Letters Only - Left Handed',
            'logs_file_path': 'searched_characters_placements/letters_only_left_handed_dir/logs',
            'marker': 'D'
        },
        {
            'display_name': 'Letters Only - Right Handed',
            'logs_file_path': 'searched_characters_placements/letters_only_right_handed_dir/logs',
            'marker': 'p'
        },
    ]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.xlabel('Generation Number', fontsize=20)
    plt.ylabel('Fitness Value', fontsize=20)

    for search_to_plot in searches_to_plot:
        fitness_values = fitness_values_extractor(search_to_plot['logs_file_path'])
        ax.plot(
            [1] + [i for i in range(5, 101, 5)],
            fitness_values,
            label=search_to_plot['display_name'],
            marker=search_to_plot['marker'],
            markersize=8,
            linewidth=2
        )

    plt.xticks([1] + [i for i in range(5, 101, 5)])
    # plt.yticks([])

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    plt.legend(fontsize=20)
    plt.show()
