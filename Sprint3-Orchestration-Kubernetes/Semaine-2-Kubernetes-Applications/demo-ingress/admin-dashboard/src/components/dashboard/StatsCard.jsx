import React from 'react';
import {Card, CardContent, Typography, Box, Chip} from '@mui/material';
import {TrendingUp, TrendingDown} from '@mui/icons-material';

const StatsCard = ({title, value, icon, trend, color = 'primary'}) => {
  const isPositiveTrend = trend >= 0;

  return (
    <Card sx={{height: '100%'}}>
      <CardContent>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            mb: 2
          }}
        >
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 48,
              height: 48,
              borderRadius: 2,
              backgroundColor: `${color}.light`,
              color: `${color}.contrastText`
            }}
          >
            {icon}
          </Box>
          {trend !== undefined && (
            <Chip
              icon={isPositiveTrend ? <TrendingUp /> : <TrendingDown />}
              label={`${Math.abs(trend)}%`}
              color={isPositiveTrend ? 'success' : 'error'}
              size='small'
              variant='outlined'
            />
          )}
        </Box>
        <Typography
          variant='h4'
          component='div'
          fontWeight='bold'
          color={`${color}.main`}
        >
          {typeof value === 'number' ? value.toLocaleString('fr-FR') : value}
        </Typography>
        <Typography variant='body2' color='text.secondary'>
          {title}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default StatsCard;
