import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils.dataframe import dataframe_to_rows
from PIL import Image

# File mapping
files = {
    "Paragrafo 1": {"BM": "BM_1.TXT", "NV": "NV_1.TXT"},
    "Paragrafo 2": {"BM": "BM_2.TXT", "NV": "NV_2.txt"},
    "Paragrafo 3": {"BM": "BM_3.TXT", "NV": "NV_3.txt"}
}

# Load data
def load_data(file):
    return pd.read_csv(file, sep="\t")

# Extract saccades and fixations
def extract_events(df):
    sacc = df[df['label'] == 'SACC']
    fixa = df[df['label'] == 'FIXA']
    return sacc, fixa

# Compute PRL and its stability
def compute_prl(fixations):
    x = (fixations['start_x'] + fixations['end_x']) / 2
    y = (fixations['start_y'] + fixations['end_y']) / 2
    return x.mean(), y.mean(), x.std(), y.std()

# Compute statistics
def compute_stats(sacc, fixa):
    prl_x, prl_y, prl_std_x, prl_std_y = compute_prl(fixa)
    return {
        "Numero Saccadi": len(sacc),
        "Ampiezza Media Saccadi": sacc['amp'].mean(),
        "Velocità Picco Media Saccadi": sacc['peak_vel'].mean(),
        "Durata Media Fissazioni": fixa['duration'].mean(),
        "Stabilità Fissazioni (std)": np.sqrt(((fixa['start_x'] + fixa['end_x'])/2).std()**2 + ((fixa['start_y'] + fixa['end_y'])/2).std()**2),
        "PRL_x": prl_x,
        "PRL_y": prl_y,
        "Stabilità PRL (std)": np.sqrt(prl_std_x**2 + prl_std_y**2)
    }

# Plot saccades and fixations
def plot_saccades_fixations(saccades, fixations, prl, title, ax, limits):
    for _, row in saccades.iterrows():
        ax.arrow(row['start_x'], row['start_y'],
                 row['end_x'] - row['start_x'], row['end_y'] - row['start_y'],
                 head_width=1.5, head_length=2, fc='blue', ec='blue', alpha=0.5)
    fx = (fixations['start_x'] + fixations['end_x']) / 2
    fy = (fixations['start_y'] + fixations['end_y']) / 2
    ax.scatter(fx, fy, color='green', label='Fixations', alpha=0.6)
    dx = saccades['end_x'] - saccades['start_x']
    dy = saccades['end_y'] - saccades['start_y']
    angles = np.arctan2(dy, dx)
    mean_angle = np.arctan2(np.mean(np.sin(angles)), np.mean(np.cos(angles)))
    ax.arrow(prl[0], prl[1], 20 * math.cos(mean_angle), 20 * math.sin(mean_angle),
             head_width=2, head_length=3, fc='red', ec='red', label='Direzione Media')
    ax.scatter(*prl, color='red', s=100, marker='x', label='PRL')
    ax.set_title(title)
    ax.set_xlim(limits)
    ax.set_ylim(limits)
    ax.set_aspect('equal')
    ax.legend()

# Heatmap fissazioni
def plot_heatmap(fixations, title, limits, ax):
    fx = (fixations['start_x'] + fixations['end_x']) / 2
    fy = (fixations['start_y'] + fixations['end_y']) / 2
    sns.kdeplot(x=fx, y=fy, fill=True, cmap="Reds", bw_adjust=1, ax=ax)
    ax.set_title(title)
    ax.set_xlim(limits)
    ax.set_ylim(limits)
    ax.set_aspect('equal')

# Create Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Statistiche"

# Collect all stats
all_stats = []
images = []

for par, conds in files.items():
    row = {"Paragrafo": par}
    fig1, axes1 = plt.subplots(1, 2, figsize=(14, 6))
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))
    all_fx = []
    all_fy = []

    for i, (cond, fname) in enumerate(conds.items()):
        df = load_data(fname)
        sacc, fixa = extract_events(df)
        stats = compute_stats(sacc, fixa)
        for k, v in stats.items():
            row[f"{k} ({cond})"] = v
        fx = (fixa['start_x'] + fixa['end_x']) / 2
        fy = (fixa['start_y'] + fixa['end_y']) / 2
        all_fx.append(fx)
        all_fy.append(fy)

    all_fx = pd.concat(all_fx)
    all_fy = pd.concat(all_fy)
    limits = (min(all_fx.min(), all_fy.min()) - 20, max(all_fx.max(), all_fy.max()) + 20)

    for i, (cond, fname) in enumerate(conds.items()):
        df = load_data(fname)
        sacc, fixa = extract_events(df)
        prl = compute_prl(fixa)[:2]
        plot_saccades_fixations(sacc, fixa, prl, f"{cond} - {par}", axes1[i], limits)
        plot_heatmap(fixa, f"Heatmap {cond} - {par}", limits, axes2[i])

    fig1.tight_layout()
    fig2.tight_layout()
    fig1_path = f"sacc_fix_{par.replace(' ', '_')}.png"
    fig2_path = f"heatmap_{par.replace(' ', '_')}.png"
    fig1.savefig(fig1_path)
    fig2.savefig(fig2_path)
    images.append((fig1_path, fig2_path))
    plt.close(fig1)
    plt.close(fig2)
    all_stats.append(row)

# Write stats to Excel
df_stats = pd.DataFrame(all_stats)
for r in dataframe_to_rows(df_stats, index=False, header=True):
    ws.append(r)

# Add images to Excel
row_offset = len(df_stats) + 3
for i, (fig1_path, fig2_path) in enumerate(images):
    img1 = XLImage(fig1_path)
    img2 = XLImage(fig2_path)
    img1.anchor = f"A{row_offset + i*30}"
    img2.anchor = f"K{row_offset + i*30}"
    ws.add_image(img1)
    ws.add_image(img2)

# Add PRL description
ws2 = wb.create_sheet("Metodo PRL")
ws2["A1"] = "Metodo di stima del PRL"
ws2["A2"] = (
    "Il PRL (Preferred Retinal Locus) è stimato come il centro medio delle fissazioni, "
    "calcolato come media dei punti centrali tra inizio e fine di ogni fissazione:\n\n"
    "PRL_x = media((start_x + end_x)/2)\n"
    "PRL_y = media((start_y + end_y)/2)\n\n"
    "La stabilità del PRL è calcolata come deviazione standard euclidea delle posizioni di fissazione."
)

# Save workbook
wb.save("report_completo.xlsx")
print("Report completo salvato in 'report_completo.xlsx'")
