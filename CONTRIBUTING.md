# Contributing Guidelines
Thank you for taking part of this project! Below, you will find specific guidelines for both the development and documentation teams.

## How to Contribute

## 1. For the Development Team (UDC)

### Cloning the Repository 

1. Clone your fork to your local machine:

        git clone https://github.com/your-username/your-repository.git

### Creating a New Branch for Your Changes 

2. Create a new branch for your feature or bug fix:

        git checkout -b your-feature-branch

    - Use descriptive branch names related to the feature or fix (e.g., feature/auth-system or bugfix/issue-123).

### Writing Clean Code 

3. Follow coding standards:

    - Adhere to the coding style guidelines for the project. For Python, follow PEP 8.
    - Keep functions and methods concise and ensure your code is well-commented where necessary.
    - Avoid hardcoding values and ensure your code is modular and maintainable.

### Running Tests 
    
4. Test your code before committing:

    - Run all existing tests to ensure nothing breaks.

### Submittin a Pull Request (PR) 

5. Commit and push your changes:

    - Ensure your commit messages are clear and follow this format:

            git commit -m "Brief description of the changes"

6. Push your branch to GitHub:

    - Double check you push your changes to the right branch.

            git push origin your-feature-branch

7. Open a Pull Request:

    - On GitHub, open a Pull Request (PR) from your feature branch to the main branch.
    - In the PR description, clearly explain:

        - The purpose of the changes.
        - Any issues or features your PR addresses (referencing issue numbers where applicable).
        - Any special steps required to test the changes.



## 2. For the Documentation Team (SENECA)

### Updating the README.md 

1. Cloning the repository:

    - Clone it to your machine, following the same steps as the development team.

2. Working on the README.md:

    - Create a new branch for documentation updates:

            git checkout -b update-readme
            
    - Keep the README.md well-structured:

        - Include sections for project overview, installation, usage, and contribution guidelines.
        - Ensure instructions are clear for both developers and users.

    - Formatting:

        - Use Markdown syntax properly and keep a consistent style.
        - Ensure any technical terms or concepts are correctly explained.

3. Commit your changes:

    - Use clear commit messages such as:
    - git commit -m "Update README.md with installation instructions"

4. Push your changes and open a Pull Request:

    - Push your branch to GitHub and open a Pull Request with the title "Update README.md: [Description]".
    - Provide a detailed explanation of the changes.


### Updating GitHub Pages (docs/ folder) 

1. GitHub Pages documentation:

    - All documentation updates for GitHub Pages are made within the docs/ directory.

2. Create a new branch:

    - Work on a new branch for updating GitHub Pages content:

            git checkout -b update-github-pages

3. Editing or adding new content:

    - Adding new documentation: When adding new guides or sections, create a new Markdown file (.md) 
      inside the docs/ folder and update any navigation or index files.

    - Maintaining consistency: Follow the existing structure of the GitHub Pages site to ensure consistency. For example:
        - Use the same headings and formatting styles.
        - Keep the language clear and concise.


4. Preview changes locally:

    - Preview your changes before submitting them:

5. Submit a Pull Request:

    - Push your branch and open a Pull Request with the title "GitHub Pages Update: [Description of Changes]".
    - Describe what content was added or modified and provide any relevant context for reviewers or members of the project.


## 3. General Contribution Guidelines

### Reviewing and Merging

- Pull Request Review: Every PR will be reviewed by at least one member of the team before merging. Make sure your PR is clearly explained and ready for review.
- Feedback and Revisions: Be open to feedback and revisions, whether it's for code, documentation, or formatting.

### Issues and Communication 

- For any doubts, concerns or discussions, do not hesitate to reach the channels of communitation stablished by the team members.