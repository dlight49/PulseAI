import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Metrics API
const CONV_BASE_URL = 'http://localhost:8001'; // Conversations API
const API_KEY = 'pulse_secret_dev_key';

const api = axios.create({
  headers: {
    'X-Pulse-API-Key': API_KEY,
  },
});

export const getBusinessSummary = async (businessId) => {
  const response = await api.get(`${API_BASE_URL}/metrics/${businessId}/summary`);
  return response.data;
};

export const getTransactions = async (businessId) => {
  const response = await api.get(`${API_BASE_URL}/metrics/${businessId}/transactions`);
  return response.data;
};

export const getRecentChats = async (businessId) => {
  const response = await api.get(`${CONV_BASE_URL}/conversations/${businessId}/recent`);
  return response.data;
};

export const getChatHistory = async (businessId, contactId) => {
  const response = await api.get(`${CONV_BASE_URL}/conversations/${businessId}/${contactId}`);
  return response.data;
};
