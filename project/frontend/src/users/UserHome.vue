<!-- This is the user home page where user can search for books, request and buy -->

<template>
  <div>
    <navbar></navbar>
    <div class="search-container">
      <input type="text" v-model="searchQuery" placeholder="Search by book name, section name, or author" />
      <button @click="search" class="btn btn-outline-primary">Search</button>
    </div>
    <div v-for="section in filteredSections" :key="section.id" class="section-container">
      <h2 class="section-title">{{ section.name }}</h2>
      <h4 style="text-align: center;"><p><i>{{ section.description }}</i></p></h4>
      <div class="books">
        <div v-for="book in section.books" :key="book.id" class="book-card">
          <img src="/images/data.jpg.webp" alt="Book cover" class="book-image" />
          <h4>{{ book.name }}</h4>
          <p><strong>Authors:</strong> {{ book.authors }}</p>
          <!-- <p><strong>Price:</strong> {{ book.price }}</p> -->
          <button @click="requestBook(book.id)" class="btn btn-outline-primary">Request</button>
          <button @click="buyBook(book.id)" class="btn btn-outline-success">Buy</button>
        </div>
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
      sections: [],
      searchQuery: '',
      filteredSections: []
    }
  },
  watch: {
    searchQuery: 'search'
  },
  created() {
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/sections');
        const sections = response.data;
        const sectionPromises = sections.map(section =>
          axios.get(`http://127.0.0.1:5000/api/sections/${section.id}`)
            .then(res => ({
              ...section,
              books: res.data.books.map(book => ({
                ...book,
                imageUrl: `/images/${book.imageName}`
              }))
            }))
        );
        const results = await Promise.all(sectionPromises);
        this.sections = results;
        this.filteredSections = results;
      } catch (error) {
        console.log(error);
      }
    },
    search() {
      const query = this.searchQuery.toLowerCase();
      if (!query) {
        this.filteredSections = this.sections; // If search query is empty, show all sections
      } else {
        this.filteredSections = this.sections
          .map(section => {
            if (section.name.toLowerCase().includes(query)) {
              // If section name matches, return the whole section with all books
              return section;
            } else {
              // Otherwise, filter books within the section
              const filteredBooks = section.books.filter(book =>
                book.name.toLowerCase().includes(query) ||
                book.authors.toLowerCase().includes(query)
              );
              if (filteredBooks.length > 0) {
                return {
                  ...section,
                  books: filteredBooks
                };
              }
            }
            return null; 
          })
          .filter(section => section !== null); 
      }
    },
    requestBook(bookId) {
      this.$router.push({ name: 'BookRequest', params: { id: bookId } });
    },
    buyBook(bookId) {
      this.$router.push({ name: 'BuyBook', params: { id: bookId } });
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

.search-container {
  display: flex;
  justify-content: center;
  margin: 20px;
}

.search-container input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}

.search-container button {
  padding: 10px 20px;
  font-size: 16px;
}

.section-container {
  margin-bottom: 20px;
}

.section-title {
  text-align: center;
  margin-bottom: 10px;
}

.books {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.book-card {
  border: 1px solid #ddd;
  padding: 16px;
  margin: 8px;
  width: 200px;
  text-align: center;
}

.book-image {
  width: 100%;
  height: auto;
  display: block;
  margin-bottom: 10px;
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

.btn-outline-success {
  background-color: #f9f9f9;
  color: #28a745;
  border: 1px solid #28a745;
}

.btn-outline-success:hover {
  background-color: #28a745;
  color: white;
}
</style>
