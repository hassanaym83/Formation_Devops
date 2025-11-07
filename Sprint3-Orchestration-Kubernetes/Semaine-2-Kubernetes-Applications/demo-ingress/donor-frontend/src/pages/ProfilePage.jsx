import React from 'react';
import {Container, Typography, Box, Paper} from '@mui/material';

const ProfilePage = () => {
  return (
    <Container maxWidth='lg'>
      <Box sx={{py: 4}}>
        <Typography variant='h4' gutterBottom sx={{fontWeight: 'bold'}}>
          Mon profil
        </Typography>

        <Paper elevation={1} sx={{p: 4, textAlign: 'center'}}>
          <Typography variant='h6' gutterBottom>
            🚧 Page en construction
          </Typography>
          <Typography color='text.secondary'>
            Cette page permettra de consulter et modifier ses informations
            personnelles et médicales.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default ProfilePage;
