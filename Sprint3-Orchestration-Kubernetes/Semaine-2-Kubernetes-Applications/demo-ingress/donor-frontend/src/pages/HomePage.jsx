import React from 'react';
import {Link} from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Container,
  Paper,
  Avatar
} from '@mui/material';

import {useAuth} from '../contexts/AuthContext';

const HomePage = () => {
  const {isAuthenticated, user} = useAuth();

  const features = [
    {
      title: 'Prise de RDV Facile',
      description: 'Réservez votre créneau de don en quelques clics'
    },
    {
      title: 'Géolocalisation',
      description: 'Trouvez les campagnes près de chez vous'
    },
    {
      title: 'Sécurisé',
      description: 'Vos données médicales sont protégées'
    },
    {
      title: 'Suivi Personnel',
      description: 'Consultez votre historique de dons'
    }
  ];

  const stats = [
    {number: '1,250', label: 'Donneurs inscrits'},
    {number: '89', label: 'Campagnes actives'},
    {number: '3,420', label: 'Dons réalisés'},
    {number: '15,680', label: 'Vies sauvées'}
  ];

  return (
    <Container maxWidth='lg'>
      {/* Section Hero */}
      <Box sx={{py: {xs: 4, md: 8}, textAlign: 'center'}}>
        <Typography
          variant='h2'
          component='h1'
          gutterBottom
          sx={{
            fontWeight: 'bold',
            fontSize: {xs: '2rem', md: '3rem'},
            color: 'primary.main'
          }}
        >
          Donnez du sang, <br />
          Sauvez des vies
        </Typography>

        <Typography
          variant='h5'
          color='text.secondary'
          sx={{mb: 4, fontSize: {xs: '1.1rem', md: '1.5rem'}}}
        >
          Plateforme de gestion des campagnes de don de sang
        </Typography>

        {isAuthenticated ? (
          <Box
            sx={{
              display: 'flex',
              gap: 2,
              justifyContent: 'center',
              flexWrap: 'wrap'
            }}
          >
            <Button
              variant='contained'
              size='large'
              component={Link}
              to='/campaigns'
              sx={{px: 4, py: 1.5}}
            >
              Voir les campagnes
            </Button>
            <Button
              variant='outlined'
              size='large'
              component={Link}
              to='/my-appointments'
              sx={{px: 4, py: 1.5}}
            >
              Mes rendez-vous
            </Button>
          </Box>
        ) : (
          <Box
            sx={{
              display: 'flex',
              gap: 2,
              justifyContent: 'center',
              flexWrap: 'wrap'
            }}
          >
            <Button
              variant='contained'
              size='large'
              component={Link}
              to='/register'
              sx={{px: 4, py: 1.5}}
            >
              Devenir donneur
            </Button>
            <Button
              variant='outlined'
              size='large'
              component={Link}
              to='/campaigns'
              sx={{px: 4, py: 1.5}}
            >
              Voir les campagnes
            </Button>
          </Box>
        )}
      </Box>

      {/* Message de bienvenue personnalisé */}
      {isAuthenticated && (
        <Paper
          elevation={2}
          sx={{
            p: 3,
            mb: 6,
            background: 'linear-gradient(45deg, #ffebee 30%, #e8f5e8 90%)',
            borderRadius: 2
          }}
        >
          <Box sx={{display: 'flex', alignItems: 'center', gap: 2}}>
            <Avatar sx={{bgcolor: 'primary.main', width: 56, height: 56}}>
              ❤️
            </Avatar>
            <Box>
              <Typography variant='h6' sx={{fontWeight: 'bold'}}>
                Bienvenue {user?.first_name} ! 👋
              </Typography>
              <Typography color='text.secondary'>
                Prêt(e) à sauver des vies ? Découvrez les campagnes près de chez
                vous.
              </Typography>
            </Box>
          </Box>
        </Paper>
      )}

      {/* Statistiques */}
      <Paper elevation={1} sx={{p: 4, mb: 6, borderRadius: 2}}>
        <Typography
          variant='h4'
          align='center'
          gutterBottom
          sx={{fontWeight: 'bold', mb: 4}}
        >
          Notre Impact
        </Typography>
        <Grid container spacing={3}>
          {stats.map((stat, index) => (
            <Grid item xs={6} md={3} key={index}>
              <Box sx={{textAlign: 'center'}}>
                <Typography
                  variant='h3'
                  sx={{
                    fontWeight: 'bold',
                    color: 'primary.main',
                    fontSize: {xs: '1.8rem', md: '2.5rem'}
                  }}
                >
                  {stat.number}
                </Typography>
                <Typography variant='body1' color='text.secondary'>
                  {stat.label}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Fonctionnalités */}
      <Box sx={{py: 6}}>
        <Typography
          variant='h4'
          align='center'
          gutterBottom
          sx={{fontWeight: 'bold', mb: 4}}
        >
          Pourquoi nous choisir ?
        </Typography>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                sx={{
                  height: '100%',
                  textAlign: 'center',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4
                  }
                }}
              >
                <CardContent sx={{p: 3}}>
                  <Avatar
                    sx={{
                      bgcolor: 'primary.main',
                      width: 64,
                      height: 64,
                      mx: 'auto',
                      mb: 2
                    }}
                  >
                    {feature.icon}
                  </Avatar>

                  <Typography
                    variant='h6'
                    gutterBottom
                    sx={{fontWeight: 'bold'}}
                  >
                    {feature.title}
                  </Typography>

                  <Typography variant='body2' color='text.secondary'>
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Appel à l'action */}
      <Paper
        elevation={2}
        sx={{
          p: 6,
          mt: 6,
          textAlign: 'center',
          background: 'linear-gradient(135deg, #d32f2f 0%, #f44336 100%)',
          color: 'white'
        }}
      >
        <Typography variant='h4' gutterBottom sx={{fontWeight: 'bold'}}>
          Prêt à faire la différence ?
        </Typography>

        <Typography variant='h6' sx={{mb: 4, opacity: 0.9}}>
          Un don de sang peut sauver jusqu'à 3 vies
        </Typography>

        {!isAuthenticated && (
          <Button
            variant='contained'
            size='large'
            component={Link}
            to='/register'
            sx={{
              bgcolor: 'white',
              color: 'primary.main',
              px: 4,
              py: 1.5,
              '&:hover': {
                bgcolor: '#f5f5f5'
              }
            }}
          >
            Rejoignez-nous maintenant
          </Button>
        )}

        {isAuthenticated && (
          <Button
            variant='contained'
            size='large'
            component={Link}
            to='/campaigns'
            sx={{
              bgcolor: 'white',
              color: 'primary.main',
              px: 4,
              py: 1.5,
              '&:hover': {
                bgcolor: '#f5f5f5'
              }
            }}
          >
            Réserver un créneau
          </Button>
        )}
      </Paper>
    </Container>
  );
};

export default HomePage;
