<!-- This page will diplay user all the books which he have issued currently along with option to read , return, and give feedback -->

<template>
  <div>
    <navbar></navbar>
    <div class="issued-books-container">
      <h2 style="text-align: center;">Books You Currently Have Issued</h2>
      <div v-if="filteredBooks.length > 0">
        <table class="table">
          <thead>
            <tr>
              <th>Book Name</th>
              <th>Book Authors</th>
              <th>Issue Date</th>
              <th>Return Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in filteredBooks" :key="book.id">
              <td>{{ book.book_name }}</td>
              <td>{{ book.book_author }}</td>
              <td>{{ book.issue_date }}</td>
              <td>{{ book.return_date }}</td>
              <td>
                <button @click="readBook(getBookId(book.book_name))" class="btn btn-outline-success">Read</button>
                <button @click="updateStatus(book.id, 'returned')" class="btn btn-outline-danger">Return</button>
                <button @click="goToFeedbackPage(book.id)" class="btn btn-outline-warning">Feedback</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <h3 style="text-align: center;">You have not issued any books.</h3>
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
      books: [],
      allbooks: []
    };
  },
  async created() {
    await this.fetchBooks();
    await this.fetchAllBooks();
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
    async fetchAllBooks() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/books`);
        this.allbooks = response.data;
      } catch (error) {
        console.error('Error fetching books', error);
      }
    },
    async updateStatus(bookId, status) {
      const toast = useToast();
      try {
        const response = await axios.post(`http://127.0.0.1:5000/book_requests/${bookId}/status`, { status });
        toast.success(response.data.message, {
          position: "top-right",
          timeout: 5000
        });
        this.fetchBooks();
      } catch (error) {
        console.error('Error updating request status', error);
      }
    },
    getBookId(bookName) {
      const book = this.allbooks.find(book => book.name === bookName);
      return book ? book.id : null;
    },
    readBook(bookId) {
      if (bookId) {
        this.$router.push({ name: 'ReadBook', params: { id: bookId } });
      } else {
        console.error('Book ID not found for the given book name.');
      }
    },
    goToFeedbackPage(bookId) {
      this.$router.push({ name: 'GiveFeedback', params: { id: bookId } });
    }
  }
}
</script>

<style scoped>
.issued-books-container {
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

.btn-outline-success {
  background-color: #f9f9f9;
  color: #4CAF50;
  border: 1px solid #4CAF50;
}

.btn-outline-success:hover {
  background-color: #4CAF50;
  color: white;
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

.btn-outline-warning {
  background-color: #f9f9f9;
  color: #ff9800;
  border: 1px solid #ff9800;
}

.btn-outline-warning:hover {
  background-color: #ff9800;
  color: white;
}
</style>
