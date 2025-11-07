import React from 'react';
import {Container, Typography, Box, Paper} from '@mui/material';

const BookingPage = () => {
  return (
    <Container maxWidth='lg'>
      <Box sx={{py: 4}}>
        <Typography variant='h4' gutterBottom sx={{fontWeight: 'bold'}}>
          Réserver un créneau
        </Typography>

        <Paper elevation={1} sx={{p: 4, textAlign: 'center'}}>
          <Typography variant='h6' gutterBottom>
            🚧 Page en construction
          </Typography>
          <Typography color='text.secondary'>
            Cette page permettra de réserver un créneau pour une campagne avec
            calendrier interactif et confirmation de réservation.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default BookingPage;
