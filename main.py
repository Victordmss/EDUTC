from PIL import Image, ImageDraw


def main():
    with open('emploi_du_temps.txt', 'r') as f:
        file = f.readlines()
    data = extract_data(file)
    # Initialiser l'image
    img = Image.new('RGB', (1000, 12 * 60), color='white')
    draw = ImageDraw.Draw(img)

    # Dessin des données
    for data in data:
        if data['jour'] == "LUNDI...":
            col = 100
        elif data['jour'] == "MARDI...":
            col = 210
        elif data['jour'] == "MERCREDI":
            col = 320
        elif data['jour'] == "JEUDI...":
            col = 430
        else:
            col = 540
        print(col)
        debut, fin = data['horaire'].split('-')
        debut = debut.split(":")
        debut = (int(debut[0]) * 60 + int(debut[1])) - (8 * 60)
        fin = fin.split(":")
        fin = (int(fin[0]) * 60 + int(fin[1])) - (8 * 60)
        square_coords = ((col, debut), (col+100, fin))
        draw.rectangle(square_coords, fill='red')

    # Affichage et sauvegarde de l'image
    img.show()


def extract_data(lines):
    tab = []
    for line in lines:
        line = line.strip().split()
        if line:
            matiere = line[0]
            type = line[1]
            numero = line[2]
            decalage = 0
            semaine = 'all'
            if len(line[3]) == 1:
                semaine = line[3]
                decalage = 1
            jour = line[3 + decalage]
            autre = line[4 + decalage].split(",")
            horaire = autre[0]
            salle = autre[2]
            tab.append({
                'matiere': matiere,
                'type': type,
                'numero': numero,
                'semaine': semaine,
                'jour': jour,
                'horaire': horaire,
                'salle': salle,
            })
    return tab


if __name__ == '__main__':
    main()
