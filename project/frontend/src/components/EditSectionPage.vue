<!-- This page is about updation of a section in the library -->

<template>
  <div>
    <navbar></navbar>
    <div class="form-container">
      <h2 style="text-align: center;">Edit Section</h2>
      <form @submit.prevent="updateSection" class="section-form">
        <div class="form-group">
          <label for="sectionname" class="form-label">Section Name</label>
          <input type="text" id="sectionname" v-model="section.name" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="date_created" class="form-label">Date Created</label>
          <input type="date" id="date_created" v-model="section.date_created" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="description" class="form-label">Description</label>
          <input type="text" id="description" v-model="section.description" class="form-control" required>
        </div>
        <button type="submit" class="btn-submit">Update</button>
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
  name: 'EditSectionPage',
  components: {
    Navbar
  },
  data() {
    return {
      section: {
        id: '',
        name: '',
        date_created: '',
        description: ''
      }
    };
  },
  async created() {
    const sectionId = this.$route.params.id;
    try {
      const response = await axios.get(`http://127.0.0.1:5000/sections/${sectionId}`);
      this.section = response.data;
    } catch (error) {
      console.error('Error fetching section:', error);
    }
  },
  methods: {
    async updateSection() {
      const toast = useToast();
      try {
        const sectionId = this.$route.params.id;
        await axios.put(`http://127.0.0.1:5000/sections/${sectionId}`, this.section);
        this.$router.push('/section');
        toast.success('Section updated successfully', {
          timeout: 2000
        })
      } catch (error) {
        console.error('Error updating section:', error);
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
};
</script>

<style scoped>
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

.section-form {
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
