<!-- This page is the confirmation page for deleting a section -->

<template>
  <div>
    <navbar></navbar>
    <div class="delete-confirmation-container">
      <h2 style="text-align: center;">Confirm Deletion</h2>
      <p>Are you sure you want to delete this section?</p>
      <p>
        <strong>Section Name:</strong> {{ section.name }}<br>
        <strong>Date Created:</strong> {{ section.date_created }}<br>
        <strong>Description:</strong> {{ section.description }}
      </p>
      <div class="buttons">
        <button @click="confirmDelete" class="btn btn-danger">Yes, Delete</button>
        <button @click="cancelDelete" class="btn btn-outline-secondary">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '../users/NavBar.vue';
import { useToast } from 'vue-toastification';

export default {
  name: 'DeleteConfirmation',
  components: {
    Navbar
  },
  data() {
    return {
      section: {}
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
    async confirmDelete() {
      const toast = useToast();
      const sectionId = this.$route.params.id;
      try {
        await axios.delete(`http://127.0.0.1:5000/sections/${sectionId}`);
        this.$router.push('/section');
        toast.success('Section deleted successfully!',{
          timeout: 2000,
        });
        

      } catch (error) {
        console.error('Error deleting section:', error);
      }
    },
    cancelDelete() {
      this.$router.push('/section');
    }
  }
};
</script>

<style scoped>
.delete-confirmation-container {
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
  margin-top: 20px;
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
