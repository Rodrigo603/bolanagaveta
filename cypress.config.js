const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      return config;
    },
    baseUrl: "http://127.0.0.1:8000/",
    viewportWidth: 1920,
    viewportHeight: 1080,
    watchForFileChanges: false,
    specPattern: 'cypress/e2e/**/*.cy.js', 
    retries: 2, 
    video: false, 
    execTimeout: 60000, 
    failOnNonZeroExit: false, 
  },
});