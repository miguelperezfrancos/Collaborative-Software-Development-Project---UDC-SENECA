# Project overview

This repository shows a project completed by the development team at the University of Coruna and the technical writer at Seneca Polytechnic. The team members used COIL collaboration to create a linear regression app call TrendLine.

## Documentation audience

This documentation aims to provide all the information needed for developers and technical writers to work on the TrendLine app. The content is written in English, but international contributors are welcome.

# COIL collaboration

Collaborative Online International Learning (COIL) is an online learning method where students from different international and educational backgrounds work together to create a project. By using online communication tools, the students have the opportunity to grow their collective knowledge and ability to work with diverse peers. The current team consists of developers from Coruna, Spain, and a technical writer from Toronto, Canada.

The goals of the development team are to:

- Plan and complete weekly sprint user stories and tasks.
- Write and revise code to create TrendLine’s features.
- Update the technical writer with new information as needed.
- Participate in weekly sprint retrospectives.

The goals of the technical writer are to:

- Get weekly updates about TrendLine from the development team.
- Understand TrendLine’s existing and new features.
- Create clear documentation that aligns with the TrendLine.
- Participate in weekly sprint retrospectives.

Table 1 shows the project tools that are used.

| Tool Used         | Purpose                                                     |
|-------------------|-------------------------------------------------------------|
| WhatsApp          | For regular communication and video calls regarding the project updates. |
| Taiga             | For planning the sprint tasks.                              |
| VS Code           | For writing and testing the code.                           |
| Python            | For using the modules in the code.                          |
| GitHub            | For storing the code and documentation.                     |
| Microsoft Word    | For writing documentation.                                  |
| Microsoft Excel   | For storing the datasets in .csv file.                      |

**Table 1:** The project tools used to create TrendLine.

# The agile development process

The agile development process is software development process that focuses on achieving small, iterative tasks called sprints.

The tasks for the project are created by the stakeholder. Each sprint lasts one week and involves planning, designing, building, testing and reviewing the project tasks. This is a flexible process that allows any issues to be communicated immediately, so changes and improvements can be made quickly and consistently.

Each sprint follows this format:

1. The developers plan and work on the tasks that are needed to move the project forward.
2. The tasks are reflected on their Taiga agile project management platform.
3. After the tasks are completed, the developers and technical writer meet by video call on WhatsApp.
4. The scrum master (one of the developers) leads a discussion on the tasks completed during the sprint, potential solutions, and next steps.

If there are any issues that cannot be solved by the team, the stakeholder or product manager can be contacted.

In total, there are 8 sprints in this project, each spanning 1 week-long.

Table 2 shows the role and responsibilities of each team member.

| Role              | Name                          | Responsibilities                                                                 |
|-------------------|-------------------------------|---------------------------------------------------------------------------------|
| Product Owner     | Alberto                       | - Define the software requirements                                              |
|                   |                               | - Create the product backlog and tasks                                          |
|                   |                               | - Clarify requirements as needed                                                 |
| Scrum Master      | Alberto, Guillermo             | - Lead the weekly scrums                                                         |
|                   |                               | - Ensure each team member has what they need to complete their tasks            |
|                   |                               | - Lead discussions to resolve issues that may arise                              |
|                   |                               | - Answer questions from team members as needed                                  |
| Technical Writer  | Grace                         | - Write and update documentation for the software based on feedback from managers, users, and developers |
|                   |                               | - Interview developers to gain knowledge about the software                       |
|                   |                               | - Use technical writing best practices in the documentation                       |
|                   |                               | - Keep track of hours and tasks in Taiga                                        |
|                   |                               | - Review information on GitHub from developers                                  |
|                   |                               | - Participate in weekly scrums                                                  |
| Developer         | Miguel, Rafael, Guillermo, Rodrigo | - Work with other developers to follow the tasks in the product backlog         |
|                   |                               | - Add the tasks to each sprint and estimate each task’s difficulty and timeline  |
|                   |                               | - Keep track of tasks and timeline on Taiga                                      |
|                   |                               | - Write and update files on GitHub                                              |
|                   |                               | - Write code to develop the software according to the requirements               |
|                   |                               | - Participate in weekly scrums                                                  |

**Table 2:** The roles and responsibilities for the project.

# The goals of TrendLine

TrendLine is an English desktop app that uses one set of data to predict another set of data. Once a .csv dataset file is uploaded, TrendLine will then:

- Build a linear regression model to show the relationship between the input and output data
- Display the model’s formula, MSE and r<sup>2</sup> value
- Show a graph of the data
- Save the dataset as a linear regression model
- Open a previously saved linear regression model to continue using it in the app
- Calculate predicted outputs based on the linear regression model

## TrendLine audience

This app was created for corporate companies who need to use their medium-sized datasets to predict output. They will use the predicted output to make future business decisions and plans.

## TrendLine system requirements

Both macOS 15 and Windows 11 computer systems are compatible for this project and TrendLine.

