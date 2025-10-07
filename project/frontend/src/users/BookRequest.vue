<!-- This is a page where user can request a book -->

<template>
  <div>
    <navbar></navbar>
    <div class="request-form-container">
      <h2>Request a Book</h2>
      <form @submit.prevent="submitRequest">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required class="form-control" />

        <label for="bookName">Book Name:</label>
        <input type="text" id="bookName" v-model="bookName" required class="form-control" :readonly="readonlyBookName" />

        <label for="authors">Authors:</label>
        <input type="text" id="authors" v-model="authors" required class="form-control" :readonly="readonlyAuthors" />

        <label for="requestDate">Request Date:</label>
        <input type="date" id="requestDate" v-model="requestDate" required class="form-control" />

        <label for="returnDate">Return Date:</label>
        <input type="date" id="returnDate" v-model="returnDate" required class="form-control" />

        <button type="submit" class="btn btn-primary">Request</button>
        <button @click="goBack" class="btn btn-outline-secondary">Back</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';
import Navbar from './NavBar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      username: '',
      bookName: '',
      authors: '',
      requestDate: '',
      returnDate: '',
      readonlyBookName: false,
      readonlyAuthors: false
    };
  },
  mounted() {
    
    this.fetchBookDetails();
  },
  methods: {
    async fetchBookDetails() {
      try {
        const username = localStorage.getItem('username');
        const bookId = this.$route.params.id; 
        const response = await axios.get(`http://127.0.0.1:5000/api/books/${bookId}`);
        const book = response.data;
        this.username = username;
        this.bookName = book.name;
        this.authors = book.authors;
        this.readonlyBookName = true; 
        this.readonlyAuthors = true; 
      } catch (error) {
        console.error('Error fetching book details:', error.response.data);
      }
    },
    async submitRequest() {
      const toast = useToast();
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/book_requests', {
          user_name: this.username,
          book_name: this.bookName,
          request_date: this.requestDate,
          return_date: this.returnDate,
          book_author: this.authors,
          status: 'pending'
        });
        toast.success('Book Request Submitted Successfully!', {
          position: "top-right",
          timeout: 3000
        });
        this.$router.push('/userhome');
        this.clearForm();
      } catch (error) {
        console.error('Error submitting request:', error.response.data);
        toast.error(error.response.data.error, {
          position: "top-right",
          timeout: 4000
        });
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    clearForm() {
      this.username = '';
      this.bookName = '';
      this.authors = '';
      this.requestDate = '';
      this.returnDate = '';
      this.readonlyBookName = false; 
      this.readonlyAuthors = false; 
    }
  }
};
</script>

<style scoped>
.request-form-container {
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

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-outline-secondary {
  background-color: #f9f9f9;
  color: #6c757d;
  border: 1px solid #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}
</style>
