<!-- This page will show all the books that have been issued to users -->

<template>
    <div>
      <navbar></navbar>
      <div class="table-container">
        <div v-if="filteredBooks.length > 0">
          <h2 style="text-align: center;">Currently Issued Books to Users</h2>
          <table class="table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Book Name</th>
                <th>Book Authors</th>
                <th>Issue Date</th>
                <th>Return Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="book in filteredBooks" :key="book.id">
                <td>{{ book.user_name }}</td>
                <td>{{ book.book_name }}</td>
                <td>{{ book.book_author }}</td>
                <td>{{ book.issue_date }}</td>
                <td>{{ book.return_date }}</td>
                <td>
                  <button @click="updateStatus(book.id, 'revoked')" class="btn btn-outline-danger">Revoke</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          <h3><p><strong>You have not issued any books.</strong></p></h3>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Navbar from '../users/NavBar.vue';
  import { useToast } from 'vue-toastification';
  
  export default {
    name: 'IssuedBooks',
    components: {
      Navbar
    },
    computed: {
      filteredBooks() {
        return this.books.filter(book => book.status === 'accepted');
      }
    },
    data() {
      return {
        books: []
      };
    },
    async created() {
      this.fetchBooks();
    },
    methods: {
      async fetchBooks() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/get/book_requests');
          this.books = response.data;
        } catch (error) {
          console.error('Error fetching requests', error);
        }
      },
      async updateStatus(bookId, status) {
        const toast = useToast();
        try {
          const response = await axios.post(`http://127.0.0.1:5000/book_requests/${bookId}/status`, { status });
          // alert(response.data.message);
          toast.success(response.data.message, {
            position: "top-right",
            timeout: 3000
          })
          this.fetchBooks(); // Refresh the request list after updating status
        } catch (error) {
          console.error('Error updating request status', error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .table-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .table th, .table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  .table th {
    background-color: #f2f2f2;
    font-weight: bold;
  }
  
  .table td {
    background-color: #fff;
  }
  
  .btn {
    padding: 5px 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    margin-right: 5px;
    text-align: center;
    transition: background-color 0.3s;
  }
  
  .btn-outline-secondary {
    background-color: #f9f9f9;
    color: #000;
    border: 1px solid #ccc;
  }
  
  .btn-outline-secondary:hover {
    background-color: #e9e9e9;
  }
  
  .btn-outline-danger {
    background-color: #f9f9f9;
    color: #f44336;
    border: 1px solid #f44336;
  }
  
  .btn-outline-danger:hover {
    background-color: #f44336;
    color: white;
  }
  </style>
  