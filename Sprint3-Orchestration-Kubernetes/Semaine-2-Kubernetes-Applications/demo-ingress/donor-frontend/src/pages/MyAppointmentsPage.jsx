import React from 'react';
import {Container, Typography, Box, Paper} from '@mui/material';

const MyAppointmentsPage = () => {
  return (
    <Container maxWidth='lg'>
      <Box sx={{py: 4}}>
        <Typography variant='h4' gutterBottom sx={{fontWeight: 'bold'}}>
          Mes rendez-vous
        </Typography>

        <Paper elevation={1} sx={{p: 4, textAlign: 'center'}}>
          <Typography variant='h6' gutterBottom>
            🚧 Page en construction
          </Typography>
          <Typography color='text.secondary'>
            Cette page affichera l'historique des rendez-vous avec options
            d'annulation et de confirmation.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default MyAppointmentsPage;
