// frontend/taskmaster.config.js
export default {
  project: {
    name: "SOA Loyalty Frontend",
    description: "Frontend service for the SOA Loyalty application",
  },
  ai: {
    provider: "openai", // or your preferred AI provider
    model: "gpt-4", // or your preferred model
  },
  // Add any specific configurations for your project
  paths: {
    src: "./src/*",
    components: "./src/components",
    pages: "./src/pages",
  },
};
