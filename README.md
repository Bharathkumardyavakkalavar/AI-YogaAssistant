# Body Posture Estimation for Yoga Assistance

## Overview
This project focuses on providing real-time feedback on yoga postures using computer vision techniques. The application uses machine learning and computer vision to analyze body posture and give instructions through a speaker to ensure proper alignment during yoga practice.

## Features
- **Real-Time Posture Estimation**: Utilizes computer vision to analyze and provide feedback on yoga poses in real time.
- **Audio Feedback**: Offers verbal instructions to users about their posture, helping them improve their yoga practice.
- **User-Friendly**: A simple interface that can be run on a local machine with Python.

## Architectural Workflow
The following diagram illustrates the workflow of the posture estimation system:

[Architectural Workflow](images/Architectural_workflow.png)

## Keypoints Visualization
The system detects key points on the human body to estimate yoga poses. Below is an example visualization of detected key points:

[Keypoints Visualization](images/Key_points.png)

## Results
The following images show the results of the posture estimation process, including correct and incorrect posture feedback:

[Initial results](initial_results.png)
[Final results](images/Final_results.png)

## Dataset
The project uses the dataset located in `angle_teacher_yoga.csv`, which contains key angle measurements for various yoga poses. This data is utilized in the machine learning algorithms to analyze and provide feedback on user posture.

## Files
- `give_angle_teacher.py`: Contains functions to calculate angles between joints for posture estimation.
- `main.py`: The main application file that runs the posture estimation and audio feedback system.
- `requirements.txt`: Lists the required Python libraries and dependencies for running the project.
- `utils.py`: Contains utility functions that support the main application logic.

## Installation
Follow these steps to set up and run the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Body_Posture_Estimation_for_Physical_Training_Assistance.git
   cd Body_Posture_Estimation_for_Physical_Training_Assistance
   ```
2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   Execute the main Python script to start the application:
   ```bash
   python main.py
   ```

## Usage
- **Set Up Camera**: Ensure your webcam is set up and accessible by the application.
- **Start Yoga Practice**: Follow the verbal instructions provided by the application to perform yoga poses.
- **Adjust Based on Feedback**: Make adjustments to your posture based on the audio feedback to improve your alignment.

## Future Enhancements
- **Expand Dataset**: Include more yoga poses and variations for a comprehensive analysis.
- **Mobile Application**: Develop a mobile version of the application for easier access during practice.
- **User Profiles**: Implement user profiles to track progress over time.

## Contact
For any questions or contributions, feel free to reach out to me via GitHub.
