from ultralytics import YOLO
import cv2
import json

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to access webcam")
        break

    # Run YOLO detection
    results = model(frame)

    # Count people
    people_count = 0

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])

            # Class 0 = Person
            if cls == 0:
                people_count += 1

    # Crowd Status Logic
    if people_count < 5:
        status = "Not Crowded"
    elif people_count < 10:
        status = "Moderately Crowded"
    else:
        status = "Highly Crowded"
    data = {
    "people_count": people_count,
    "status": status
    }

    with open("backend/live_data.json", "w") as f:
        json.dump(data, f)
    

    # Draw detection boxes
    frame = results[0].plot()

    # Display people count
    cv2.putText(
        frame,
        f"People Count: {people_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Display crowd status
    cv2.putText(
        frame,
        f"Status: {status}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    # Show window
    cv2.imshow("AI Crowd Detection", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()