<!-- This page will display all the sections along with add section button -->

<template>
  <div>
    <navbar></navbar>
    <div class="table-container">
      <router-link to="/addsection" class="btn btn-add-section">Add Section</router-link>
      <h2 style="text-align: center;">Sections</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Section Name</th>
            <th>Date Created</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="section in sections" :key="section.id">
            <td>{{ section.name }}</td>
            <td>{{ section.date_created }}</td>
            <td>{{ section.description }}</td>
            <td>
              <button @click="seelist(section.id)" class="btn btn-success">See List</button>
              <button @click="editSection(section.id)" class="btn btn-outline-secondary">Edit</button>
              <button @click="confirmDelete(section.id)" class="btn btn-danger">Delete</button>
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
  name: 'SectionsTable',
  components: {
    Navbar
  },
  data() {
    return {
      sections: []
    };
  },
  async created() {
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/sections');
        this.sections = response.data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    editSection(id) {
      this.$router.push(`/editsection/${id}`);
    },
    confirmDelete(id) {
      this.$router.push(`/deletesection/${id}`);
    },
    seelist(id) {
      this.$router.push(`/sectionbook/${id}`);
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

.btn-danger {
  background-color: #f44336;
  color: white;
}

.btn-danger:hover {
  background-color: #da190b;
}

.btn-add-section {
  display: inline-block;
  margin-bottom: 15px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn-add-section:hover {
  background-color: #0056b3;
}
</style>
