import React from 'react';
import {Container, Typography, Box, Paper} from '@mui/material';

const CampaignDetailsPage = () => {
  return (
    <Container maxWidth='lg'>
      <Box sx={{py: 4}}>
        <Typography variant='h4' gutterBottom sx={{fontWeight: 'bold'}}>
          Détails de la campagne
        </Typography>

        <Paper elevation={1} sx={{p: 4, textAlign: 'center'}}>
          <Typography variant='h6' gutterBottom>
            🚧 Page en construction
          </Typography>
          <Typography color='text.secondary'>
            Cette page affichera les détails d'une campagne spécifique avec
            créneaux disponibles, informations pratiques et bouton de
            réservation.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default CampaignDetailsPage;
