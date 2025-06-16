import cv2

def zoom_on_faces(input_path, output_path, zoom_factor=1.5):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            cx, cy = x + w//2, y + h//2

            crop_w = int(w * zoom_factor)
            crop_h = int(h * zoom_factor)

            x1 = max(cx - crop_w // 2, 0)
            y1 = max(cy - crop_h // 2, 0)
            x2 = min(cx + crop_w // 2, frame.shape[1])
            y2 = min(cy + crop_h // 2, frame.shape[0])

            zoomed = frame[y1:y2, x1:x2]
            zoomed = cv2.resize(zoomed, (width, height))
            out.write(zoomed)
        else:
            out.write(frame)

    cap.release()
    out.release()
