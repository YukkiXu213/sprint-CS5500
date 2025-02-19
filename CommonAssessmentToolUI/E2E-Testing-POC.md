# E2E Testing with Cypress: Proof of Concept

## Overview
This document outlines the proof of concept (POC) for implementing end-to-end (E2E) testing in our React application using Cypress. It provides details on the setup, configuration, and the basic test that has been checked in.

## Goals
- Evaluate Cypress as the E2E testing framework for our React application.
- Demonstrate the feasibility of implementing E2E tests.
- Set up a foundation for future E2E test coverage.

## Setup and Configuration
1. **Install Cypress**:
   ```bash
   npm install --save-dev cypress

2. **Open Cypress**:
   ```bash
   npx cypress open

3. **Add Cypress Scripts to package.json**:
   ```json
   "scripts": {
    "cypress:open": "cypress open",
    "cypress:run": "cypress run"
    }

## Understanding the flow
  - Client Retrieval:
    - Navigate to /clients.
    - Search for a client by name.
    - Validate the search results.
  - Client Detail Update:
    - Select a client and navigate to /client/:id.
    - Modify client details and validate the changes.
  - Score Calculation:
    - Submit the updated client details.
    - Validate the generated score and interventions on /results.

## Identifying Test Scenarios
Test user interactions across different pages:
  - Landing Page:
    - Verify navigation buttons (New Entry, Upload PDF/CSV, etc.).
  - Client Search:
    - Test search functionality and ensure valid/invalid search inputs return expected results.
  - Detail Page:
    - Test editing client details.
    - Ensure data validation (e.g., age limits, required fields).
  - Result Page:
    - Validate the return-to-work probability and interventions.
    - Ensure that buttons like "Save as PDF" and "Back to Form" work correctly.

## Mock Api calls
- Mock server responses for client retrieval and updates to make tests deterministic.
- Use cy.intercept() to stub API responses:

## Test Environment Configuration
Add environment variables for base URLs and API endpoints in cypress.config.js:

```js
module.exports = {
  e2e: {
    baseUrl: 'http://localhost:3000',
    setupNodeEvents(on, config) {
      // Implement node event listeners here
    },
  },
};
```
## Create Fixtures:
Add JSON fixtures for mock data in the cypress/fixtures directory:
- In our case : added clientSearch.json: Mock data for clients.

## Sample test workflow:

- A sample test for search functionality is written in ClientSearch.cy.js file.
- In order to run that there are 3 ways:

  - **Run tests using the Cypress GUI**:
     ```bash
     npx cypress open
     ```
   
  - **Run tests headlessly**:
     ```bash
     npx cypress run
      ```

  - **Run specific test**:
     ```bash
     npx cypress run --spec cypress/e2e/client/clientSearch.cy.js
      ```

## Sample images of testing workflow

- When we run ```npx cypress open```, we see this:

  <img width="1196" alt="image" src="https://github.com/user-attachments/assets/03fb4ca0-aec7-4315-80a0-fe5f2a24e46e">

- Click on ```E2E testing```, since we have configured that. Then we see this:
  
  <img width="1194" alt="image" src="https://github.com/user-attachments/assets/558047b0-fa36-4fdd-b3d9-f3d1ffa303b3">
  
- Any browser can be selected among the listed ones. I chose chrome and clicked on ```Start E2E Testing in Chrome```. So I see this:
  
  <img width="1724" alt="image" src="https://github.com/user-attachments/assets/daab71df-b2cc-407d-a424-13f4ede6c24b">

- Click on ```clientSearch.cy.js```. Then we run the tests in that file and see logs and output and other details like this:

  <img width="1728" alt="image" src="https://github.com/user-attachments/assets/327b9ab4-b44b-48be-a443-662850a50ba7">







