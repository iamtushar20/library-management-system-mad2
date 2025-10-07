<!-- This is the login page for user or admin -->

<template>
    <navbar></navbar>
    <div class="form-container">
      <h2>Login</h2>
      <form @submit.prevent="login" class="login-form">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required class="form-control">
  
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required class="form-control">
  
        <button type="submit" class="btn-submit">Login</button>
      </form>
      <router-link v-if="!isauthenticated" to="/usersignup" class="signup-link">Not a user? Sign Up</router-link>
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
        username: '',
        password: '',
        isauthenticated: '',
      };
    },
    methods: {
      async login() {
        const toast = useToast();
        try {
          const response = await axios.post('http://127.0.0.1:5000/login', {
            username: this.username,
            password: this.password
          });
          console.log(response.data);
          // setting items in localstorage when a user logs in to the app to use them later
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('userRole', response.data.userRole);
          localStorage.setItem('isauthenticated', true);
          localStorage.setItem('username', this.username);
          const userRole = response.data.userRole;
          if (userRole === 'admin') {
            toast.success('Welcome, Admin!', {
              position: "top-right",
              timeout: 3000
            });
            this.$router.push('/adminhomepage');
          } else {
            toast.success('Welcome, User!', {
              position: "top-right",
              timeout: 3000
            });
            this.$router.push('/userhome');
          }
        } catch (error) {
          toast.error('Login failed. Please check your credentials.', {
            position: "top-right",
            timeout: 3000
          });
          console.error(error.response.data);
        }
      }
    }
  };
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
  
  .login-form {
    display: flex;
    flex-direction: column;
  }
  
  .login-form label {
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .login-form input {
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
  
  .signup-link {
    display: block;
    text-align: center;
    margin-top: 10px;
    color: #007BFF;
    text-decoration: none;
  }
  
  .signup-link:hover {
    text-decoration: underline;
  }
  </style>
  