import cv2

def zoom_on_faces(input_path, output_path, zoom_factor=1.5, max_frames=300):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise Exception("Cannot open video")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    frame_count = 0

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            cx, cy = x + w // 2, y + h // 2
            crop_w, crop_h = int(w * zoom_factor), int(h * zoom_factor)

            x1 = max(cx - crop_w // 2, 0)
            y1 = max(cy - crop_h // 2, 0)
            x2 = min(cx + crop_w // 2, width)
            y2 = min(cy + crop_h // 2, height)

            zoomed = frame[y1:y2, x1:x2]
            zoomed = cv2.resize(zoomed, (width, height))
            out.write(zoomed)
        else:
            out.write(frame)

        frame_count += 1

    cap.release()
    out.release()
