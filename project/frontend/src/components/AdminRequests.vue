<!-- This page will display all the requests made by the user for issuing of book -->

<template>
    <div>
      <navbar></navbar>
      <div class="table-container">
        <div v-if="filteredRequests.length > 0">
          <h2 style="text-align: center;">List of Book Requests</h2>
          <table class="table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Book Name</th>
                <th>Status</th>
                <th>Request Date</th>
                <th>Return Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in filteredRequests" :key="req.id">
                <td>{{ req.user_name }}</td>
                <td>{{ req.book_name }}</td>
                <td>{{ req.status }}</td>
                <td>{{ req.request_date }}</td>
                <td>{{ req.return_date }}</td>
                <td>
                  <button @click="updateStatus(req.id, 'accepted')" class="btn btn-outline-success">Accept</button>
                  <button @click="updateStatus(req.id, 'rejected')" class="btn btn-outline-danger">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          <h3><p><strong>Currently, there are no book requests from users.</strong></p></h3>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Navbar from '../users/NavBar.vue';
  import { useToast } from 'vue-toastification';
  
  export default {
    name: 'AdminRequests',
    data() {
      return {
        req_list: [],
      };
    },
    components: {
      Navbar
    },
    computed: {
      filteredRequests() {
        return this.req_list.filter(req => req.status === 'pending');
      }
    },
    async created() {
      this.fetchRequests();
    },
    methods: {
      async fetchRequests() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/get/book_requests');
          this.req_list = response.data;
        } catch (error) {
          console.error('Error fetching requests', error);
        }
      },
      async updateStatus(reqId, status) {
        const toast = useToast();
        try {
          const response = await axios.post(`http://127.0.0.1:5000/book_requests/${reqId}/status`, { status });
        //   alert(response.data.message);
          toast.success(response.data.message, {
            position: "top-right",
            timeout: 2000
          })  
          this.fetchRequests(); // Refresh the request list after updating status
        } catch (error) {
          console.error('Error updating request status', error);
        }
      }
    }
  }
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
  
  .btn-outline-success {
    background-color: #f9f9f9;
    color: #4CAF50;
    border: 1px solid #4CAF50;
  }
  
  .btn-outline-success:hover {
    background-color: #4CAF50;
    color: white;
  }
  
  .btn-outline-danger {
    background-color: #f9f9f9;
    color: #f44336;
    border: 1px solid #f44336;
  }
  
  .btn-outline-danger:hover {
    background-color: #f44336;
    color: white;
  }
  </style>
  