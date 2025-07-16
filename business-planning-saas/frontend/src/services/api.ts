import axios, { AxiosInstance } from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para tratar respostas de erro
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Tipos para APIs
export interface Business {
  id: string;
  name: string;
  description?: string;
  segment: string;
  industry: string;
  business_type: string;
  cnpj?: string;
  founded_date?: string;
  address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country: string;
  target_audience?: string;
  market_size?: string;
  owner_id: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface BusinessCreate {
  name: string;
  description?: string;
  segment: string;
  industry: string;
  business_type: string;
  cnpj?: string;
  founded_date?: string;
  address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  target_audience?: string;
  market_size?: string;
}

// API functions
export const businessApi = {
  list: () => apiClient.get<Business[]>('/businesses'),
  get: (id: string) => apiClient.get<Business>(`/businesses/${id}`),
  create: (data: BusinessCreate) => apiClient.post<Business>('/businesses', data),
  update: (id: string, data: Partial<BusinessCreate>) => apiClient.put<Business>(`/businesses/${id}`, data),
  delete: (id: string) => apiClient.delete(`/businesses/${id}`),
  getDashboard: (id: string) => apiClient.get(`/businesses/${id}/dashboard`),
};