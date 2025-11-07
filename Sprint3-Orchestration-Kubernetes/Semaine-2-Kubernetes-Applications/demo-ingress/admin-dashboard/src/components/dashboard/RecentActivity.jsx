import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
  Chip,
  Avatar
} from '@mui/material';
import {
  PersonAdd,
  Campaign,
  Event,
  CheckCircle,
  Cancel,
  Edit
} from '@mui/icons-material';

const RecentActivity = ({activities = []}) => {
  const getActivityIcon = (type) => {
    switch (type) {
      case 'user_registered':
        return <PersonAdd color='success' />;
      case 'campaign_created':
        return <Campaign color='primary' />;
      case 'appointment_booked':
        return <Event color='info' />;
      case 'appointment_completed':
        return <CheckCircle color='success' />;
      case 'appointment_cancelled':
        return <Cancel color='error' />;
      case 'campaign_updated':
        return <Edit color='warning' />;
      default:
        return <Event color='action' />;
    }
  };

  const getActivityMessage = (activity) => {
    switch (activity.type) {
      case 'user_registered':
        return `${activity.details.userName} s'est inscrit`;
      case 'campaign_created':
        return `Nouvelle campagne "${activity.details.campaignName}" créée`;
      case 'appointment_booked':
        return `RDV réservé pour la campagne "${activity.details.campaignName}"`;
      case 'appointment_completed':
        return `Don réalisé - ${activity.details.userName}`;
      case 'appointment_cancelled':
        return `RDV annulé - ${activity.details.userName}`;
      case 'campaign_updated':
        return `Campagne "${activity.details.campaignName}" modifiée`;
      default:
        return activity.message || 'Activité inconnue';
    }
  };

  const formatTimeAgo = (dateString) => {
    const now = new Date();
    const activityDate = new Date(dateString);
    const diffMs = now - activityDate;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "À l'instant";
    if (diffMins < 60) return `Il y a ${diffMins} min`;
    if (diffHours < 24) return `Il y a ${diffHours}h`;
    return `Il y a ${diffDays} jour${diffDays > 1 ? 's' : ''}`;
  };

  // Données d'exemple si aucune activité n'est fournie
  const exampleActivities = [
    {
      id: 1,
      type: 'user_registered',
      details: {userName: 'Marie Dupont'},
      createdAt: new Date(Date.now() - 300000) // 5 min ago
    },
    {
      id: 2,
      type: 'appointment_booked',
      details: {
        campaignName: 'Don urgente - Hôpital Central',
        userName: 'Jean Martin'
      },
      createdAt: new Date(Date.now() - 900000) // 15 min ago
    },
    {
      id: 3,
      type: 'campaign_created',
      details: {campaignName: 'Collecte de Noël 2024'},
      createdAt: new Date(Date.now() - 1800000) // 30 min ago
    },
    {
      id: 4,
      type: 'appointment_completed',
      details: {userName: 'Sophie Bernard'},
      createdAt: new Date(Date.now() - 3600000) // 1h ago
    },
    {
      id: 5,
      type: 'campaign_updated',
      details: {campaignName: 'Don mensuel - Centre ville'},
      createdAt: new Date(Date.now() - 7200000) // 2h ago
    }
  ];

  const displayActivities =
    activities.length > 0 ? activities : exampleActivities;

  return (
    <Card sx={{height: '100%'}}>
      <CardContent>
        <Typography variant='h6' gutterBottom>
          Activité récente
        </Typography>
        <List dense>
          {displayActivities.slice(0, 8).map((activity) => (
            <ListItem key={activity.id} sx={{px: 0}}>
              <ListItemIcon>
                <Avatar sx={{width: 32, height: 32, bgcolor: 'transparent'}}>
                  {getActivityIcon(activity.type)}
                </Avatar>
              </ListItemIcon>
              <ListItemText
                primary={
                  <Typography variant='body2'>
                    {getActivityMessage(activity)}
                  </Typography>
                }
                secondary={
                  <Box sx={{display: 'flex', alignItems: 'center', mt: 0.5}}>
                    <Chip
                      label={formatTimeAgo(activity.createdAt)}
                      size='small'
                      variant='outlined'
                      sx={{fontSize: '0.7rem', height: 20}}
                    />
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
        {displayActivities.length === 0 && (
          <Box sx={{textAlign: 'center', py: 4, color: 'text.secondary'}}>
            <Typography variant='body2'>Aucune activité récente</Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default RecentActivity;
