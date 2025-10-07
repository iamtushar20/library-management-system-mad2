<!-- This is a buying book page, where user will pay the price for the book and go to download book page -->

<template>
  <div>
    <navbar></navbar>
    <div class="buy-form-container">
      <h2>Buy a Book</h2>
      <form @submit.prevent="goToReadBook">
        <label for="bookName">Book Name:</label>
        <input type="text" id="bookName" v-model="book.name" readonly class="form-control" />

        <label for="bookAuthor">Book Author:</label>
        <input type="text" id="bookAuthor" v-model="book.authors" readonly class="form-control" />

        <label for="bookPrice">Price:</label>
        <input type="text" id="bookPrice" v-model="book.price" readonly class="form-control" />

        <button type="submit" class="btn btn-outline-success">Pay Rs. {{ book.price }}</button>
        <button type="button" @click="cancel" class="btn btn-outline-danger">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './NavBar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      book: {
        name: '',
        authors: '',
        price: null,
        content: ''
      }
    };
  },
  mounted() {
    this.fetchBookDetails();
  },
  methods: {
    async fetchBookDetails() {
      try {
        const bookId = this.$route.params.id; 
        const response = await axios.get(`http://127.0.0.1:5000/api/books/${bookId}`);
        const book = response.data;
        this.book.name = book.name;
        this.book.authors = book.authors;
        this.book.price = book.price;
        this.book.content = book.content;
      } catch (error) {
        console.error('Error fetching book details:', error.response.data);
      }
    },
    goToReadBook() {
      this.$router.push({ name: 'DownloadBook', params: { id: this.$route.params.id } });
    },
    cancel() {
      this.$router.push('/userhome'); 
    }
  }
}
</script>

<style scoped>
.buy-form-container {
  max-width: 500px;
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

.form-control {
  display: block;
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 5px;
  margin-right: 5px;
  transition: background-color 0.3s;
}

.btn-outline-success {
  background-color: #f9f9f9;
  color: #28a745;
  border: 1px solid #28a745;
}

.btn-outline-success:hover {
  background-color: #28a745;
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
</style>
