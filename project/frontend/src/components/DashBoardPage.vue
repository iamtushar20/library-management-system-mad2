<template>
    <div>
        <nav class="navbar">
            <div class="container">
                <div class="'navbar-brand'">
                    <h1 class="'title'">Library Management</h1>
                </div>
                <div class="navbar-menu">
                    <div class="navbar-end">
                        
                        <router-link v-if="!isauthenticated" to="/loginpage" class="navbar-item">Login</router-link>
                        <router-link v-if="!isauthenticated" to="/usersignup" class="navbar-item">Sign Up</router-link>
                        <router-link v-if="isauthenticated" to="/dashboard" class="navbar-item">Dashboard</router-link>
                        <button v-if="isauthenticated" @click="logout" class="navbar-item">Logout</button>
                    </div>
                </div>
            </div>
        </nav>
        <div>
            <h2> This is the library management system </h2>
        </div>
    </div>
    

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isauthenticated: JSON.parse(localStorage.getItem('isauthenticated')) || false,
    };
  },
  methods: {
    async logout() {
      const access_token = localStorage.getItem('access_token');
      try {
        await axios.post('http://127.0.0.1:5000/logout', null, {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        });
        
        localStorage.removeItem('access_token');
        localStorage.removeItem('userRole')
        localStorage.removeItem('username')
        localStorage.setItem('isauthenticated', JSON.stringify(false));

        this.isauthenticated = false;
        this.$router.push('/loginpage');
      } catch (error) {
        console.error('Error during logout:', error);
        
      }
    },
  },
};
</script>