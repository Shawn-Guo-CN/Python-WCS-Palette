import csv
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import matplotlib.pyplot as plt
import numpy as np


wcs_file = './cnum-vhcm-lab-new.txt'

chip_list = []
legend_list = []

with open(wcs_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    _ = next(reader, None)
    for row in reader:
        if row[2] == '0' and row[3] == '0':
            legend_list.append(row)
        else:
            chip_list.append(row)

def _convert2rgb(chip):
    chip_lab_code = LabColor(float(chip[-3]), float(chip[-2]), float(chip[-1]))
    chip_rgb_code = convert_color(chip_lab_code, sRGBColor)
    return chip_rgb_code.get_upscaled_value_tuple()

chip_rgbs = [_convert2rgb(chip) for chip in chip_list]
legend_rdbs = [_convert2rgb(chip) for chip in legend_list]

nrows, ncols = 8, 40
row_labels = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
col_labels = range(ncols)

image = np.asarray(chip_rgbs)
image = image.reshape((nrows, ncols, 3))
legends = np.asarray(legend_rdbs)
legends = legends.reshape((1, 10, 3))

# 2 extra columns and rows for the legend
fig = plt.figure(figsize=(40, 12))

# plot legend first
for i in range(len(legend_list)):
    ax = fig.add_subplot(nrows+2, ncols+2, i*(ncols+2)+1)
    plt.imshow(legends[0, i, :].reshape(1, 1, 3))
    plt.xticks([])
    plt.yticks([])
    ax.axis('off')
    
# plot V values in Munsell chart
for i in range(10):
    ax = fig.add_subplot(nrows+2, ncols+2, i*(ncols+2)+2)
    ax.patch.set_alpha(0.0)
    ax.patch.set_edgecolor('none')
    ax.axis('off')
    plt.text(0.5, 0.5, chr(65+i), 
             ha='center', va='center', fontsize=28, color='black'
            )
    
# plot ticks for the colours chips
for i in range(40):
    ax = fig.add_subplot(nrows+2, ncols+2, i+3)
    ax.patch.set_alpha(0.0)
    ax.patch.set_edgecolor('none')
    ax.axis('off')
    plt.text(0.5, 0.5, str(i+1), 
             ha='center', va='center', fontsize=28, color='black',
             bbox=dict(alpha=0.0)
            )

# plot the mode colours
for r in range(1, nrows+1):
    for c in range(1, ncols+1):
        ax = fig.add_subplot(nrows+2, ncols+2, r*(ncols+2)+c+2)
        plt.imshow(image[r-1, c-1, :].reshape(1, 1, 3))
        ax.axis('off')
        
plt.savefig('wcs_palette.pdf', format='pdf', dpi=300, bbox_inches='tight')
plt.show()
