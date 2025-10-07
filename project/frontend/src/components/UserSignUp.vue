<!-- This is a sign up page for users -->

<template>
    <div>
        <navbar></navbar>
    
        <div class="form-container">
        <h2>Sign Up</h2>
        <div class="form-group">
            <form @submit.prevent="signup" class="form">
            <label for="name" class="form-label">Name</label>
            <input type="text" id="name" name="name" v-model="name" class="form-control"><br>
    
            <label for="email" class="form-label">Email</label>
            <input type="email" id="email" name="email" v-model="email" class="form-control"><br>
    
            <label for="username" class="form-label">Username</label>
            <input type="text" id="username" name="username" v-model="username" class="form-control"><br>
    
            <label for="password" class="form-label">Password</label>
            <input type="password" id="password" name="password" v-model="password" class="form-control"><br>
    
            <button type="submit" class="btn-submit">Sign Up</button>
            </form>
            <router-link v-if="!isauthenticated" to="/loginpage">Already a user? Login</router-link>
        </div>
        </div>
    </div>
    
  </template>
  
  <script>
  import { useToast } from 'vue-toastification';
  import Navbar from '../users/NavBar.vue';
  import axios from 'axios';
  
  export default {
    components: {
        Navbar
    },
    data() {
      return {
        name: '',
        email: '',
        username: '',
        password: '',
        isauthenticated: false
      };
    },
    methods: {
      async signup() {
        const toast = useToast();
        try {
          const response = await axios.post('http://127.0.0.1:5000/signup', {
            name: this.name,
            email: this.email,
            username: this.username,
            password: this.password
          });
          console.log('Signup Successful', response.data);
          toast.success(response.data.message, { position: "top-right", timeout: 3000 });
          this.$router.push('/loginpage');
        } catch (error) {
          console.error(error.response.data);
          toast.error(error.response.data.error, {
            position: "top-right",
            timeout: 3000
          });
        }
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
  
  .form {
    display: flex;
    flex-direction: column;
  }
  
  .form-label {
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .form-control {
    margin-bottom: 15px;
    padding: 10px;
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
  </style>
  