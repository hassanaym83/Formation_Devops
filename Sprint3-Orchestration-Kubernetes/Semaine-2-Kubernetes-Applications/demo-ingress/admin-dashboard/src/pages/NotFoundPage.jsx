import React from 'react';
import {Container, Typography, Box, Button} from '@mui/material';
// Icons removed
import {useNavigate} from 'react-router-dom';

const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth='sm' sx={{mt: 8, mb: 4, textAlign: 'center'}}>
      <Box sx={{mb: 4}}>
        <Error sx={{fontSize: 80, color: 'error.main', mb: 2}} />
        <Typography variant='h3' gutterBottom>
          404
        </Typography>
        <Typography variant='h5' gutterBottom color='text.secondary'>
          Page non trouvée
        </Typography>
        <Typography variant='body1' color='text.secondary' sx={{mb: 4}}>
          La page que vous recherchez n'existe pas ou a été déplacée.
        </Typography>
        <Button
          variant='contained'
          startIcon={<Home />}
          onClick={() => navigate('/dashboard')}
          size='large'
        >
          Retour au tableau de bord
        </Button>
      </Box>
    </Container>
  );
};

export default NotFoundPage;
