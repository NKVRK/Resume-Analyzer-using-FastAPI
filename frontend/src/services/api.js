import axios from 'axios';

// Create an Axios instance pointing to our backend API
const API_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadResume = (formData) => {
  return apiClient.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getResumes = () => {
  return apiClient.get('/resumes');
};

export const getResumeById = (id) => {
  return apiClient.get(`/resumes/${id}`);
};

export const deleteResume = (id) => {
  return apiClient.delete(`/resumes/${id}`);
};