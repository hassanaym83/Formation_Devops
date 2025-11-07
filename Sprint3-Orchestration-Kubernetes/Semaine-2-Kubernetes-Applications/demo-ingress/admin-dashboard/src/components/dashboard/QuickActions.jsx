import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import {
  PersonAdd,
  Campaign,
  Event,
  Analytics,
  Settings,
  Refresh,
  Download,
  Notifications
} from '@mui/icons-material';
import {useNavigate} from 'react-router-dom';

const QuickActions = () => {
  const navigate = useNavigate();

  const actions = [
    {
      id: 'create-campaign',
      title: 'Créer une campagne',
      description: 'Organiser une nouvelle collecte',
      icon: <Campaign color='primary' />,
      onClick: () => navigate('/campaigns/create')
    },
    {
      id: 'add-user',
      title: 'Ajouter un utilisateur',
      description: 'Créer un nouveau compte',
      icon: <PersonAdd color='success' />,
      onClick: () => navigate('/users/create')
    },
    {
      id: 'view-appointments',
      title: 'Voir les RDV du jour',
      description: 'Gérer les rendez-vous',
      icon: <Event color='info' />,
      onClick: () => navigate('/appointments')
    },
    {
      id: 'analytics',
      title: 'Rapports & Analytics',
      description: 'Consulter les statistiques',
      icon: <Analytics color='warning' />,
      onClick: () => navigate('/analytics')
    }
  ];

  const systemActions = [
    {
      id: 'refresh-data',
      title: 'Actualiser les données',
      icon: <Refresh />,
      onClick: () => window.location.reload()
    },
    {
      id: 'export-data',
      title: 'Exporter les données',
      icon: <Download />,
      onClick: () => console.log('Export des données...')
    },
    {
      id: 'notifications',
      title: 'Centre de notifications',
      icon: <Notifications />,
      onClick: () => console.log('Notifications...')
    },
    {
      id: 'settings',
      title: 'Paramètres système',
      icon: <Settings />,
      onClick: () => navigate('/settings')
    }
  ];

  return (
    <Card sx={{height: '100%'}}>
      <CardContent>
        <Typography variant='h6' gutterBottom>
          Actions rapides
        </Typography>

        <Typography variant='subtitle2' color='text.secondary' sx={{mb: 1}}>
          Gestion
        </Typography>
        <List dense>
          {actions.map((action) => (
            <ListItemButton
              key={action.id}
              onClick={action.onClick}
              sx={{
                borderRadius: 1,
                mb: 0.5,
                '&:hover': {
                  bgcolor: 'action.hover'
                }
              }}
            >
              <ListItemIcon sx={{minWidth: 36}}>{action.icon}</ListItemIcon>
              <ListItemText
                primary={
                  <Typography variant='body2' fontWeight='medium'>
                    {action.title}
                  </Typography>
                }
                secondary={
                  <Typography variant='caption' color='text.secondary'>
                    {action.description}
                  </Typography>
                }
              />
            </ListItemButton>
          ))}
        </List>

        <Divider sx={{my: 2}} />

        <Typography variant='subtitle2' color='text.secondary' sx={{mb: 1}}>
          Système
        </Typography>
        <List dense>
          {systemActions.map((action) => (
            <ListItemButton
              key={action.id}
              onClick={action.onClick}
              sx={{
                borderRadius: 1,
                mb: 0.5,
                '&:hover': {
                  bgcolor: 'action.hover'
                }
              }}
            >
              <ListItemIcon sx={{minWidth: 36}}>{action.icon}</ListItemIcon>
              <ListItemText
                primary={
                  <Typography variant='body2'>{action.title}</Typography>
                }
              />
            </ListItemButton>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default QuickActions;
