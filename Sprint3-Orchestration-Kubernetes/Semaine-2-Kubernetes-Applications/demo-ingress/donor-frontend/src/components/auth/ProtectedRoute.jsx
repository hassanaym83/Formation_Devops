import React from 'react';
import {Navigate, useLocation} from 'react-router-dom';
import {Box, CircularProgress, Typography} from '@mui/material';
import {useAuth} from '../../contexts/AuthContext';

const ProtectedRoute = ({children}) => {
  const {isAuthenticated, loading} = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50vh',
          gap: 2
        }}
      >
        <CircularProgress color='primary' />
        <Typography variant='body1' color='text.secondary'>
          Vérification de l'authentification...
        </Typography>
      </Box>
    );
  }

  if (!isAuthenticated) {
    // Rediriger vers la page de connexion avec l'URL de retour
    return <Navigate to='/login' state={{from: location}} replace />;
  }

  return children;
};

export default ProtectedRoute;
