<!-- This page is the dashboard page for admin where he can see two bar graphs and one pie chart along with user triggered csv export part. -->

<template>
    <div>
      <navbar></navbar>
      <div class="dashboard-container">
        <h2 class="dashboard-title">Admin Dashboard</h2>
        <div class="charts-container">
          <div class="chart card">
            <h3>Total Counts</h3>
            <canvas id="barChart"></canvas>
          </div>
          <div class="chart card">
            <h3>Books per Section</h3>
            <canvas id="pieChart"></canvas>
          </div>
          <div class="chart card">
            <h3>Top 5 Issued Books</h3>
            <canvas id="topBooksChart"></canvas>
          </div>
        </div>
        <div class="export-container">
          <h3>Export CSV</h3>
          <button @click="triggerExport" class="btn btn-primary">Export as CSV</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { Bar, Pie } from 'vue-chartjs';
  import Chart from 'chart.js/auto';
  import Navbar from '../users/NavBar.vue';
  
  export default {
    name: 'AdminDashboard',
    components: {
      BarChart: Bar,
      PieChart: Pie,
      Navbar
    },
    data() {
      return {
        stats: {},
        sectionBooks: [],
        topIssuedBooks: []
      };
    },
    async created() {
      await this.fetchAdminStats();
      await this.fetchSectionBooks();
      await this.fetchTopIssuedBooks();
      this.renderCharts();
    },
    methods: {
      async fetchAdminStats() {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/stats');
        this.stats = response.data;
      },
      async fetchSectionBooks() {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/section_books');
        this.sectionBooks = response.data;
      },
      async fetchTopIssuedBooks() {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/top_issued_books');
        this.topIssuedBooks = response.data;
      },
      renderCharts() {
        this.renderBarChart();
        this.renderPieChart();
        this.renderTopBooksChart();
      },
      renderBarChart() {
        const ctx = document.getElementById('barChart').getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Users', 'Sections', 'Books', 'Pending Requests', 'Issued Books'],
            datasets: [{
              label: 'Count',
              data: [
                this.stats.total_users,
                this.stats.total_sections,
                this.stats.total_books,
                this.stats.total_pending_requests,
                this.stats.total_issued_books
              ],
              backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff']
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      },
      renderPieChart() {
        const ctx = document.getElementById('pieChart').getContext('2d');
        new Chart(ctx, {
          type: 'pie',
          data: {
            labels: this.sectionBooks.map(section => section.section),
            datasets: [{
              data: this.sectionBooks.map(section => section.book_count),
              backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#ff9f40']
            }]
          },
          options: {
            responsive: true
          }
        });
      },
      renderTopBooksChart() {
        const ctx = document.getElementById('topBooksChart').getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: this.topIssuedBooks.map(book => book.name),
            datasets: [{
              label: 'Issue Count',
              data: this.topIssuedBooks.map(book => book.issue_count),
              backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff']
            }]
          },
          options: {
            responsive: true,
            indexAxis: 'x',  // Display vertically (along the x-axis)
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      },
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
          a.download = 'Book Transaction.csv';
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
        } catch (error) {
          console.error('There was a problem with the fetch operation:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .dashboard-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .dashboard-title {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .charts-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 20px;
  }
  
  .chart {
    flex: 1;
    min-width: 300px;
    max-width: 45%;
    text-align: center;
  }
  
  .chart canvas {
    width: 100% !important;
    height: auto !important;
  }
  
  h3 {
    text-align: center;
    margin-bottom: 10px;
  }
  
  .export-container {
    text-align: center;
    margin-top: 50px;
  }
  
  button {
    background-color: #4CAF50;
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
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  