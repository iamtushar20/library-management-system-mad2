<!-- This is the home page of admin where what admin can do is mentioned -->

<template>
  <div class="admin-home">
    <navbar></navbar>
    <header class="style_outer">
      <div class="style_inner">
        <h1>Welcome, Admin</h1>
        <p>Manage your library efficiently with the tools provided below.</p>
      </div>
    </header>

    <section class="admin-overview">
      <div class="overview-card">
        <h2>Add and Edit Books</h2>
        <p>As an admin, you can add new books to the library collection, edit existing book details, and delete books that are no longer needed.</p>
      </div>

      <div class="overview-card">
        <h2>Manage Sections</h2>
        <p>Admins have the ability to create, edit, and delete sections in the library, ensuring the collection is well-organized and easily navigable.</p>
      </div>

      <div class="overview-card">
        <h2>Handle Book Requests</h2>
        <p>Admins can accept, reject, or revoke book requests made by users, ensuring that book circulation is managed smoothly.</p>
      </div>

      <div class="overview-card">
        <h2>Track Book Status</h2>
        <p>Admins can track the status of issued books, including which user has borrowed a specific book and the return date, ensuring all books are accounted for.</p>
      </div>
    </section>

   
  </div>
</template>

<script>
import Navbar from '../users/NavBar.vue';

export default {
  name: 'AdminHome',
  components: {
    Navbar,
  },
};
</script>

<style>
.admin-home {
  font-family: Arial, sans-serif;
  color: #333;
}

.style_outer {
  background-image: url('/path-to-your-image.jpg');
  background-size: cover;
  background-position: center;
  color: white;
  text-align: center;
  padding: 20px 15px;
}

.style_inner {
  background: rgba(0, 0, 0, 0.5);
  display: inline-block;
  padding: 20px;
  border-radius: 10px;
}

.style_outer h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

.style_outer p {
  font-size: 1.2em;
  margin-bottom: 20px;
}

.admin-overview {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 50px 20px;
  background: #f4f4f4;
}

.overview-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  margin: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 300px;
  text-align: center;
}

.overview-card h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
}

.overview-card p {
  font-size: 1em;
}

.footer {
  text-align: center;
  padding: 20px;
  background: #333;
  color: white;
}
</style>
