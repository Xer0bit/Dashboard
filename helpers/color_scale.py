
import pandas as pd

def color_scale(series):
    max_val = series.max()
    min_val = series.min()
    sorted_series = series.sort_values(ascending=False)
    gradient_colors = generate_gradient(len(series), max_val, min_val)

    color_map = pd.Series(gradient_colors, index=sorted_series.index)
    return ['background-color: {}'.format(color_map.get(val, '#FFFFFF')) for val in series.index]

def generate_gradient(n, max_val, min_val):
    green = (0, 128, 0)
    orange = (255, 165, 0)
    
    def blend_colors(c1, c2, blend_factor):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * blend_factor) for i in range(3))

    gradient = []
    for i in range(n):
        blend_factor = i / (n - 1) if n > 1 else 0
        blended_color = blend_colors(green, orange, blend_factor)
        hex_color = '#{:02x}{:02x}{:02x}'.format(*blended_color)
        gradient.append(hex_color)
    
    return gradient
