<template>
    <div class="dashboard">
      <h1>Export Accepted Transactions</h1>
      <button @click="triggerExport">Export as CSV</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserDashBoard',
    methods: {
      async triggerExport() {
        try {
          const response = await fetch('http://127.0.0.1:5000/export_transactions', {
            method: 'GET'
          });
  
          if (!response.ok) {
            throw new Error('Network response was not ok.');
          }
  
          const blob = await response.blob();
          const url = window.URL.createObjectURL(new Blob([blob]));
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = url;
          a.download = 'accepted_transactions.csv';
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
        } catch (error) {
          console.error('There was a problem with the fetch operation:', error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .dashboard {
    text-align: center;
    margin-top: 50px;
  }
  
  button {
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
  }
  </style>
  