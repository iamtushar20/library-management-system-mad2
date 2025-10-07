<!-- This is the page where user can see the request he or she have made and can cancel it also . -->

<template>
    <div>
      <navbar></navbar>
      <div class="table-container">
        <h2 style="text-align: center;">Your Pending Requests</h2>
        <div v-if="filteredBooks.length > 0">
          <table class="table">
            <thead>
              <tr>
                <th>Book Name</th>
                <th>Book Authors</th>
                <th>Request Date</th>
                <th>Return Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="book in filteredBooks" :key="book.id">
                <td>{{ book.book_name }}</td>
                <td>{{ book.book_author }}</td>
                <td>{{ book.request_date }}</td>
                <td>{{ book.return_date }}</td>
                <td>{{ book.status }}</td>
                <td>
                  <button @click="updateStatus(book.id, 'cancelled')" class="btn btn-outline-danger">Cancel</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          <h3 style="text-align: center;"><strong>You do not have any pending requests currently.</strong></h3>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useToast } from 'vue-toastification';
  import Navbar from './NavBar.vue';
  
  export default {
    name: 'IssuedBooks',
    data() {
      return {
        books: [],
      };
    },
    computed: {
      filteredBooks() {
        return this.books.filter(book => book.status === 'pending');
      }
    },
    components: {
      Navbar
    },
    async created() {
      this.fetchBooks();
    },
    methods: {
      async fetchBooks() {
        try {
          const username = localStorage.getItem('username');
          const response = await axios.get(`http://127.0.0.1:5000/api/get/book_requests?username=${username}`);
          this.books = response.data;
        } catch (error) {
          console.error('Error fetching requests', error);
        }
      },
      async updateStatus(bookId, status) {
        const toast = useToast();
        try {
          const response = await axios.post(`http://127.0.0.1:5000/book_requests/${bookId}/status`, { status });
          toast.success(response.data.message, {
            position: "top-right",
            timeout: 3000
          });
          this.fetchBooks();
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
  