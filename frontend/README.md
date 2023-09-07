# Project Name

UI of the Doc Generator

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

Following features are implemented:

1. **Landing Page:** The homepage of the UI from which the user can navigate to the real-time rendering of documents page or login/signup to access dashboard.

2. **Document Generator Page:**
   - Renders templates in real-time.
   - User enters the Template type, Template input, output type, and data. Submit the data to start rendering.
     Note: choose from existing templates at the moment works only for creating a batch of docs.
   - Example of inputs:<br>
   ```
     Template Type: JSTL
     Template Input: "${name}"
     Data: {"name" : "abc"}
   ```
3. **Dashboard:**
   - View all submitted batches of documents.
   - Create a batch of documents with a template ID from existing templates. Add more data input using the + button. The data is sent as an array of JSON objects.
   - Example:<br>
   ```
     Template Type: JINJA
     Template Input: *choose one form the existing templates*
     Data: {"variable_name" : "value"}
   ```
   - Search, filter based on status, and share functionality needs to be implemented.

## Tech Stack

- **Next.js:** This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).
  This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.
- **Other technologies or libraries:** Axios, react-dom, react-icons.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-project.git
   cd Doc-generator/frontend/
   ```

2. Install dependencies:

   ```bash
   npm install
   # or
   yarn add
   ```

3. Start the development server:

   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

**NOTE: For the API integrations to work, start the server in another port.**

## Usage

To access the Landing Page, open your browser and navigate to http://localhost:3000/.

To use the Document Generator Page, navigate to http://localhost:3000/generator
(can be navigated from the landing page)

To use the Dashboard Page, navigate to http://localhost:3000/dashboard

To use the Create batches of doc Page, navigate to http://localhost:3000/createBatches
(can be navigated from the dashboard)

## Contributing

We welcome contributions from the community to improve and enhance this project. Please follow these guidelines when contributing:

1. Fork the project repository to your GitHub account.

2. Clone your forked repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-project.git
   cd your-project/
   ```

**Branching Strategy**
Create a new branch for each contribution or issue you're working on. Name your branch with a descriptive, lowercase, and hyphen-separated title, like feature/new-feature or bugfix/fix-issue.

**Commit Guidelines**
Follow conventional commit messages to format your commits. This helps with automatic versioning and generating changelogs.

**Pull Requests**

- Create a pull request (PR) when you're ready to submit your changes.
- Provide a clear and descriptive title and description for your PR.
- Reference any related issues or pull requests in the description using GitHub's syntax (e.g., "Closes #123").

**Code Review**

- A project maintainer will review your changes, and you may need to make additional updates based on their feedback.
- Always write clear and concise commit messages that explain the purpose and scope of your changes.

**Documentation**
If your contribution introduces new features, update the project's documentation to reflect these changes.
