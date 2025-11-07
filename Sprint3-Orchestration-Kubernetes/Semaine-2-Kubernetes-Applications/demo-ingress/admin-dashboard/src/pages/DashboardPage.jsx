import React, {useState, useEffect} from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Chip,
  LinearProgress,
  Button
} from '@mui/material';
// Icons removed
import {adminAPI, adminAnalyticsAPI} from '../services/api';
import StatsCard from '../components/dashboard/StatsCard';
import RecentActivity from '../components/dashboard/RecentActivity';
import QuickActions from '../components/dashboard/QuickActions';

const DashboardPage = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError('');

      // Chargement des données du dashboard admin
      const dashboardPromise = adminAPI.getDashboard();
      const analyticsPromise = adminAnalyticsAPI.getDashboard();

      const [dashboardResult, analyticsResult] = await Promise.all([
        dashboardPromise,
        analyticsPromise
      ]);

      setDashboardData(dashboardResult);
      setAnalyticsData(analyticsResult);
    } catch (err) {
      console.error('Erreur lors du chargement du dashboard:', err);
      setError('Impossible de charger les données du dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box
        display='flex'
        justifyContent='center'
        alignItems='center'
        minHeight='400px'
      >
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth='lg' sx={{mt: 4}}>
        <Alert
          severity='error'
          action={<Button onClick={loadDashboardData}>Réessayer</Button>}
        >
          {error}
        </Alert>
      </Container>
    );
  }

  const stats = dashboardData?.stats || {};
  const analytics = analyticsData?.overview || {};

  return (
    <Container maxWidth='lg' sx={{mt: 4, mb: 4}}>
      {/* En-tête */}
      <Box sx={{mb: 4}}>
        <Typography variant='h4' gutterBottom>
          Tableau de bord
        </Typography>
        <Typography variant='body1' color='text.secondary'>
          Vue d'ensemble de l'activité des campagnes de don de sang
        </Typography>
      </Box>

      {/* Statistiques principales */}
      <Grid container spacing={3} sx={{mb: 4}}>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title='Utilisateurs inscrits'
            value={stats.totalUsers || 0}
            trend={analytics.usersGrowth || 0}
            color='primary'
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title='Campagnes actives'
            value={stats.activeCampaigns || 0}
            trend={analytics.campaignsGrowth || 0}
            color='success'
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title='RDV ce mois'
            value={stats.monthlyAppointments || 0}
            trend={analytics.appointmentsGrowth || 0}
            color='info'
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title='Dons réalisés'
            value={stats.completedDonations || 0}
            trend={analytics.donationsGrowth || 0}
            color='error'
          />
        </Grid>
      </Grid>

      {/* Statistiques des rendez-vous */}
      <Grid container spacing={3} sx={{mb: 4}}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant='h6' gutterBottom>
                État des rendez-vous
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Box textAlign='center'>
                    <CheckCircle color='success' sx={{fontSize: 40}} />
                    <Typography variant='h6'>
                      {stats.completedAppointments || 0}
                    </Typography>
                    <Typography variant='caption' color='text.secondary'>
                      Terminés
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box textAlign='center'>
                    <Schedule color='warning' sx={{fontSize: 40}} />
                    <Typography variant='h6'>
                      {stats.scheduledAppointments || 0}
                    </Typography>
                    <Typography variant='caption' color='text.secondary'>
                      Programmés
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box textAlign='center'>
                    <Cancel color='error' sx={{fontSize: 40}} />
                    <Typography variant='h6'>
                      {stats.cancelledAppointments || 0}
                    </Typography>
                    <Typography variant='caption' color='text.secondary'>
                      Annulés
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box textAlign='center'>
                    <TrendingUp color='info' sx={{fontSize: 40}} />
                    <Typography variant='h6'>
                      {(
                        (stats.completedAppointments /
                          (stats.totalAppointments || 1)) *
                        100
                      ).toFixed(1)}
                      %
                    </Typography>
                    <Typography variant='caption' color='text.secondary'>
                      Taux de réussite
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{height: '100%'}}>
            <CardContent>
              <Typography variant='h6' gutterBottom>
                Activité système
              </Typography>
              <Box sx={{mb: 2}}>
                <Box display='flex' justifyContent='space-between' mb={1}>
                  <Typography variant='body2'>Utilisation CPU</Typography>
                  <Typography variant='body2'>45%</Typography>
                </Box>
                <LinearProgress variant='determinate' value={45} />
              </Box>
              <Box sx={{mb: 2}}>
                <Box display='flex' justifyContent='space-between' mb={1}>
                  <Typography variant='body2'>Mémoire</Typography>
                  <Typography variant='body2'>62%</Typography>
                </Box>
                <LinearProgress
                  variant='determinate'
                  value={62}
                  color='warning'
                />
              </Box>
              <Box sx={{mb: 2}}>
                <Typography variant='body2' gutterBottom>
                  État des services
                </Typography>
                <Box display='flex' flexWrap='wrap' gap={0.5}>
                  <Chip label='API Users' color='success' size='small' />
                  <Chip label='API Campaigns' color='success' size='small' />
                  <Chip label='API Appointments' color='success' size='small' />
                  <Chip label='Analytics' color='warning' size='small' />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Actions rapides et activité récente */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <QuickActions />
        </Grid>
        <Grid item xs={12} md={8}>
          <RecentActivity activities={dashboardData?.recentActivities || []} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default DashboardPage;
