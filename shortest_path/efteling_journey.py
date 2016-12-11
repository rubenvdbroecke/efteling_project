import matplotlib.pyplot as plt
from project_managament.eftel_data_filename import file_path

a_s = ['Entrance', 'Pirana', 'JorisendeDraak', 'Python', 'DeVliegendeHollander', 'Baron1898',
       'CarnavalFestival', 'Stoomcarrousel']


def generate_journey(attraction_sequence):
    image_name = file_path + 'efteling_map.png'

    im = plt.imread(image_name)
    implot = plt.imshow(im)

    attraction_coordinates = [{'Entrance': {'x': 402,
                                            'y': 816},
                               'Pirana': {'x': 780,
                                          'y': 495},
                               'JorisendeDraak': {'x': 844,
                                                  'y': 245},
                               'Python': {'x': 824,
                                          'y': 201},
                               'DeVliegendeHollander': {'x': 756,
                                                        'y': 266},
                               'Baron1898': {'x': 691,
                                             'y': 361},
                               'CarnavalFestival': {'x': 236,
                                                    'y': 170},
                               'Stoomcarrousel': {'x': 326,
                                                  'y': 424},
                               'FataMorgana': {'x': 753,
                                               'y': 738},
                               'Kleuterhof': {'x': 316,
                                              'y': 84},
                               'VogelRok': {'x': 265,
                                            'y': 147},
                               'VillaVolta': {'x': 77,
                                              'y': 492},
                               'Bobbaan': {'x': 650,
                                           'y': 592},
                               'HalveMaen': {'x': 649,
                                             'y': 162},
                               'OudeTuffer': {'x': 603,
                                              'y': 121},
                               'Pandadroom': {'x': 567,
                                              'y': 630},
                               'Droomvlucht': {'x': 135,
                                               'y': 604}}]

    x = []
    y = []
    for a in attraction_sequence:
        for b in attraction_coordinates:
            x.append(b[a]['x'])
            y.append(b[a]['y'])

    plt.plot(x, y, marker='o', markersize=7, linestyle='--', color='r', linewidth=2.5, label='Route')
    plt.xlabel('Radius/Side')
    plt.ylabel('Area')
    plt.axis('off')
    plt.title('Your Efteling Journey')
    plt.legend()
    plt.show()


# generate_journey(a_s)