<!-- This book is to see feedback given by the user about a particular book -->

<template>
  <navbar></navbar>
  <div class="book-feedback">
    
    <h1 style="text-align: center;">Feedback for {{ bookName }}</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Username</th>
          <th>Feedback</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in filteredTransactions" :key="transaction.id">
          <td>{{ transaction.user_name }}</td>
          <td>{{ transaction.feedback }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '../users/NavBar.vue';

export default {
  name: 'SeeFeedback',
  components: {
    Navbar
  },
  data() {
    return {
      bookName: this.$route.params.bookName,
      transactions: [],
      filteredTransactions: []
    };
  },
  async created() {
    await this.fetchTransactions();
    this.filterTransactions();
  },
  methods: {
    async fetchTransactions() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/transactions');
        this.transactions = response.data;
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    },
    filterTransactions() {
      this.filteredTransactions = this.transactions.filter(transaction => 
        transaction.book_name === this.bookName && transaction.status === 'accepted'
      );
    }
  }
};
</script>

<style scoped>
.book-feedback {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
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
</style>
