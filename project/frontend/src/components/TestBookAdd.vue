<template>
    <div class="buy-form-container">
        <h2>Add Book to Section</h2>
        <form @submit.prevent="addBook">
            <label for="name">Name:</label>
            <input type="text" id="name" v-model="book.name" required>
            <label for="content">Content (PDF):</label>
            <input type="file" id="content" @change="handleFileUpload" required>
            <label for="authors">Authors:</label>
            <input type="text" id="authors" v-model="book.authors" required>
            <label for="date_added">Date Added:</label>
            <input type="date" id="date_added" v-model="book.date_added" required>
            <label for="price">Price:</label>
            <input type="number" id="price" v-model="book.price" required>
            <button type="submit" class="btn btn-success">Add Book</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            book: {
                name: '',
                authors: '',
                date_added: '',
                price: null
            },
            file: null
        };
    },
    methods: {
        handleFileUpload(event) {
            this.file = event.target.files[0];
        },
        async addBook() {
            try {
                const formData = new FormData();
                formData.append('name', this.book.name);
                formData.append('content', this.file);
                formData.append('authors', this.book.authors);
                formData.append('date_added', this.book.date_added);
                formData.append('price', this.book.price);
                formData.append('section_id', this.$route.params.sectionId);

                const response = await axios.post('http://127.0.0.1:5000/api/books', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                console.log('Book added:', response.data);
                this.$router.push(`/sectionbook/${this.$route.params.sectionId}`);
            } catch (error) {
                console.error('Error adding book:', error);
            }
        }
    }
};
</script>
