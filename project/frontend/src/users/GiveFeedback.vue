<!-- This is a page where user can give feedback for a book -->

<template>
  <div>
    <navbar></navbar>
    <div class="feedback-container">
      <h2>Submit Feedback for Book ID: {{ bookId }}</h2>
      <form @submit.prevent="submitFeedback">
        <div class="form-group">
          <label for="feedback">Feedback:</label>
          <textarea v-model="feedback" id="feedback" class="form-control" rows="5" required></textarea>
        </div>
        <button type="submit" class="btn btn-outline-primary">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';
import Navbar from './NavBar.vue';

export default {
  name: 'GiveFeedback',
  components: {
    Navbar
  },
  data() {
    return {
      bookId: this.$route.params.id,
      feedback: ''
    };
  },
  methods: {
    async submitFeedback() {
      const toast = useToast();
      try {
        const response = await axios.post(`http://127.0.0.1:5000/book_requests/${this.bookId}/feedback`, { feedback: this.feedback });
        toast.success(response.data.message, {
          position: "top-right",
          timeout: 5000
        });
        this.$router.push({ name: 'IssuedBooks' });
      } catch (error) {
        console.error('Error submitting feedback', error);
      }
    }
  }
};
</script>

<style scoped>
.feedback-container {
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

.btn {
  display: inline-block;
  padding: 10px 20px;
  margin-top: 10px;
  font-size: 14px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 5px;
}

.btn-outline-primary {
  background-color: #f9f9f9;
  color: #007bff;
  border: 1px solid #007bff;
}

.btn-outline-primary:hover {
  background-color: #007bff;
  color: white;
}
</style>
