import React from 'react';
import {Routes, Route, Navigate} from 'react-router-dom';
import {Container} from '@mui/material';

import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import ProtectedRoute from './components/auth/ProtectedRoute';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import CampaignsPage from './pages/CampaignsPage';
import CampaignDetailsPage from './pages/CampaignDetailsPage';
import BookingPage from './pages/BookingPage';
import ProfilePage from './pages/ProfilePage';
import MyAppointmentsPage from './pages/MyAppointmentsPage';
import NotFoundPage from './pages/NotFoundPage';

import {useAuth} from './contexts/AuthContext';

function App() {
  const {isAuthenticated, loading} = useAuth();

  if (loading) {
    return <div>Chargement...</div>;
  }

  return (
    <div style={{display: 'flex', flexDirection: 'column', minHeight: '100vh'}}>
      <Navbar />

      <Container
        component='main'
        maxWidth='lg'
        sx={{
          flex: 1,
          py: 3,
          px: {xs: 2, sm: 3}
        }}
      >
        <Routes>
          {/* Routes publiques */}
          <Route path='/' element={<HomePage />} />
          <Route path='/campaigns' element={<CampaignsPage />} />
          <Route path='/campaigns/:id' element={<CampaignDetailsPage />} />

          {/* Routes d'authentification */}
          <Route
            path='/login'
            element={isAuthenticated ? <Navigate to='/' /> : <LoginPage />}
          />
          <Route
            path='/register'
            element={isAuthenticated ? <Navigate to='/' /> : <RegisterPage />}
          />

          {/* Routes protégées */}
          <Route
            path='/book/:campaignId'
            element={
              <ProtectedRoute>
                <BookingPage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/profile'
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path='/my-appointments'
            element={
              <ProtectedRoute>
                <MyAppointmentsPage />
              </ProtectedRoute>
            }
          />

          {/* 404 */}
          <Route path='*' element={<NotFoundPage />} />
        </Routes>
      </Container>

      <Footer />
    </div>
  );
}

export default App;
