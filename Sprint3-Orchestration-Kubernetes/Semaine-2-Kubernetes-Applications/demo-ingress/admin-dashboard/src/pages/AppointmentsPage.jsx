import React from 'react';
import {Container, Typography, Box} from '@mui/material';

const AppointmentsPage = () => {
  return (
    <Container maxWidth='lg' sx={{mt: 4, mb: 4}}>
      <Box sx={{mb: 4}}>
        <Typography variant='h4' gutterBottom>
          Gestion des rendez-vous
        </Typography>
        <Typography variant='body1' color='text.secondary'>
          Cette page sera bientôt disponible pour gérer tous les rendez-vous de
          don de sang.
        </Typography>
      </Box>

      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '400px',
          bgcolor: 'background.paper',
          borderRadius: 2,
          border: '2px dashed',
          borderColor: 'divider'
        }}
      >
        <Typography variant='h6' color='text.secondary'>
          Interface de gestion des rendez-vous en développement
        </Typography>
      </Box>
    </Container>
  );
};

export default AppointmentsPage;
