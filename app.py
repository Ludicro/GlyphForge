import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageTk
import numpy as np
import GlyphEngine.writer as writer
import GlyphEngine.bases as bases
import GlyphEngine.line_shapes as line_shapes
import random
import json

class SpellApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Spell Generator")
        self.current_image = None

        # Load attributes
        with open("GlyphEngine/attributes.json", "r") as f:
            attributes = json.load(f)
            self.levels = attributes["levels"]
            self.schools = attributes["schools"] 
            self.durations = attributes["durations"]
            self.ranges = attributes["ranges"]
            self.areas = attributes["area_types"]
            self.dtypes = attributes["damage_types"]
            self.conditions = attributes["conditions"]
         


        # Create dropdowns
        self.create_dropdowns()

        # Create frame for buttons
        button_frame = ttk.Frame(master)
        button_frame.pack()

        # Button to generate spell
        self.generate_button = tk.Button(button_frame, text="Generate Glyph", command=self.generate_spell)
        self.generate_button.pack(side=tk.LEFT, padx=5)

        # Button to randomly generate spell
        self.random_button = tk.Button(button_frame, text="Random Spell", command=self.random_spell)
        self.random_button.pack(side=tk.LEFT, padx=5)

        # Button to download the image
        self.download_button = tk.Button(button_frame, text="Download Glyph", command=self.download_image)
        self.download_button.pack(side=tk.LEFT, padx=5)

        # Label to display the image
        self.image_label = tk.Label(master)
        self.image_label.pack()

        # Create label for spell name
        self.spell_name_label = tk.Label(master, text="")
        self.spell_name_label.pack()



    def create_dropdowns(self):
        self.level_var = tk.StringVar()
        self.school_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.range_var = tk.StringVar()
        self.area_var = tk.StringVar()
        self.dtype_var = tk.StringVar()
        self.condition_var = tk.StringVar()
        self.concentration_var = tk.StringVar()
        self.ritual_var = tk.StringVar()
        self.shape_var = tk.StringVar()
        self.lineType_var = tk.StringVar()

        # Create frames for organizing dropdowns
        top_frame = ttk.Frame(self.master)
        top_frame.pack()
        bottom_frame = ttk.Frame(self.master)
        bottom_frame.pack()

        # Level dropdown
        ttk.Label(top_frame, text="Select Level:").grid(row=0, column=0)
        level_dropdown = ttk.Combobox(top_frame, textvariable=self.level_var, values=self.levels)
        level_dropdown.grid(row=1, column=0, padx=5)

        # School dropdown
        ttk.Label(top_frame, text="Select School:").grid(row=0, column=1)
        school_dropdown = ttk.Combobox(top_frame, textvariable=self.school_var, values=self.schools)
        school_dropdown.grid(row=1, column=1, padx=5)

        # Duration dropdown
        ttk.Label(top_frame, text="Select Duration:").grid(row=0, column=2)
        duration_dropdown = ttk.Combobox(top_frame, textvariable=self.duration_var, values=self.durations)
        duration_dropdown.grid(row=1, column=2, padx=5)

        # Range dropdown
        ttk.Label(top_frame, text="Select Range:").grid(row=0, column=3)
        range_dropdown = ttk.Combobox(top_frame, textvariable=self.range_var, values=self.ranges)
        range_dropdown.grid(row=1, column=3, padx=5)

        # Area dropdown
        ttk.Label(top_frame, text="Select Area Type:").grid(row=0, column=4)
        area_dropdown = ttk.Combobox(top_frame, textvariable=self.area_var, values=self.areas)
        area_dropdown.grid(row=1, column=4, padx=5)

        # Damage Type dropdown
        ttk.Label(top_frame, text="Select Damage Type:").grid(row=0, column=5)
        dtype_dropdown = ttk.Combobox(top_frame, textvariable=self.dtype_var, values=self.dtypes)
        dtype_dropdown.grid(row=1, column=5, padx=5)

        # Condition dropdown
        ttk.Label(top_frame, text="Select Conditions:").grid(row=0, column=6)
        condition_dropdown = ttk.Combobox(top_frame, textvariable=self.condition_var, values=self.conditions)
        condition_dropdown.grid(row=1, column=6, padx=5)

        # Concentration dropdown
        ttk.Label(bottom_frame, text="Concentration:").grid(row=0, column=0)
        concentration_dropdown = ttk.Combobox(bottom_frame, textvariable=self.concentration_var, values=["Yes", "No"])
        concentration_dropdown.grid(row=1, column=0, padx=5)

        # Ritual dropdown
        ttk.Label(bottom_frame, text="Ritual:").grid(row=0, column=1)
        ritual_dropdown = ttk.Combobox(bottom_frame, textvariable=self.ritual_var, values=["Yes", "No"])
        ritual_dropdown.grid(row=1, column=1, padx=5)

        # Shape Dropdown
        ttk.Label(bottom_frame, text="Select Shape:").grid(row=0, column=2)
        shape_dropdown = ttk.Combobox(bottom_frame, textvariable=self.shape_var, values=["Polygon", "Quadratic", "Circle", "Cubic", "Golden"])
        shape_dropdown.grid(row=1, column=2, padx=5)

        # Line Type Dropdown
        ttk.Label(bottom_frame, text="Select Line Type:").grid(row=0, column=3)
        lineType_dropdown = ttk.Combobox(bottom_frame, textvariable=self.lineType_var, values=["Straight", "Centre Circle"])
        lineType_dropdown.grid(row=1, column=3, padx=5)


        # Set default values
        self.level_var.set("None")
        self.school_var.set("None")
        self.duration_var.set("Instantaneous")
        self.range_var.set("None")
        self.area_var.set("None")
        self.dtype_var.set("None")
        self.condition_var.set("None")
        self.concentration_var.set("No")
        self.ritual_var.set("No")
        self.shape_var.set("Polygon")
        self.lineType_var.set("Straight")

        
    def load_attributes(self, filename):
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines()]

    def generate_spell(self):
        # Get the user inputs for each field
        level = self.level_var.get()
        school = self.school_var.get()
        duration = self.duration_var.get()
        rang = self.range_var.get()
        area = self.area_var.get()
        dtype = self.dtype_var.get()
        condition = self.condition_var.get()
        concentration = self.concentration_var.get()
        ritual = self.ritual_var.get()
        shape = self.shape_var.get()
        lineType = self.lineType_var.get()

        # Set default inputs - had to do it this way cause the results get passed in anyway
        if level == '':
            level = "None"
        if school == '':
            school = "None"
        if duration == '':
            duration = "Instantaneous"
        if rang == '':
            rang = "None"
        if area == '':
            area = "None"
        if dtype == '':
            dtype = "None"
        # Add this line to define include_conditions
        include_conditions = bool(condition and condition != 'None')
        if concentration == '':
            concentration = "No"
        if ritual == '':
            ritual = "No"

        # Set the shape given by the user to the respective class object
        match shape:
            case "Polygon":
                shape = bases.polygon
            case "Line":
                shape = bases.line
            case "Quadratic":
                shape = bases.quadratic
            case "Circle":
                shape = bases.circle
            case "Cubic":
                shape = bases.cubic
            case "Golden":
                shape = bases.golden
            case _:
                shape = bases.polygon

        # Set the line_shape given by the user to the respective class object
        match lineType:
            case "Centre Circle":
                lineType = line_shapes.centre_circle
            case "Straight":
                lineType = line_shapes.straight
            case _:
                lineType = line_shapes.straight

        # Convert the concentration and ritual values to booleans
        if concentration=="Yes":
            concentration = True
        else:
            concentration = False

        if ritual=="Yes":
                ritual = True
        else:
            ritual = False

        # Generate the spell image
        image = self.create_spell_image(level, rang, area, dtype, school, duration, 
                                  condition if include_conditions else 'None', 
                                  concentration, ritual, shape, lineType, 
                                  include_conditions=include_conditions)
        
        # Check for matching spell
        matching_spell = self.find_matching_spell(level, rang, area, dtype, school, duration, condition, concentration, ritual)
        if matching_spell:
            self.spell_name_label.config(text=f"Matching Spell: {matching_spell}")
        else:
            self.spell_name_label.config(text="Spell does not exist... yet")


        # Display the image
        self.display_image(image)
    def random_spell(self):
        # Generate a random spell
        with open('attributes/levels.txt', 'r') as f:
            levels = f.read().splitlines()
        level = random.choice(levels)
    
        with open('attributes/range.txt', 'r') as f:
            ranges = f.read().splitlines()
        rang = random.choice(ranges)
    
        with open('attributes/area_types.txt', 'r') as f:
            areas = f.read().splitlines()
        area = random.choice(areas)
    
        with open('attributes/damage_types.txt', 'r') as f:
            dtypes = f.read().splitlines()
        dtype = random.choice(dtypes)
    
        with open('attributes/school.txt', 'r') as f:
            schools = f.read().splitlines()
        school = random.choice(schools)
    
        with open('attributes/duration.txt', 'r') as f:
            durations = f.read().splitlines()
        duration = random.choice(durations)

        with open('attributes/conditions.txt', 'r') as f:
            conditions = f.read().splitlines()
        condition = random.choice(conditions)

        concentration = random.choice([True, False])
        ritual = random.choice([True, False])
        shape = random.choice([bases.polygon, bases.quadratic, bases.circle, bases.cubic, bases.golden])
        lineType = random.choice([line_shapes.centre_circle, line_shapes.straight])

        # To prevent poor looking shapes from being randomly generated
        if (concentration or ritual) and shape == bases.circle:
            shape = bases.polygon
        if ritual and shape == bases.quadratic:
            shape = bases.polygon
        if lineType == line_shapes.straight and (shape == bases.quadratic or shape == bases.cubic):
            shape = bases.polygon

        # Update dropdown values to match random selections
        self.level_var.set(level)
        self.school_var.set(school)
        self.duration_var.set(duration)
        self.range_var.set(rang)
        self.area_var.set(area)
        self.dtype_var.set(dtype)
        self.condition_var.set(condition)
        self.concentration_var.set("Yes" if concentration else "No")
        self.ritual_var.set("Yes" if ritual else "No")
        self.shape_var.set({
            bases.polygon: "Polygon",
            bases.quadratic: "Quadratic", 
            bases.circle: "Circle",
            bases.cubic: "Cubic",
            bases.golden: "Golden"
        }[shape])
        self.lineType_var.set("Centre Circle" if lineType == line_shapes.centre_circle else "Straight")

        # Generate the spell image
        image = self.create_spell_image(level, rang, area, dtype, school,duration, condition, concentration, ritual, shape, lineType)
        
        # Check for matching spell
        matching_spell = self.find_matching_spell(level, rang, area, dtype, school, duration, condition, concentration, ritual)
        if matching_spell:
            self.spell_name_label.config(text=f"Matching Spells: {matching_spell}")
        else:
            self.spell_name_label.config(text="Spell does not exist... yet")

        # Display the image
        self.display_image(image)

    # Call the writer.py app to do all the match and drawing
    def create_spell_image(self, level, rang, area, dtype, school, duration, condition, concentration,ritual, shape, lineType, include_conditions=True):
        buf = BytesIO()
        writer.draw_spell(level, rang, area, dtype, school, duration, condition, concentration, ritual, shape, lineType, include_conditions=include_conditions, savename=buf)
        buf.seek(0)
        return buf

    def display_image(self, buf):
        image = Image.open(buf)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.current_image = image  # Store current image for download


    def find_matching_spell(self, level, rang, area, dtype, school, duration, condition, concentration, ritual):
        level_files = {
            "0": "wizard_cantrips.json",
            "1": "wizard_1.json", 
            "2": "wizard_2.json",
            "3": "wizard_3.json",
            "4": "wizard_4.json",
            "5": "wizard_5.json",
            "6": "wizard_6.json",
            "7": "wizard_7.json",
            "8": "wizard_8.json",
            "9": "wizard_9.json"
        }
        
        filename = level_files.get(level, "wizard_cantrips.json")
        matching_spells = []
        
        with open(f'Grimoire/{filename}', 'r') as file:
            spells = json.load(file)
        
        for spell in spells:
            if (str(spell['level']) == level and
                spell['school'] == school and
                spell['duration'] == duration and
                spell['range'] == rang and
                spell['area_type'] == area and
                spell['dtype'] == dtype and
                spell['condition'] == condition and
                spell['concentration'] == concentration and
                spell['ritual'] == ritual):
                matching_spells.append(spell['name'])
        
        return ' | '.join(matching_spells) if matching_spells else None

    def download_image(self):
        if self.current_image:
            filename = filedialog.asksaveasfilename(
                initialfile="glyph",  # Set default filename
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                self.current_image.save(filename)



if __name__ == "__main__":
    root = tk.Tk()
    app = SpellApp(root)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()
