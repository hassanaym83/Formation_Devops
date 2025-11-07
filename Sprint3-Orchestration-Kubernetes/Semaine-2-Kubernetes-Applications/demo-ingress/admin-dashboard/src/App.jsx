import React from 'react';
import {Routes, Route, Navigate} from 'react-router-dom';
import {Box} from '@mui/material';

import AdminLayout from './components/layout/AdminLayout';
import ProtectedRoute from './components/auth/ProtectedRoute';

// Pages Admin
import LoginPage from './pages/auth/LoginPage';
import DashboardPage from './pages/DashboardPage';
import UsersPage from './pages/UsersPage';
import CampaignsPage from './pages/CampaignsPage';
import AppointmentsPage from './pages/AppointmentsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import SystemPage from './pages/SystemPage';
import NotFoundPage from './pages/NotFoundPage';

import {useAdminAuth} from './contexts/AdminAuthContext';

function App() {
  const {isAuthenticated, loading} = useAdminAuth();

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh'
        }}
      >
        Chargement...
      </Box>
    );
  }

  return (
    <Routes>
      {/* Route de connexion */}
      <Route
        path='/login'
        element={isAuthenticated ? <Navigate to='/' /> : <LoginPage />}
      />

      {/* Routes protégées avec layout admin */}
      <Route
        path='/'
        element={
          <ProtectedRoute>
            <AdminLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path='users' element={<UsersPage />} />
        <Route path='campaigns' element={<CampaignsPage />} />
        <Route path='appointments' element={<AppointmentsPage />} />
        <Route path='analytics' element={<AnalyticsPage />} />
        <Route path='system' element={<SystemPage />} />
      </Route>

      {/* 404 */}
      <Route path='*' element={<NotFoundPage />} />
    </Routes>
  );
}

export default App;
