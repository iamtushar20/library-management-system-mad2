<!-- This page is the confirmation page for deleting a book -->

<template>
  <div>
    <navbar></navbar>
    <div class="delete-book-container">
      <h2 style="text-align: center;">Delete Book</h2>
      <strong><p>Are you sure you want to delete this <b>"{{ book.name }}"</b> book?</p></strong>
      <div class="buttons">
        <button @click="deleteBook" class="btn btn-danger">Delete</button>
        <button @click="goBack" class="btn btn-outline-secondary">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '../users/NavBar.vue';
import { useToast } from 'vue-toastification';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      book: {}
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
    async deleteBook() {
      const id = this.$route.params.id;
      const toast = useToast();
      try {
        await axios.delete(`http://127.0.0.1:5000/api/books/${id}`);
        this.$router.push(`/sectionbook/${this.book.section_id}`);
        toast.success('Book deleted successfully!',{
          timeout: 2000,
        })
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    },
    goBack() {
      this.$router.go(-1);
    }
  }
}
</script>

<style scoped>
.delete-book-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
}

p {
  font-size: 18px;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}

.btn-danger:hover {
  background-color: #da190b;
}

.btn-outline-secondary {
  background-color: #f9f9f9;
  color: #000;
  border: 1px solid #ccc;
}

.btn-outline-secondary:hover {
  background-color: #e9e9e9;
}
</style>
