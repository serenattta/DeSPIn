# Project name

## 0 Overview

## 1 Problem

*LLM is now popular, bringing a more intuitive way for human-computer interaction. How to convert vague instructions into specific machine instructions, artificial intelligence provides us with a convenient way to make robots universal and intelligent. The problem we have to solve is how to translate human language into a task that a smart car can perform, and have the car perform that task automatically within a given framework.*

Large language models (LLMs) have gained significant popularity, offering a more intuitive approach to human-computer interaction. One of the key challenges in robotics is converting vague, natural-language instructions into precise machine-executable commands. Artificial intelligence provides an efficient solution, enabling robots to become more adaptable and intelligent.  

To solve this problem, our aim is to develop a framework that translates human language into actionable tasks for autonomous vehicles. Thus we designed a system where a smart car can interpret instructions and execute them autonomously within predefined constraints.

如今LLM大行其道，为人机交互带来了更为直观的方式。如何将模糊的指令转换成具体的机器指令，人工智能为我们提供了一个便捷的方法，使得机器人通用化，智能化。我们要解决的问题是如何将人类语言转换成智能小车能执行的任务，并让小车在给定的框架下自动执行该任务。

## 2 Solution

* Successfully deployed the Deepseek large language model (1.5B parameter version) on a Raspberry Pi 4, enabling effective communication.
* The primary objective is to standardize ambiguous instructions by leveraging the language model. For instance, when given an input such as *"Go find the red ball and get it back,"* the model processes the command and extracts key action-oriented components, such as *"red,"* *"go,"* and *"get it back."*
* Subsequently, the program interprets the model’s output and translates it into actionable commands. Specifically, the system navigates the vehicle forward while utilizing its camera to detect the color red, facilitating task execution.

1. 我们在raspberry pi 4上部署了Deepseek大语言模型（1.5B参数版本），目前成功对话
2. 目的是需要将模糊的指令通过语言模型标准化，比如我在计算机上输入“去找红色的球再拿回来”，语言模型能输出”红色“。
3. 接着我的程序会识别这个语言模型的输出。并操控小车前进，使用摄像头识别红色。
