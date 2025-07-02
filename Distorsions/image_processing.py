import cv2
import numpy as np

def apply_blur_and_vortex(frame, center_x, center_y, radius, blur_intensity, vortex_strength):
    height, width = frame.shape[:2]

    # Creazione di una maschera circolare sfumata
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, 255, -1)
    mask = cv2.GaussianBlur(mask, (51, 51), 0)  # Aumentato il kernel per una sfumatura più ampia

    # Applicazione dell'effetto di sfocatura periferica
    blurred_frame = cv2.GaussianBlur(frame, (blur_intensity, blur_intensity), 0)

    # Applicazione dell'effetto di distorsione tipo vortex
    map_x, map_y = np.meshgrid(np.arange(width), np.arange(height))
    dx = map_x - center_x
    dy = map_y - center_y
    distance = np.sqrt(dx * dx + dy * dy)
    angle = np.arctan2(dy, dx)
    mask_distortion = distance < radius

    map_x[mask_distortion] = center_x + distance[mask_distortion] * np.cos(angle[mask_distortion] + vortex_strength * (radius - distance[mask_distortion]) / radius)
    map_y[mask_distortion] = center_y + distance[mask_distortion] * np.sin(angle[mask_distortion] + vortex_strength * (radius - distance[mask_distortion]) / radius)

    warped_frame = cv2.remap(blurred_frame, map_x.astype(np.float32), map_y.astype(np.float32), interpolation=cv2.INTER_LINEAR)

    # Combinazione degli effetti utilizzando la maschera sfumata
    mask = cv2.merge([mask, mask, mask])
    result_frame = cv2.addWeighted(frame, 1, warped_frame, 0.5, 0)
    result_frame = np.where(mask == 255, warped_frame, frame)

    return result_frame

# Funzione per ottenere le coordinate del mouse
def mouse_callback(event, x, y, flags, param):
    global center_x, center_y
    if event == cv2.EVENT_MOUSEMOVE:
        center_x, center_y = x, y

# Funzione per aggiornare l'intensità del blur
def update_blur(val):
    global blur_intensity
    blur_intensity = val * 2 + 1  # Assicurati che sia un numero dispari

# Funzione per aggiornare l'intensità del vortex
def update_vortex(val):
    global vortex_strength
    vortex_strength = val / 100.0

# Apri la telecamera
cap = cv2.VideoCapture(0)

# Imposta le coordinate iniziali del centro e il raggio del cerchio
center_x, center_y = 0, 0
radius = 100  # Puoi regolare il raggio come preferisci
blur_intensity = 21  # Intensità iniziale del blur
vortex_strength = 0.5  # Intensità iniziale del vortex

# Crea una finestra e imposta la callback del mouse
cv2.namedWindow('Video con Effetti')
cv2.setMouseCallback('Video con Effetti', mouse_callback)

# Crea le scrollbar per regolare il blur e il vortex
cv2.createTrackbar('Blur', 'Video con Effetti', 10, 50, update_blur)
cv2.createTrackbar('Vortex', 'Video con Effetti', 50, 100, update_vortex)

while True:
    # Cattura frame per frame
    ret, frame = cap.read()

    if not ret:
        break

    # Applica l'effetto di sfocatura e distorsione tipo vortex
    processed_frame = apply_blur_and_vortex(frame, center_x, center_y, radius, blur_intensity, vortex_strength)

    # Mostra il frame con gli effetti applicati
    cv2.imshow('Video con Effetti', processed_frame)

    # Premi 'q' per uscire
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia la telecamera e chiudi tutte le finestre
cap.release()
cv2.destroyAllWindows()