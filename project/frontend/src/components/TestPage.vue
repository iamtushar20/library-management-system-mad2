<template>
    <!-- <BaseLayout /> -->
    <BaseLayout>
      <div>
        <h1>Test Page</h1>
        <p>This is a test page content.</p>
      </div>
    </BaseLayout>
  </template>
  
  <script>
  import BaseLayout from './BaseLayout.vue'; // Adjust the path as needed
  
  export default {
    name: 'TestPage',
    components: {
      BaseLayout,
    },
  };
  </script>
  
  <style scoped>
  /* Add component-specific styles here if needed */
  </style>
  