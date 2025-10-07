<!-- This page is about updation of a book -->

<template>
  <div>
    <navbar></navbar>
    <div class="form-container">
      <h2 style="text-align: center;">Edit Book</h2>
      <form @submit.prevent="updateBook" class="book-form">
        <div class="form-group">
          <label for="name">Book Name</label>
          <input type="text" id="name" v-model="book.name" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="authors">Book Authors</label>
          <input type="text" id="authors" v-model="book.authors" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="content">Book Content</label>
          <input type="text" id="content" v-model="book.content" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="price">Price</label>
          <input type="number" id="price" v-model="book.price" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="date_added">Date Added</label>
          <input type="date" id="date_added" v-model="book.date_added" class="form-control" required>
        </div>
        <button type="submit" class="btn-submit">Update Book</button>
        <button @click="goBack" class="btn-outline-secondary">Back</button>
      </form>
    </div>
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
        name: '',
        authors: '',
        content: '',
        price: '',
        date_added: ''
      }
    };
  },
  async created() {
    const id = this.$route.params.id;
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/books/${id}`);
      this.book = response.data;
    } catch (error) {
      console.error('Error fetching book:', error);
    }
  },
  methods: {
    async updateBook() {
      const toast = useToast();
      const id = this.$route.params.id;
      try {
        await axios.put(`http://127.0.0.1:5000/api/books/${id}`, this.book);
        this.$router.push(`/sectionbook/${this.book.section_id}`);
      } catch (error) {
        console.error('Error updating book:', error);
        toast.error(error.response.data.message, {
          position: "top-right",
          timeout: 3000
        });
      }
    },
    goBack() {
      this.$router.go(-1);
    }
  }
}
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

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
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

.btn-outline-secondary {
  padding: 10px 20px;
  background-color: #f9f9f9;
  color: #000;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  font-size: 16px;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.btn-outline-secondary:hover {
  background-color: #e9e9e9;
}
</style>
