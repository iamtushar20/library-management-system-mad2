<!-- This is the navbar page and also contains logout button functionality -->

<template>
  <div>
    <nav class="navbar">
      <div class="navbar-brand">
        
      </div>
      <div class="navbar-links">
        <router-link v-if="!isauthenticated" to="/">Home</router-link>
        <router-link v-if="!isauthenticated" to="/loginpage">Login</router-link>
        <router-link v-if="!isauthenticated" to="/usersignup">SignUp</router-link>

        <router-link v-if="isauthenticated && !isAdmin" to="/userhome">Home</router-link>
        <router-link v-if="isauthenticated && !isAdmin" to="/user/issued/books">Your Books</router-link>
        <router-link v-if="isauthenticated && !isAdmin" to="/user/your/requests">Your Requests</router-link>
        <router-link v-if="isauthenticated && !isAdmin" to="/user/issued/history">History</router-link>
        <router-link v-if="isauthenticated && isAdmin" to="/adminhomepage">Home</router-link>
        <router-link v-if="isauthenticated && isAdmin" to="/dashboard/chart">DashBoard</router-link>
        <router-link v-if="isauthenticated && isAdmin" to="/section">Sections</router-link>
        <router-link v-if="isauthenticated && isAdmin" to="/allbooks">All Books</router-link>
        <router-link v-if="isauthenticated && isAdmin" to="/admin/requests">Book Requests</router-link>
        <router-link v-if="isauthenticated && isAdmin" to="/admin/issued/all/books">Issued Books</router-link>
        <router-link v-if="isauthenticated && isAdmin" to="/allbookstatus">Book Status</router-link>

        <button v-if="isauthenticated" @click="logout" type="button" class="btn btn-danger">Logout</button>
      </div>
    </nav>


    <!-- <footer class="footer">
      <p>&copy; 2024 Your Library. All rights reserved.</p>
    </footer> -->
  </div>
</template>

<script>

import { useToast } from 'vue-toastification';
export default {
  data() {
    return {
      isauthenticated: JSON.parse(localStorage.getItem('isauthenticated')) || false,
    };
  },
  computed: {
    isAdmin() {
      const userRole = localStorage.getItem('userRole');
      return userRole === 'admin';
    }
  },
  methods: {
    // Logout functionality and unsetting the local storage values which were set in login page
    logout() {
      const toast = useToast();
      localStorage.removeItem('access_token');
      localStorage.removeItem('userRole');
      localStorage.removeItem('isauthenticated');
      localStorage.removeItem('username')
      this.$router.push('/loginpage');
      toast.success('Logged out successfully!',{
        timeout: 2000,
      })

    }
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #343a40;
  padding: 10px 20px;
  border-bottom: 1px solid #ccc;
}

/* .navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #343a40;
  padding: 10px 20px;
  border-top: 1px solid #ccc;
  position: fixed;
  width: 100%;
  bottom: 0;
} */  

/* .navbar {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  background-color: #343a40;
  padding: 10px;
  border-left: 1px solid #ccc;
  position: fixed;
  height: 100%;
  right: 0;
  top: 0;
}

.navbar-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
} */

/* .navbar {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  background-color: #343a40;
  padding: 10px;
  border-right: 1px solid #ccc;
  position: fixed;
  height: 100%;
  left: 0;
  top: 0;
}

.navbar-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
} */


.navbar-brand {
  font-weight: bold;
  font-size: 24px;
  color: white;
  text-decoration: none;
}

.navbar-links {
  display: flex;
  gap: 20px;
}

.navbar-links a, .navbar-links .btn {
  text-decoration: none;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.navbar-links a:hover, .navbar-links .btn:hover {
  background-color: #495057;
}

.navbar-links .btn {
  background-color: #007bff;
  border: none;
  cursor: pointer;
}

.navbar-links .btn.btn-danger {
  background-color: #dc3545;
}

.navbar-links .btn.btn-danger:hover {
  background-color: #c82333;
}

.container {
  margin: 20px;
}

.footer {
  text-align: center;
  padding: 1px;
  background: #343a40;
  color: white;
  position: fixed;
  width: 100%;
  bottom: 0;
}
</style>
