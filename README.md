# Face Recognition Based Attendance System

This project is a face recognition-based attendance system that uses OpenCV and Python. The system uses a camera to capture images of individuals and then compares them with the images in the database to mark attendance.

## Installation

1. Clone the repository to your local machine. ``` git clone https://github.com/Arijit1080/Face-Recognition-Based-Attendance-System ```
2. Install the required packages using ```pip install -r requirements.txt```.
3. Download the dlib models from https://drive.google.com/drive/folders/12It2jeNQOxwStBxtagL1vvIJokoz-DL4?usp=sharing and place the data folder inside the repo

## Usage

Run the dashboard from the project folder:

```powershell
python app.py
```

The dashboard opens in your default browser at `http://127.0.0.1:5000`. Use its **Register a new student** button to capture face images; when you close the registration window, the face recognition data is updated automatically. Use **Take attendance** to open the recognition camera, and use **Present students** to view attendance by date. Press `q` in the attendance camera window to end an attendance session.

The camera actions open desktop windows, so run the dashboard on the same computer as the camera. Keep the terminal running while you use it.


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have any suggestions.


