<!-- This page will show all the books currently in the database and allow for editing and deletion. -->


<template>
  <div>
    <navbar></navbar>
    <div class="table-container">
      <h2 style="text-align: center;">Books</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Book Name</th>
            <th>Book Authors</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td>{{ book.name }}</td>
            <td>{{ book.authors }}</td>
            <td>{{ book.price }}</td>
            <td>
              <button @click="editBook(book.id)" class="btn btn-outline-secondary">Edit</button>
              <button @click="confirmDelete(book.id)" class="btn btn-outline-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '../users/NavBar.vue';

export default {
  name: 'BooksTable',
  components: {
    Navbar
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
        const response = await axios.get('http://127.0.0.1:5000/allbooks');
        this.books = response.data;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    editBook(id) {
      this.$router.push({ name: 'EditBook', params: { id } });
    },
    confirmDelete(id) {
      this.$router.push({ name: 'DeleteBook', params: { id } });
    }
  }
};
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

.btn-success {
  background-color: #4CAF50;
  color: white;
}

.btn-success:hover {
  background-color: #45a049;
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
