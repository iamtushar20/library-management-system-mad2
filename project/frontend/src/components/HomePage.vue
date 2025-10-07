<!-- This is the home page when a user first time lands on the app  -->

<template>
  <div class="home">
    <navbar></navbar>
    <header class="outer">
      <div class="inner">
        <h1>Welcome to Your Digital Library</h1>
        <p>Discover, request, and manage your favorite books all in one place.</p>
        <router-link to="/loginpage" class="btn btn-primary">Get Started</router-link>
      </div>
    </header>

    <section class="features">
      <div class="feature">
        <h2>Explore a Wide Range of Books</h2>
        <p>Browse our extensive collection of books across various genres and categories.</p>
      </div>
      <div class="feature">
        <h2>Manage Your Borrowed Books</h2>
        <p>Easily track the books you have borrowed and their return dates.</p>
      </div>
      <div class="feature">
        <h2>Seamless Book Requests</h2>
        <p>Request books with a single click and get notified when they're available.</p>
      </div>
    </section>

    
  </div>
</template>

<script>
import Navbar from '../users/NavBar.vue';

export default {
  name: 'Home',
  components: {
    Navbar,
  },
};
</script>

<style scoped>
.home {
  font-family: Arial, sans-serif;
  color: #333;
}

.outer {
  background-image: url('/path-to-your-image.jpg');
  background-size: cover;
  background-position: center;
  color: white;
  text-align: center;
  padding: 80px 20px;
}

.inner {
  background: rgba(0, 0, 0, 0.5);
  display: inline-block;
  padding: 20px;
  border-radius: 10px;
  max-width: 600px; 
}

.outer h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

.outer p {
  font-size: 1.2em;
  margin-bottom: 20px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 1em;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  text-decoration: none;
}

.features {
  display: flex;
  justify-content: space-around;
  padding: 50px 20px;
  background: #f4f4f4;
}

.feature {
  text-align: center;
  max-width: 300px;
}

.feature h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
}

.feature p {
  font-size: 1em;
}

.footer {
  text-align: center;
  padding: 20px;
  background: #333;
  color: white;
}
</style>
