import GlyphEngine.bases as bases
import GlyphEngine.line_shapes as line_shapes
import numpy as np
import matplotlib.pyplot as plt
import os
import json

cmap = plt.get_cmap('turbo')

#---------Functions for creating unique binary numbers------
def cycle_list(l, loops=1):
    n = len(l)
    for t in range(loops):
        l = [l[(i + 1) % n] for i in range(n)]
    return l

def generate_unique_combinations(L):
    combinations = generate_binary_strings(L)
    non_repeating = [combinations[0]]
    for i in range(len(combinations)):
        ref = list(combinations[i])
        N = len(ref)
        test = 0
        for j in range(len(non_repeating)):
            for n in range(N):
                if cycle_list(list(non_repeating[j]), loops=n + 1) == ref:
                    test += 1
        if test == 0:
            non_repeating.append(combinations[i])
            
    for i in range(len(non_repeating)):
        non_repeating[i] = [int(s) for s in list(non_repeating[i])]
    return non_repeating


def generate_binary_strings(bit_count):
    # List to store all binary strings
    binary_strings = []
    
    # Helper function to recursively generate binary strings
    def genbin(n, bs=''):
        # Base case: if binary string length equals desired bit count, add it to list
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            # Recursive case: append both 0 and 1 to current string and continue
            genbin(n, bs + '0')
            genbin(n, bs + '1')

    # Start recursive generation with initial bit count
    genbin(bit_count)
    return binary_strings


#-------Functions for drawing runes
def decode_shape(in_array, k=1, point_color='k', on_color='darkred', off_color="grey",
                 label=None, base_fn=bases.polygon, base_kwargs=[],
                 shape_fn=line_shapes.straight, shape_kwargs=[], plot_base=False):
    n = len(in_array)
    x, y = base_fn(n, *base_kwargs)
    if plot_base:
        plt.scatter(x[1:], y[1:], s=70, facecolors='none', edgecolors=point_color)
        plt.scatter(x[0], y[0], s=70, facecolors=point_color, edgecolors=point_color)
        plt.axis('off')
        plt.axis('scaled')
    for i, elem in enumerate(in_array):
        P = [x[i], y[i]]
        Q = [x[(i + k) % n], y[(i + k) % n]]
        X, Y = shape_fn(P, Q, *shape_kwargs)
        if elem == 0:
            plt.plot(X, Y, color=off_color, ls="--", linewidth=0.25)
        elif elem == 1:
            plt.plot(X, Y, color=on_color, ls="-", label=label if i == np.where(in_array == 1)[0][0] else None,
                     linewidth=2)
        else:
            print(f'elem {elem} at index {i} is not valid, input being skipped')

def draw_multiple_inputs(in_array, concentration, ritual, 
                         base_fn=bases.polygon, base_kwargs=[],
                         shape_fn=line_shapes.straight, shape_kwargs=[],
                         point_color='k', labels=[], legend=False, colors=[],
                         legend_loc="upper left"):
    
    if isinstance(colors, list) and len(colors) == 0:
        colors = [point_color] * in_array.shape[0]
    elif isinstance(colors, str):
        colors = [colors] * in_array.shape[0]
    n = in_array.shape[1]
    x, y = base_fn(n, *base_kwargs)
    plt.scatter(x[1:], y[1:], s=70, facecolors='none', edgecolors=point_color)
    plt.scatter(x[0], y[0], s=70, facecolors=point_color, edgecolors=point_color)
    
    if len(labels) != in_array.shape[0]:
        labels = [None] * in_array.shape[0]

    for i, k in enumerate(range(in_array.shape[0])):
        decode_shape(in_array[i], k=k + 1, base_fn=base_fn, base_kwargs=base_kwargs,
                     shape_fn=shape_fn, shape_kwargs=shape_kwargs, label=labels[i], on_color=colors[i])

    if labels[0] is not None and legend:
        # Get current handles and labels
        handles, labels = plt.gca().get_legend_handles_labels()
        
        # Create concentration and ritual entries first
        conc_line, = plt.plot([], [], 'o', color='black', label=f"Concentration: {concentration}")
        ritual_line, = plt.plot([], [], 'o', color='black', label=f"Ritual: {ritual}")
        
        # Then create base and shape entries
        base_name = base_fn.__name__
        shape_name = shape_fn.__name__
        base_line, = plt.plot([], [], '-', color='black', label=f"Base: {base_name}")
        shape_line, = plt.plot([], [], '-', color='black', label=f"Shape: {shape_name}")
        
        # Add to handles and labels in the desired order
        handles.extend([conc_line, ritual_line, base_line, shape_line])
        labels.extend([f"Concentration: {concentration}", f"Ritual: {ritual}",
                      f"Base: {base_name}", f"Shape: {shape_name}"])
        match base_fn:
            case bases.polygon: # If generating a polygon
                plt.legend(loc=legend_loc, fontsize=10, bbox_to_anchor=(-.7, 1.0))
            case bases.quadratic: # If generating a quadratic
                match shape_fn:
                    case line_shapes.straight: # of straight line type
                        plt.legend(loc=legend_loc, fontsize=10, bbox_to_anchor=(-2, 1.0))
                    case line_shapes.centre_circle: # of centre circle type
                        plt.legend(loc=legend_loc, fontsize=10, bbox_to_anchor=(-1, 1.0))
            case bases.circle:
                    plt.legend(loc=legend_loc, fontsize=10, bbox_to_anchor=(-.5, 1.0))
            case bases.cubic: # If generating a cubic
                match shape_fn:
                    case line_shapes.centre_circle: # of centre circle type
                        plt.legend(loc=legend_loc, fontsize=10, bbox_to_anchor=(-1, 1.0))
                    case line_shapes.straight: # of straight line type
                        plt.legend(loc=legend_loc, fontsize=10, bbox_to_anchor=(-2, 1.0))
            case bases.golden: # If generating a golden
                match shape_fn:
                    case line_shapes.centre_circle: # of centre circle type
                        plt.legend(loc=legend_loc, fontsize=10, bbox_to_anchor=(-.7, 1.0))
                    case line_shapes.straight: # of straight line type
                        plt.legend(loc=legend_loc, fontsize=10, bbox_to_anchor=(-.5, 1.0))
        
    plt.axis('off')
    plt.axis('scaled')

