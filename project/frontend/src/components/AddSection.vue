<!-- This page will allow admin to add a section -->

<template>
    <navbar></navbar>
    <div class="form-container">
        <h2>Add Section</h2>
        <form @submit.prevent="addsection" class="section-form">
            <label for="sectionname" class="form-label">Section Name</label>
            <input type="text" id="sectionname" name="sectionname" v-model="sectionname" class="form-control" required><br>

            <label for="date_created" class="form-label">Date Created</label>
            <input type="date" id="date_created" name="date_created" v-model="date_created" class="form-control" required><br>

            <label for="description" class="form-label">Description</label>
            <textarea id="description" name="description" v-model="description" class="form-control" required></textarea><br>

            <div class="form-group">
                <button type="submit" class="btn btn-primary">Add</button>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';
import Navbar from '../users/NavBar.vue';

export default {
    name: 'AddSection',
    components: {
        Navbar
    },
    data() {
        return {
            sectionname: '',
            date_created: '',
            description: '',
        };
    },
    methods: {
        async addsection() {
            const toast = useToast();
            try {
                const response = await axios.post('http://127.0.0.1:5000/addsection', {
                    sectionname: this.sectionname,
                    date_created: this.date_created,
                    description: this.description
                });
                console.log(response.data);
                this.$router.push('/section');
            } catch (error) {
                console.error(error.response.data);
                toast.error(error.response.data.message, {
                    position: "top-right",
                    timeout: 2000
                });
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

.section-form {
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

textarea.form-control {
    resize: vertical;
}

.btn {
    display: inline-block;
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

.btn:hover {
    background-color: #45a049;
}

.form-group {
    text-align: center;
}
</style>
