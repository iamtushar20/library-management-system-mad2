<!-- This page will display the status of all the books to whom it have been issued and will also display the feedback of the books -->

<template>
  <navbar></navbar>
  <div class="all-book-status">
    
    <h1 style="text-align: center;">All Accepted Books</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Book Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in uniqueBooks" :key="book.book_name">
          <td>{{ book.book_name }}</td>
          <td>
            <button @click="goToStatusPage(book.book_name)" class="btn btn-status">Status</button>
            <button @click="goToFeedbackPage(book.book_name)" class="btn btn-feedback">Feedback</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '../users/NavBar.vue';

export default {
  name: 'AllBookStatus',
  components: {
    Navbar
  },
  data() {
    return {
      books: [],
      uniqueBooks: []
    };
  },
  async created() {
    await this.fetchBooks();
    this.filterUniqueAcceptedBooks();
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/transactions');
        this.books = response.data;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    filterUniqueAcceptedBooks() {
      const acceptedBooks = this.books.filter(book => book.status === 'accepted');
      const uniqueBooksMap = new Map();
      acceptedBooks.forEach(book => {
        if (!uniqueBooksMap.has(book.book_name)) {
          uniqueBooksMap.set(book.book_name, book);
        }
      });
      this.uniqueBooks = Array.from(uniqueBooksMap.values());
    },
    goToStatusPage(bookName) {
      this.$router.push({ name: 'CheckStatus', params: { bookName } });
    },
    goToFeedbackPage(bookName) {
      this.$router.push({ name: 'SeeFeedback', params: { bookName } });
    }
  }
};
</script>

<style scoped>
.all-book-status {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
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

.btn-status {
  background-color: #4CAF50; 
  color: white;
}

.btn-status:hover {
  background-color: #45a049;
}

.btn-feedback {
  background-color: #f0ad4e; 
  color: white;
}

.btn-feedback:hover {
  background-color: #ec971f;
}
</style>