def load_attribute(fname):
    with open(fname, "r") as f:
        data = f.readlines()
    data = [d.strip().lower() for d in data]
    return data

def draw_spell(level, rang, area, dtype, school, duration, condition, 
               concentration, ritual, base_fn, shape_fn, include_conditions=True,
               savename="output.png", legend=True, base_kwargs=[],
               shape_kwargs=[], colors=[], legend_loc="upper left", breakdown=True,
               base_dir=""):
    plt.clf()  # Clear the figure before drawing new glyph

    # Load attributes
    with open("GlyphEngine/attributes.json", "r") as f:
        attributes = json.load(f)
        ranges = attributes["ranges"]
        levels = attributes["levels"]
        area_types = attributes["area_types"]
        dtypes = attributes["damage_types"]
        schools = attributes["schools"]
        durations = attributes["durations"]
        conditions = attributes["conditions"]
    
    # Find indices for the attributes and uses lowercases values
    i_range = [r.lower() for r in ranges].index(rang.lower())
    i_levels = levels.index(str(level))
    i_area = [a.lower() for a in area_types].index(area.lower())
    i_dtype = [dt.lower() for dt in dtypes].index(dtype.lower())
    i_school = [s.lower() for s in schools].index(school.lower())
    i_duration = [d.lower() for d in durations].index(duration.lower())
    i_condition = [ct.lower() for ct in conditions].index(condition.lower())

    # Always include all attributes in consistent order
    attributes = [i_levels, i_school, i_duration, i_range, i_area, i_dtype, i_condition]
    labels = [f"Level: {level}", 
             f"School: {school}", 
             f"Duration: {duration}", 
             f"Range: {rang}", 
             f"Area Type: {area}", 
             f"Damage Type: {dtype}",
             f"Condition: {condition}"]
    N = 2 * len(attributes) + 1
    
    # Handle breakdown coloring
    if breakdown:
        if len(colors) == 0:  # If no colors provided, use a colormap
            colors = [cmap(i / len(attributes)) for i in range(len(attributes))]
        else:  # Use the provided colors
            assert len(colors) == len(attributes), "The number of colors must match the number of attributes"
    else:
        # Handle missing colors by providing default ones
        if len(colors) == 0:  # Check if colors is empty
            colors = ['blue'] * N  # Default to a list of blue colors

        # Ensure there are enough colors for all attributes and combinations
        if len(colors) < N:
            colors.extend(['red'] * (N - len(colors)))  # Add more colors if necessary

    # Create output directory for unique combinations
    if not os.path.isdir(base_dir + "Uniques/"):
        os.makedirs(base_dir + "Uniques/")
    
    # Load or generate unique combinations
    if os.path.isfile(base_dir + f'Uniques/{N}.npy'):
        non_repeating = np.load(base_dir + f'Uniques/{N}.npy')
    else:
        non_repeating = generate_unique_combinations(N)
        non_repeating = np.array(non_repeating)
        np.save(base_dir + f"Uniques/{N}.npy", non_repeating)

    # Create the input array based on attributes
    input_array = np.array([non_repeating[i] for i in attributes])

    # Draw the multiple inputs
    draw_multiple_inputs(input_array, concentration, ritual, base_fn=base_fn, labels=labels, legend=legend,
                        base_kwargs=base_kwargs,
                        shape_fn=shape_fn, shape_kwargs=shape_kwargs,
                        colors=colors, legend_loc=legend_loc)

    # Handle concentration and ritual markers
    if ritual:
        if len(colors) > 0:
            plt.plot(0, 0, "", markersize=10, marker=".", color=colors[0])  # Dot for ritual
    if concentration:
        if len(colors) > 1:
            plt.plot(0, 0, "", markersize=20, marker="o", color=colors[1], mfc='none', linewidth=10)  # Empty circle for concentration



    plt.savefig(savename, transparent=False, bbox_inches='tight')
    plt.clf()
