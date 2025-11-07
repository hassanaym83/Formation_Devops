import React from 'react';
import {Container, Typography, Box, Paper} from '@mui/material';

const CampaignsPage = () => {
  return (
    <Container maxWidth='lg'>
      <Box sx={{py: 4}}>
        <Typography variant='h4' gutterBottom sx={{fontWeight: 'bold'}}>
          Campagnes de don de sang
        </Typography>

        <Paper elevation={1} sx={{p: 4, textAlign: 'center'}}>
          <Typography variant='h6' gutterBottom>
            🚧 Page en construction
          </Typography>
          <Typography color='text.secondary'>
            Cette page affichera la liste des campagnes disponibles avec
            filtres, géolocalisation et options de réservation.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default CampaignsPage;
