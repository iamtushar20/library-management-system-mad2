<!-- This page will allow admin to add a book to a section -->

<template>
  <navbar></navbar>
  <div class="form-container">
    <h2>Add Book to Section</h2>
    <form @submit.prevent="addBook" class="book-form">
      <label for="name">Name:</label>
      <input type="text" id="name" v-model="book.name" required>
      
      <label for="content">Content:</label>
      <textarea id="content" v-model="book.content" required></textarea>
      
      <label for="authors">Authors:</label>
      <input type="text" id="authors" v-model="book.authors" required>
      
      <label for="date_added">Date Added:</label>
      <input type="date" id="date_added" v-model="book.date_added" required>
      
      <label for="price">Price:</label>
      <input type="number" id="price" v-model="book.price" required>
      
      <button type="submit" class="btn-submit">Add Book</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';
import Navbar from '../users/NavBar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      book: {
        section_id: this.$route.params.sectionId,
        name: '',
        content: '',
        authors: '',
        date_added: '',
        price: null
      }
    };
  },
  methods: {
    async addBook() {
      const toast = useToast();
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/books', this.book);
        console.log('Book added:', response.data);
        let sectionId = this.$route.params.sectionId;
        this.$router.push(`/sectionbook/${sectionId}`);
      } catch (error) {
        console.error('Error adding book:', error);
        toast.error(error.response.data.message, {
                    position: "top-right",
                    timeout: 3000
                });
      }
    }
  }
};
</script>

<style>
.form-container {
  max-width: 600px;
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

.book-form {
  display: flex;
  flex-direction: column;
}

.book-form label {
  margin-bottom: 5px;
  font-weight: bold;
}

.book-form input,
.book-form textarea {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.book-form textarea {
  resize: vertical;
}

.btn-submit {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-submit:hover {
  background-color: #45a049;
}
</style>
