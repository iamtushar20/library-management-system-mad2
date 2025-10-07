<!-- This is the page where user is redirected after paying for a book to download it -->

<template>
  <div>
    <navbar></navbar>
    <div class="book-container">
      <h2>{{ book.name }}</h2>
      <p>{{ book.content }}</p>
      <button @click="downloadPDF" class="btn btn-outline-primary">Download as PDF</button>
      <button @click="goBack" class="btn btn-outline-secondary">Back</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './NavBar.vue';
import jsPDF from 'jspdf'; 

export default {
  name: 'DownloadBook',
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
    downloadPDF() {
      const doc = new jsPDF();
      doc.setFontSize(18);
      doc.text(this.book.name, 10, 10); // Adding book name as title
      doc.setFontSize(12);
      const content = this.book.content.split('\n'); // Splitting content by new lines for better formatting
      let yOffset = 20;
      content.forEach((line) => {
        const splitText = doc.splitTextToSize(line, 180); // Splitting long lines into multiple lines within the width of 180
        splitText.forEach((textLine) => {
          doc.text(textLine, 10, yOffset);
          yOffset += 10;
        });
        yOffset += 5; 
      });
      doc.save(`${this.book.name}.pdf`);
    },
    goBack() {
      this.$router.go(-1);
    }
  }
}
</script>

<style scoped>
.book-container {
  max-width: 800px;
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
  text-align: left;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  margin: 10px 5px;
  font-size: 14px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s;
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
