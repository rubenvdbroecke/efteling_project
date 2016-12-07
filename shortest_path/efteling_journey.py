import matplotlib.pyplot as plt
import matplotlib.pylab as plb

# a_s = ['Entrance', 'Pirana', 'JorisendeDraak', 'Python', 'DeVliegendeHollander', 'Baron1898',
#                        'CarnavalFestival', 'Stoomcarrousel', 'Droomvlucht']


def generate_journey(attraction_sequence):
    image_name = 'C:\\Users\\vande\\Desktop\\efteling_map.png'

    im = plt.imread(image_name)
    implot = plt.imshow(im)

    attraction_coordinates = [{'Entrance': {'x': 402, 'y': 816},
                               'Pirana': {'x': 780, 'y': 495},
                               'JorisendeDraak': {'x': 844, 'y': 245},
                               'Python': {'x': 824, 'y': 201},
                               'DeVliegendeHollander': {'x': 756, 'y': 266},
                               'Baron1898': {'x': 691, 'y': 361},
                               'CarnavalFestival': {'x': 236, 'y': 170},
                               'Stoomcarrousel': {'x': 326, 'y': 424},
                               'Droomvlucht': {'x': 135, 'y': 604}}]
    x = []
    y = []
    for a in attraction_sequence:
        for b in attraction_coordinates:
            x.append(b[a]['x'])
            y.append(b[a]['y'])

    plt.plot(x, y, marker='o', linestyle='--', color='r', linewidth=3, label='Route')
    plt.xlabel('Radius/Side')
    plt.ylabel('Area')
    plt.axis('off')
    plt.title('Your Efteling Journey')
    plt.legend()
    plt.show()
