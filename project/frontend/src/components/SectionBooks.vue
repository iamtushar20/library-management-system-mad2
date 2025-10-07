<!-- This page will display the list of books in a particular section -->

<template>
  <div>
    <navbar></navbar>
    <div class="table-container">
      <div v-if="books.length > 0">
          <h2 style="text-align: center;">List of books in this section{{sectionname}}</h2>
          <router-link :to="{ name: 'AddBook', params: { sectionId: sectionId } }" class="btn btn-add-book">Add Book</router-link><br><br>
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
                  <button @click="deleteBook(book.id)" class="btn btn-danger">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <button @click="goBack" class="btn btn-outline-secondary">Back</button>
      </div>
      <div v-else>
        <h3><p><strong>No books have been added in this section.</strong></p></h3>
        <router-link :to="{ name: 'AddBook', params: { sectionId: sectionId } }" class="btn btn-add-book">Add Book</router-link><br><br>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '../users/NavBar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      sectionId: null,
      books: [],
      sectionname: ''
    };
  },
  async created() {
    
    this.sectionId = this.$route.params.id;
    this.fetchBooks();
  },
  methods: {
    async fetchBooks() {
      try {
        let id = this.$route.params.id;
        const response = await axios.get(`http://127.0.0.1:5000/section/books/${id}`);
        this.books = response.data;
        sectionname = response.data[0].section_id.name
        console.log(this.sectionname)
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    editBook(id) {
      this.$router.push({ name: 'EditBook', params: { id } });
    },
    deleteBook(id) {
      this.$router.push({ name: 'DeleteBook', params: { id } });
    },
    goBack() {
      this.$router.go(-1);
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

.btn-danger {
  background-color: #f44336;
  color: white;
}

.btn-danger:hover {
  background-color: #da190b;
}

.btn-add-book {
  display: inline-block;
  margin-bottom: 15px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn-add-book:hover {
  background-color: #0056b3;
}
</style>