# TrendLine and helpful concepts

TrendLine comprises of various concepts. To deepen your understanding of the app’s purpose, explore the following concepts:

- [What is linear regression?](#_What_is_linear)
- [What is linear regression used for?](#_What_is_linear_1)
- [What is machine learning?](#_What_is_machine)

## What is linear regression?

Linear regression is a model that uses the value of one variable to predict the value of another variable. These values can be graphed into a straight line called a linear regression.

The simplest linear regression is represented by the formula y= mx+b, where y= the output value, x= the input value, b= the y-axis intercept.

The linear regression formula and the input value are used to predict the output value. The linear regression also produces two important data points, the mean square error (MSE) and the coefficient of determination (r<sup>2</sup>).

**Note:** A linear regression assumes that the relationship of the x and y variable is linear, though this may not always be the most accurate representation.

### What is the mean squared error (MSE)?

The mean squared error (MSE) represents the distance between each point to the regression line and squaring it. The distance between each point and the regression line represents the errors, so the MSE is the mean squared error of a set of data. The lower the MSE, the lower the error.

### What is the coefficient of determination (r<sup>2</sup>)?

The predictions made by the linear regression are not 100% accurate. To determine the accuracy, the coefficient of determination value must be considered. The coefficient of determination is a number from 0 to 1 that shows the variance that the dependent variable can be explained by the input value. For example, an r<sup>2</sup> of 0.2 indicates that there is a 20% of the variance of the predicted output that is explained by the input value. The higher the r<sup>2</sup>, the more accurate the linear regression represents the dataset.

## What is linear regression used for?

Linear regressions provide a way to generate predictions that can be used in various subjects, such as biology, business, environmental sciences, and more. It is a well-trusted statistical model that can creates predictions to support business and organizational decisions.

Once the linear regression formula is produced, you can give it a new input value, and the model will calculate the predicted output value.

### Real life applications of linear regressions

Linear regressions can be used when a dataset is available to predict another dataset. For example, linear regression can be used to predict:

- Home sale prices based on number of bedrooms and bathrooms.
- Forecasted precipitation based on weather data.
- Plant growth based on amount of water.

## What is machine learning?

Machine learning is a subset of artificial intelligence. While artificial intelligence (AI) refers to a wide range of technologies that can perform tasks that are usually done by human intelligence, machine learning uses a specific dataset to identify patterns and make predictions.

For example, TrendLine uses machine learning to process the input data to predict the relevant output data. The more input data given to the model, the more accurately machine learning can learn patterns and predict trends.

# Making updates in TrendLine

The code for TrendLine is stored in the [GitHub repository](https://github.com/miguelperezfrancos/Collaborative-Software-Development-Project---UDC-SENECA). To update the code, you will need to install Python, Visual Studio Code, the TrendLine code and the required Python libraries.

## Installing Python

You will need to install Python on your device before installing TrendLine.

**To install Python**

1. Download the [latest version of Python](https://www.python.org/downloads/) for your device.  
    The Setup installer appears.
2. Check the _Add Python to PATH_ box.
3. Click **Customize installation**.
    1. Check the _pip box_.
    2. Click **Next**.
4. Check any necessary boxes and select the install location.
5. Click **Now**.
    Python is installed onto your device.

# Installing Visual Studio Code

Visual Studio Code (VS Code) is the software needed to open, edit, run and debug Python codes.

**To install VS Code**

1. Download the [latest version of Visual Studio Code](https://code.visualstudio.com/Download) for your device.  
    The installer downloads an .exe file.
2. Open the **.exe file**.
3. Select _I accept the agreement_ and click **Next**.
4. Choose the folder you would like to keep VS Code and click **Next**.
5. Check _Add to PATH_ and click **Next**.
6. Click **Install**.  
    VS Code installs onto your device.
7. Click **Finish**.
    VS code is installed and is ready to launch.

**Note:** _Add to PATH_ allows you to launch VS Code from the command line.

# Installing TrendLine

After installing Python and VS Code, you will download the app from the [GitHub repository](https://github.com/miguelperezfrancos/Collaborative-Software-Development-Project---UDC-SENECA).

**Note:** If the app has been updated, you must repeat these steps to reinstall TrendLine using the updated version from GitHub.

**To install TrendLine**

1. Go to the [GitHub repository](https://github.com/miguelperezfrancos/Collaborative-Software-Development-Project---UDC-SENECA).
2. Click **<> Code**.
    A pop-up with the cloning options appears.
3. Click **Download ZIP**.
4. Expand the folder.  
    The folder containing the linear regression app is ready to be used.

# Downloading Python modules

To run the app on your device, you will need to download some modules that contain the necessary information.

The modules are as follows:

- Pyside6
- Pandas
- UserInterface
- Matplotlib
- Scikit-learn

**To download Python modules**

1. Open **VS Code**.
2. Go to **File** > **New Folder** > select the folder containing the app.  
    The app’s code opens in VS Code.
3. Go to **View** > **Terminal**.
4. Type _pip install Pyside6_ and press **Enter** on the keyboard.  
    The module Pyside6 downloads.
5. Repeat step 4 for each module.  
    Repeat step 4 for each module: _Pandas, UserInterface, Matplotlib, Scikit-learn_.  
    Once all the modules are downloaded, proceed to [Running the linear regression app](#_Running_the_linear).

# Running TrendLine

After installing Python, VS Code, the Python modules and the linear regression app, you are ready to add the dataset and run the app.

**Note:** The dataset must be in .csv file.

**To open the app**

1. Open **VS Code**.
2. Go to **File** > **New Folder** > Select the folder containing the app.
3. Click the _main.py_ file in the side bar.  
    The _main.py_ code appears.
4. Click the **Run Python file** button.
    The linear regression app opens. The code is ready to be revised, updated and debugged as needed.

# Considerations for TrendLine updates

TrendLine is an open-source desktop app that can be updated by anyone. If you are joining this project, please keep the following considerations and guidelines during and after the 8 sprints are completed. This process should be continued for future debugging and future version releases.

## Considerations for developers

This app is written using Python. We recommend using VS code to write, edit and revise the code during each sprint. Each update must include debugging, and a summary of changes made. The list of changes and new updates must be updated in the [GitHub repository](https://github.com/miguelperezfrancos/Collaborative-Software-Development-Project---UDC-SENECA) and sent to the technical writer(s) for documentation.

## Considerations for technical writers

The technical writer is responsible for using technical writing best practices to continuously update the documentation. We recommend preparing a list of questions about the TrendLine before going to each meeting with the developers, so that you will be able to accurately describe the features and updates of the app. Any new documentation must be written in Markdown on the [GitHub repository](https://github.com/miguelperezfrancos/Collaborative-Software-Development-Project---UDC-SENECA).

# Guidelines for contributing to TrendLine

Thank you for taking part of this project! Please kindly follow the specific guidelines for both the development and documentation teams.

## Guidelines for developers

- To clone the repository, clone your fork to your local machine: git clone <https://github.com/your-username/your-repository.git>
- To create a new branch for your changes, create a new branch for your feature or bug fix: git checkout -b your-feature-branch
  - Name your new branch as the following: _your name_feature_feature that you are working on_
- To add the latest changes to your local machine: git pull origin <_name of the branch you want to pull: main/other developer's branch_\>
- Test your code before committing and run all existing tests to ensure nothing breaks.

### Guidelines for writing clean code

- Adhere to the PEP 8 coding style guidelines.
- Keep functions and methods concise.
- Ensure your code is well-commented where necessary.
- Avoid hardcoding values.
- Ensure your code is modular and maintainable.

### Guidelines for submitting a Pull Request (PR)

1. Commit and push your changes using this format: git commit -m "Brief description of the changes"
2. Push changes to the right branch in GitHub: git push origin your-feature-branch
3. Open a Pull Request (PR) from your feature branch to the main branch. In the PR description, clearly explain:
    - The purpose of the changes.
    - Any issues or features your PR addresses (referencing issue numbers where applicable).
    - Any special steps required to test the changes.

## Guidelines for technical writers

- Clone the repository by cloning it to your machine, following the same steps as the development team.
- Work on the README.md, create a new branch for documentation updates: git checkout -b update-readme
- Commit your changes by using clear commit messages such as: git commit -m "Update README.md with installation instructions"
- Push your changes and open a Pull Request with the title "Update README.md: \[Description\]".

### Guidelines for updating the README.md

- Include sections for project overview, installation, usage, and contribution guidelines.
- Ensure instructions are purposeful, concise and clear for both developers and users.
- Use Markdown syntax properly and keep a consistent style.
- Ensure any technical terms or concepts are correctly explained.

### Guidelines for updating GitHub Pages

- All documentation updates for GitHub Pages are made within the docs/ directory.
- To create a new branch, work on a new branch for updating GitHub Pages content: git checkout -b update-github-pages
- When adding new guides or sections, create a new Markdown file (.md) inside the docs/ folder and update any navigation or index files.
- Maintain consistency by following the existing structure of the GitHub Pages site.
  - Use the same headings and formatting styles.
  - Keep the language purposeful, clear and concise.
- Preview your changes before submitting them.
- To submit a Pull Request, push your branch and open a Pull Request with the title "GitHub Pages Update: \[Description of Changes\]".

## General contribution guidelines

- Every pull request will be reviewed by at least one member of the team before merging. Make sure your PR is clearly explained and ready for review.
- Be open to feedback and revisions, whether it's for code, documentation, or formatting.

## Issues and communication

For any doubts, concerns or discussions, do not hesitate to reach to the team: [gtien@myseneca.ca](mailto:gtien@myseneca.ca).

# Contact information

For additional information that is not addressed in this documentation, please contact the technical writer team: [gtien@myseneca.ca](mailto:gtien@myseneca.ca).
