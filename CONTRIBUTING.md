# **Contributing to GMF Investments Portfolio Optimization Project**

Thank you for your interest in contributing to this project\! We welcome and appreciate all contributions, from code enhancements to documentation improvements. By following these guidelines, you can help us maintain a high-quality codebase and a collaborative environment.

## **Code of Conduct**

We are committed to providing a welcoming and inclusive community. Please review and adhere to our [Code of Conduct](https://www.google.com/search?q=CODE_OF_CONDUCT.md).

## **How to Contribute**

### **1\. Fork the Repository**

First, you'll need to create your own copy of the repository.

1. Go to the main project page.  
2. Click the "Fork" button in the top right corner.

### **2\. Clone Your Fork**

Clone your forked repository to your local machine using the following command, replacing \<your-username\> with your GitHub username:

git clone https://github.com/\<your-username\>/gmf-portfolio-optimization.git

### **3\. Create a New Branch**

Create a new branch for your feature or bug fix. Use a descriptive name for your branch, for example: feat/add-lstm-model or fix/handle-missing-data.

git checkout \-b your-branch-name

### **4\. Make Your Changes**

Implement your changes, whether it's adding new features, fixing bugs, or improving documentation.

* **Follow the Project Structure:** Adhere to the existing directory structure (src/, notebooks/, scripts/, dashboard/).  
* **Write Clean Code:** Ensure your code is well-commented, readable, and follows Python's [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.  
* **Update Documentation:** If you add a new feature or change existing functionality, please update the relevant documentation, including docstrings and markdown files.

### **5\. Write Professional Git Commit Messages**

We use a specific format for our commit messages to maintain a clean and understandable history. Please follow the [**Conventional Commits**](https://www.conventionalcommits.org/en/v1.0.0/) specification.

* **Format**: \<type\>: \<description\>  
* **Types**:  
  * feat: A new feature  
  * fix: A bug fix  
  * docs: Documentation only changes  
  * style: Code formatting changes (whitespace, semicolons, etc.)  
  * refactor: A code change that neither fixes a bug nor adds a feature  
  * test: Adding missing tests or correcting existing tests  
  * chore: Changes to the build process or auxiliary tools and libraries

**Example:**

feat: Add LSTM model for forecasting

This commit introduces a new LSTM model to the forecasting pipeline.  
The model is trained in \`src/modeling.py\` and evaluated alongside the existing ARIMA model.

### **6\. Push Your Changes**

Once your changes are ready, push them to your forked repository:

git add .  
git commit \-m "feat: Add your commit message here"  
git push origin your-branch-name

### **7\. Create a Pull Request (PR)**

After pushing your changes, open a pull request from your forked repository to the main branch of this project.

* **Provide a Clear Title:** Use the same Conventional Commit format for your PR title.  
* **Describe Your Changes:** In the PR description, explain the purpose of your changes, any new features, or how a bug was fixed. This helps reviewers understand your work.  
* **Reference Issues:** If your PR addresses a specific issue, mention it in the description (e.g., "Closes \#123").

## **Feedback and Suggestions**

If you find a bug or have an idea for a new feature, please open an issue on the repository. We appreciate all feedback and use it to improve the project.

Thank you for your contribution\!