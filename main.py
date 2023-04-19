from PIL import Image, ImageDraw, ImageFont
from collections import deque
import random


def main():
    # Open the txt file
    with open('emploi_du_temps.txt', 'r') as f:
        file = f.readlines()
    data = extract_data(file)

    # Init the image
    img = Image.new('RGB', (900, 720), color='white')
    font = ImageFont.truetype("font/Classica-Bold.ttf", 10)
    draw = ImageDraw.Draw(img)

    # Draw time grid
    draw_time_grid(draw, font)

    # Draw datas
    color_not_used = ["grey", "blue", "orange", "yellow", "red", "purple", "pink", "green"]
    uvs_color = {}
    for data in data:
        draw_data_box(color_not_used, data, draw, font, uvs_color)

    # Draw the final grid and the header
    draw_day_box(draw, font)

    # Display the image
    img.show()

# This function extracts the data from the txt file
def extract_data(lines):
    tab = []
    type_key = {
        'C': 'Cours',
        'D': 'TD',
        'T': 'TP',
    }
    for line in lines:
        line = line.strip().split()
        if line:
            nom = line[0]
            type = type_key[line[1]]
            numero = line[2]
            decalage = 0
            semaine = 'all'
            if len(line[3]) == 1:
                semaine = line[3]
                decalage = 1
            jour = line[3 + decalage]
            autre = line[4 + decalage].split(",")
            horaire = autre[0]
            salle = autre[2].strip("S=")
            tab.append({
                'nom': nom,
                'type': type,
                'numero': numero,
                'semaine': semaine,
                'jour': jour,
                'horaire': horaire,
                'salle': salle,
            })
    return tab


# This function increases the time that we display on the left of the schedule
def increase_time(time):
    time = time.split('h')
    hour = str(int(time[0]) + 1)  # Increasing of one hour
    return f"{hour}h00"


# This function draws the column and the title of each day
def draw_day_box(draw, font):
    jour = deque(["Lundi", "Mardi", "Mercredi", "jeudi", "Vendredi"])
    for i in range(100, 701, 150):
        draw.rectangle(((i, 20), (i + 150, 50)), fill="lightgrey", outline="black")  # Draw the box for name of the day
        draw.text((i + 75 - (len(jour[0]) * 2), 30),  # Write the day header
                  jour.popleft(),
                  (0, 0, 0),
                  font=font)
        draw.rectangle(((i, 50), (i + 150, 710)), outline="black")  # Draw the day box


# This function draws the box of on specific course
def draw_data_box(color_not_used, data, draw, font, uvs_color):
    if f"{data['nom']}" not in uvs_color:  # Check if the color has been defined
        define_color(color_not_used, data, uvs_color)
    column_start, column_end = convert_day_to_column(data)  # Find the column
    row_start, row_end = convert_time_to_row(data["horaire"])  # Find the row
    draw_box(column_end, column_start, data, draw, row_end, row_start, uvs_color)  # Draw the box of the course
    draw_text(column_end, column_start, data, draw, font, row_end, row_start)  # Write the text of the course


# This function draws the time grid and write the time for each hour to make it easier to read
def draw_time_grid(draw, font):
    time = "8h00"   # Initial time of the schedule
    display_time = True
    for i in range(50, 681, 30):
        if display_time:    # We display hour only on the hours
            draw.text((60, i - 5),
                      time,
                      (0, 0, 0),
                      font=font)
            display_time = False
            time = increase_time(time)
        else:
            display_time = True
        for j in range(90, 850, 10):    # Let's draw lines to make it easier to read
            draw.line(((j, i), (j + 5, i)), fill="lightgrey")


# This function defines a color for a new subject by choosing a random one in the implemented list
def define_color(color_not_used, data, uvs_color):
    i = random.randint(0, len(color_not_used) - 1)
    uvs_color[f"{data['nom']}"] = color_not_used[i]    # Save the color chosen for this subject
    color_not_used.pop(i)   # Delete it from the available colors


# This function draws a box with specified information about column and row
def draw_box(column_end, column_start, data, draw, row_end, row_start, uvs_color):
    square_coords = ((column_start, row_start), (column_end, row_end))
    draw.rectangle(square_coords, fill=uvs_color[data["nom"]], outline="black")


# This function write a text with specified information about column and row
def draw_text(column_end, column_start, data, draw, font, row_end, row_start):
    draw.text((((column_start + column_end) / 2 - (len(data["nom"] * 2))),
               (row_start + row_end) / 2 - 15), data["nom"],
              (0, 0, 0),
              font=font)
    draw.text((((column_start + column_end) / 2 - (len(data["salle"] * 2))),
               (row_start + row_end) / 2 - 5),
              data["salle"],
              (0, 0, 0),
              font=font)
    draw.text((((column_start + column_end) / 2 - (len(data["type"] * 2))),
               (row_start + row_end) / 2 + 5),
              data["type"],
              (0, 0, 0),
              font=font)


# This functions converts a day into a column and allows to know in which column we need to display a course
def convert_day_to_column(data):
    if data['jour'] == "LUNDI...":
        column_start = 100
    elif data['jour'] == "MARDI...":
        column_start = 250
    elif data['jour'] == "MERCREDI":
        column_start = 400
    elif data['jour'] == "JEUDI...":
        column_start = 550
    else:
        column_start = 700
    column_end = column_start + 150
    if data['semaine'] == 'A':
        column_start += 75
    elif data['semaine'] == 'B':
        column_end -= 75
    return column_start, column_end


# This functions converts a time into a row and allows to know in which row we need to display a course
def convert_time_to_row(horaire):
    debut, fin = horaire.split('-')
    debut = debut.split(":")
    debut = (int(debut[0]) * 60 + int(debut[1])) - (8 * 60) + 50
    fin = fin.split(":")
    fin = (int(fin[0]) * 60 + int(fin[1])) - (8 * 60) + 50
    return debut, fin


if __name__ == '__main__':
    main()
