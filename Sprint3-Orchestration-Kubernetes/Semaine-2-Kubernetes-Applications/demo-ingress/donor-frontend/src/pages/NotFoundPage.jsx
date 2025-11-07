import React from 'react';
import {Link} from 'react-router-dom';
import {Box, Typography, Button, Container} from '@mui/material';
// Icons removed

const NotFoundPage = () => {
  return (
    <Container maxWidth='sm'>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          py: 8
        }}
      >
        <Typography
          variant='h1'
          sx={{
            fontSize: '6rem',
            fontWeight: 'bold',
            color: 'primary.main',
            mb: 2
          }}
        >
          404
        </Typography>

        <Typography variant='h4' gutterBottom>
          Page non trouvée
        </Typography>

        <Typography variant='body1' color='text.secondary' sx={{mb: 4}}>
          La page que vous cherchez n'existe pas ou a été déplacée.
        </Typography>

        <Box
          sx={{
            display: 'flex',
            gap: 2,
            flexWrap: 'wrap',
            justifyContent: 'center'
          }}
        >
          <Button variant='contained' component={Link} to='/' size='large'>
            🏠 Retour à l'accueil
          </Button>

          <Button
            variant='outlined'
            onClick={() => window.history.back()}
            size='large'
          >
            ← Page précédente
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default NotFoundPage;
