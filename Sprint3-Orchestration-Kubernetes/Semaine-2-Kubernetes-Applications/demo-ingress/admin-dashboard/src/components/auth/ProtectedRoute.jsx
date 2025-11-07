import React from 'react';
import {Navigate} from 'react-router-dom';
import {useAdminAuth} from '../../contexts/AdminAuthContext';
import {Box, CircularProgress} from '@mui/material';

const ProtectedRoute = ({children}) => {
  const {admin, loading} = useAdminAuth();

  // Affichage du loader pendant la vérification
  if (loading) {
    return (
      <Box
        display='flex'
        justifyContent='center'
        alignItems='center'
        minHeight='100vh'
        bgcolor='background.default'
      >
        <CircularProgress size={60} />
      </Box>
    );
  }

  // Redirection vers login si pas connecté
  if (!admin) {
    return <Navigate to='/login' replace />;
  }

  // Affichage du contenu protégé
  return children;
};

export default ProtectedRoute;
