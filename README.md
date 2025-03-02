# DeSPIn - DeepSeek PI Navigator
## 1 Problem Description

Large language models (LLMs) have gained significant popularity, offering a more intuitive approach to human-computer interaction. One of the key challenges in robotics is converting vague, natural-language instructions into precise machine-executable commands. Artificial intelligence provides an efficient solution, enabling robots to become more adaptable and intelligent.  

To solve this problem, our aim is to develop a framework that translates human language into actionable tasks for autonomous vehicles. Thus we designed a system where a smart car can interpret instructions and execute them autonomously within predefined constraints.

## 2 What it does

* Successfully deployed the Deepseek large language model (1.5B parameter version) on a Raspberry Pi 4, enabling effective communication.
* The primary objective is to standardize ambiguous instructions by leveraging the language model. For instance, when given an input such as *"Go find the red ball and get it back,"* the model processes the command and extracts key action-oriented components, such as *"red,"* *"go,"* and *"get it back."*
* Subsequently, the program interprets the model’s output and translates it into actionable commands. Specifically, the system navigates the vehicle forward while utilizing its camera to detect the color red, facilitating task execution.

## Inspiration

Configuring autonomous vehicles to perform specific tasks can be complex, often requiring expert knowledge of various settings and configurations. Different parameters can lead to varied behaviors, making it challenging for non-experts to achieve the desired outcomes. Our goal is to simplify this process by reducing the job training time required for individuals to operate and manage multiple autonomous vehicles simultaneously. Instead of dealing with intricate settings, users should be able to simply instruct the vehicle in normal conversational language, and the vehicle should execute the command seamlessly. This approach significantly reduces complexity compared to traditional configuration methods.

## What It Does

Our system allows an operator to issue requests in natural, conversational English, which the autonomous vehicle then interprets and executes. The vehicle navigates to the requested locations independently, avoiding obstacles and finding the best path to the destination without requiring external assistance.

## How We Built It

We built this system using a Raspberry Pi 4 to control a small autonomous car. The vehicle is equipped with various components, including:
- An ultrasonic sensor for detecting obstacles and measuring distances
- A speaker for audio feedback and alerts
- Servos for steering, as well as for controlling the camera’s pan and tilt
- Motors to drive the wheels
- An onboard camera for identifying and locating objectives
- A locally run DeepSeek-R1 LLM model to process natural language instructions

## Challenges We Ran Into

During development, we encountered several challenges, including:
- Accidentally burning out a speaker during initial testing
- A loose camera cable causing signal loss mid-operation
- Damage to servo sensor data, leading to occasional instability in performance
- Unexpected ultrasonic sensor readings when measuring distances beyond its capabilities, resulting in unreliable measurements
- Deepseek-R1 1.5B was able to run on the Raspberry Pi 4 itself, but was very slow so was not very usable for use.

## Accomplishments That We're Proud Of

Despite the challenges, we successfully achieved several key milestones:
- The system is capable of converting conversational instructions into explicit commands for the car
- The vehicle can locate and navigate to specified objectives autonomously
- It effectively avoids obstacles and walls when encountered
- It provides audible alerts when completing assigned objectives

## What We Learned

Throughout this project, we gained several important insights:
- Sensors and their readings are more fragile and unstable than initially expected
- Vibrations can cause connections to come loose, emphasizing the importance of regularly checking hardware connections
- Sanity checks on sensor outputs are essential to ensure reliability, as raw data often deviates from expected values

## What's Next for DeSPIn

Moving forward, we plan to implement several improvements to enhance our system:
- Replacing color-based recognition and tracking with object detection to reduce dependency on environmental color conditions
- Refining the search technique to minimize unnecessary movement, utilizing camera panning more effectively to locate objectives
- Introducing real-time voice command capabilities for even more intuitive and interactive control
