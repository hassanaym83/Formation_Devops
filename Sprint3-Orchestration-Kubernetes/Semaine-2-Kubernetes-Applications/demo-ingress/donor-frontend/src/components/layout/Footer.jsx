import React from 'react';
import {Box, Typography, Container, Grid, Link, Divider} from '@mui/material';
// Icons removed

const Footer = () => {
  return (
    <Box
      component='footer'
      sx={{
        backgroundColor: 'primary.main',
        color: 'white',
        py: 4,
        mt: 'auto'
      }}
    >
      <Container maxWidth='lg'>
        <Grid container spacing={4}>
          {/* À propos */}
          <Grid item xs={12} md={4}>
            <Typography variant='h6' gutterBottom sx={{fontWeight: 'bold'}}>
              🩸 DonDeSang
            </Typography>
            <Typography variant='body2' sx={{mb: 2}}>
              Plateforme de gestion des campagnes de don de sang. Ensemble,
              sauvons des vies en facilitant les dons de sang.
            </Typography>
            <Box sx={{display: 'flex', alignItems: 'center', mt: 2}}>
              <Typography variant='body2'>❤️ Chaque don compte</Typography>
            </Box>
          </Grid>

          {/* Liens rapides */}
          <Grid item xs={12} md={4}>
            <Typography variant='h6' gutterBottom sx={{fontWeight: 'bold'}}>
              Liens Rapides
            </Typography>
            <Box sx={{display: 'flex', flexDirection: 'column', gap: 1}}>
              <Link
                href='/campaigns'
                color='inherit'
                underline='hover'
                variant='body2'
              >
                Campagnes actives
              </Link>
              <Link
                href='/register'
                color='inherit'
                underline='hover'
                variant='body2'
              >
                Devenir donneur
              </Link>
              <Link href='#' color='inherit' underline='hover' variant='body2'>
                Conditions de don
              </Link>
              <Link href='#' color='inherit' underline='hover' variant='body2'>
                FAQ
              </Link>
            </Box>
          </Grid>

          {/* Contact */}
          <Grid item xs={12} md={4}>
            <Typography variant='h6' gutterBottom sx={{fontWeight: 'bold'}}>
              Contact
            </Typography>
            <Box sx={{display: 'flex', flexDirection: 'column', gap: 1}}>
              <Box sx={{display: 'flex', alignItems: 'center'}}>
                <Typography variant='body2'>✉️ contact@dondesang.fr</Typography>
              </Box>
              <Box sx={{display: 'flex', alignItems: 'center'}}>
                <Typography variant='body2'>📞 0800 123 456</Typography>
              </Box>
              <Box sx={{display: 'flex', alignItems: 'center'}}>
                <Typography variant='body2'>📍 Partout en France</Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>

        <Divider sx={{my: 3, borderColor: 'rgba(255,255,255,0.2)'}} />

        {/* Copyright et mentions */}
        <Grid container spacing={2} alignItems='center'>
          <Grid item xs={12} md={8}>
            <Typography variant='body2' sx={{opacity: 0.8}}>
              © 2024 DonDeSang - Système de gestion des campagnes de don de
              sang.
            </Typography>
            <Typography variant='caption' sx={{opacity: 0.6}}>
              Projet éducatif Kubernetes - Simplon DevOps
            </Typography>
          </Grid>

          <Grid item xs={12} md={4}>
            <Box
              sx={{
                display: 'flex',
                justifyContent: {xs: 'flex-start', md: 'flex-end'},
                gap: 2
              }}
            >
              <Link
                href='#'
                color='inherit'
                underline='hover'
                variant='caption'
                sx={{opacity: 0.8}}
              >
                Mentions légales
              </Link>
              <Link
                href='#'
                color='inherit'
                underline='hover'
                variant='caption'
                sx={{opacity: 0.8}}
              >
                Confidentialité
              </Link>
              <Link
                href='#'
                color='inherit'
                underline='hover'
                variant='caption'
                sx={{opacity: 0.8}}
              >
                CGU
              </Link>
            </Box>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Footer;
