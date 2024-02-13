# Flame AI

Flame AI is an advanced early fire detection system designed to revolutionize safety protocols by leveraging cutting-edge technology. It swiftly notifies first responders and administrators of fire outbreaks, provides crucial data on surrounding populations for optimal resource allocation, and enables swift rescue operations.

![rsz_demo](https://github.com/sswadkar/hackalytics/assets/63820563/0178dc9f-5538-4703-8a33-fe5bb6baf7a3)

## Inspiration

Inspired by a personal story of a team member affected by a factory fire, we delved into the limitations of existing smoke detectors. Our research highlighted the need for a system that not only detects fires early but also provides actionable data to responders, making Flame AI a necessary innovation in fire safety.

## Features

- **Live Fire Detection**: Real-time analysis of camera/video streams to detect fires.
- **Population Monitoring**: Detects and reports the number of individuals in affected areas.
- **Multi-Camera Support**: Monitors multiple camera views within a building for comprehensive coverage.
- **Instant Notifications**: Sends alerts via Gmail and phone to designated administrators and first responders.
- **Intelligent Forecasting**: Identifies regions at risk of fire using climate data.
- **Interactive Image Map**: Offers real-time environmental metadata through an intuitive interface.

## Use Cases

Flame AI serves first responders, industrial facilities, residential buildings, educational institutions, laboratories, and commercial spaces by providing early detection and crucial data for efficient emergency response and resource allocation.

## How It’s Built

### Directory Structure

- `flaskapp/`: Contains the Flask app and files for training the linear regression model for fire detection.
- `imageprocessing/`: Contains OpenCV and YOLOv5 models for image processing.

### Running the Application

- **Flask App**: Run the app (in `flaskapp/`) using `python app.py` on port 5001. `requirements.txt` is different for each folder, remember to create a venv and run it in that folder respectively.
- **Model Detection**: For each model, use `python detect.py --weights <file.pt> --source 0`. Replace `<file.pt>` with `fire.pt` for the fire detection model and the appropriate file for the regular YOLOv5 model. `requirements.txt` is different for each folder, remember to create a venv and run it in that folder respectively.
- **Combining Data**: Run `python combine.py` in parallel to monitor both models and combine their data using cv2 over a window.

## Challenges

Developing Flame AI introduced us to challenges in computer vision, real-time video processing, and data acquisition. We navigated through learning PyTorch, optimizing video feed analysis, and integrating various technologies into a cohesive system.

## Future Enhancements

We plan to integrate sensor data, detect flammable objects, and incorporate map location functionality, aiming to provide comprehensive fire safety solutions.

## Links

- **Devfolio**: [Flame AI on Devfolio](https://devfolio.co/projects/flame-ai-3ed1)
- **YouTube**: [Flame AI Video Overview](https://www.youtube.com/watch?v=DKoPu3ZSOzs)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
