import React, { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import BusinessList from './pages/BusinessList';
import BusinessDetail from './pages/BusinessDetail';
import CreateBusiness from './pages/CreateBusiness';
import LoadingSpinner from './components/LoadingSpinner';

// Componente de rota protegida
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

// Componente de rota pública (redireciona se autenticado)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

function AppContent() {
  return (
    <Routes>
      {/* Rotas públicas */}
      <Route
        path="/login"
        element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        }
      />
      <Route
        path="/register"
        element={
          <PublicRoute>
            <Register />
          </PublicRoute>
        }
      />

      {/* Rotas protegidas */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="businesses" element={<BusinessList />} />
        <Route path="businesses/new" element={<CreateBusiness />} />
        <Route path="businesses/:id" element={<BusinessDetail />} />
        
        {/* Placeholder para outras rotas */}
        <Route path="suppliers" element={<div className="p-6"><h1 className="text-2xl font-semibold">Fornecedores (Em desenvolvimento)</h1></div>} />
        <Route path="financial" element={<div className="p-6"><h1 className="text-2xl font-semibold">Financeiro (Em desenvolvimento)</h1></div>} />
        <Route path="strategic" element={<div className="p-6"><h1 className="text-2xl font-semibold">Estratégico (Em desenvolvimento)</h1></div>} />
        <Route path="reports" element={<div className="p-6"><h1 className="text-2xl font-semibold">Relatórios (Em desenvolvimento)</h1></div>} />
      </Route>

      {/* Rota 404 */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <AppContent />
      </div>
    </AuthProvider>
  );
}

export default App;