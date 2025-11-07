import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  IconButton,
  Typography,
  Box,
  Collapse
} from '@mui/material';
import {
  Dashboard,
  People,
  Campaign,
  Event,
  Analytics,
  Settings,
  ChevronLeft,
  ChevronRight,
  ExpandLess,
  ExpandMore,
  PersonAdd,
  Group,
  AddCircle,
  List as ListIcon,
  BarChart,
  Timeline,
  Assignment
} from '@mui/icons-material';
import {useNavigate, useLocation} from 'react-router-dom';
import {useState} from 'react';

const AdminSidebar = ({open, onToggle}) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [expandedItems, setExpandedItems] = useState({});

  const handleItemExpand = (itemName) => {
    setExpandedItems((prev) => ({
      ...prev,
      [itemName]: !prev[itemName]
    }));
  };

  const menuItems = [
    {
      text: 'Tableau de bord',
      icon: <Dashboard />,
      path: '/dashboard',
      active: location.pathname === '/dashboard'
    },
    {
      text: 'Utilisateurs',
      icon: <People />,
      expandable: true,
      expanded: expandedItems.users,
      subItems: [
        {text: 'Liste des utilisateurs', icon: <Group />, path: '/users'},
        {text: 'Créer utilisateur', icon: <PersonAdd />, path: '/users/create'}
      ]
    },
    {
      text: 'Campagnes',
      icon: <Campaign />,
      expandable: true,
      expanded: expandedItems.campaigns,
      subItems: [
        {text: 'Liste des campagnes', icon: <ListIcon />, path: '/campaigns'},
        {text: 'Créer campagne', icon: <AddCircle />, path: '/campaigns/create'}
      ]
    },
    {
      text: 'Rendez-vous',
      icon: <Event />,
      path: '/appointments',
      active: location.pathname === '/appointments'
    },
    {
      text: 'Analyses',
      icon: <Analytics />,
      expandable: true,
      expanded: expandedItems.analytics,
      subItems: [
        {text: "Vue d'ensemble", icon: <BarChart />, path: '/analytics'},
        {text: 'Tendances', icon: <Timeline />, path: '/analytics/trends'},
        {text: 'Rapports', icon: <Assignment />, path: '/analytics/reports'}
      ]
    }
  ];

  const settingsItems = [
    {
      text: 'Paramètres',
      icon: <Settings />,
      path: '/settings',
      active: location.pathname === '/settings'
    }
  ];

  const renderMenuItem = (item, index) => {
    if (item.expandable) {
      return (
        <React.Fragment key={index}>
          <ListItem disablePadding>
            <ListItemButton
              onClick={() => handleItemExpand(item.text.toLowerCase())}
              sx={{
                minHeight: 48,
                justifyContent: open ? 'initial' : 'center',
                px: 2.5
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: open ? 3 : 'auto',
                  justifyContent: 'center'
                }}
              >
                {item.icon}
              </ListItemIcon>
              {open && (
                <>
                  <ListItemText primary={item.text} />
                  {item.expanded ? <ExpandLess /> : <ExpandMore />}
                </>
              )}
            </ListItemButton>
          </ListItem>
          {open && (
            <Collapse in={item.expanded} timeout='auto' unmountOnExit>
              <List component='div' disablePadding>
                {item.subItems.map((subItem, subIndex) => (
                  <ListItem key={subIndex} disablePadding>
                    <ListItemButton
                      sx={{
                        pl: 4,
                        backgroundColor:
                          location.pathname === subItem.path
                            ? 'primary.light'
                            : 'transparent',
                        color:
                          location.pathname === subItem.path
                            ? 'primary.contrastText'
                            : 'inherit',
                        '&:hover': {
                          backgroundColor:
                            location.pathname === subItem.path
                              ? 'primary.main'
                              : 'grey.100'
                        }
                      }}
                      onClick={() => navigate(subItem.path)}
                    >
                      <ListItemIcon
                        sx={{
                          minWidth: 0,
                          mr: 3,
                          justifyContent: 'center',
                          color:
                            location.pathname === subItem.path
                              ? 'primary.contrastText'
                              : 'inherit'
                        }}
                      >
                        {subItem.icon}
                      </ListItemIcon>
                      <ListItemText primary={subItem.text} />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Collapse>
          )}
        </React.Fragment>
      );
    }

    return (
      <ListItem key={index} disablePadding>
        <ListItemButton
          sx={{
            minHeight: 48,
            justifyContent: open ? 'initial' : 'center',
            px: 2.5,
            backgroundColor: item.active ? 'primary.light' : 'transparent',
            color: item.active ? 'primary.contrastText' : 'inherit',
            '&:hover': {
              backgroundColor: item.active ? 'primary.main' : 'grey.100'
            }
          }}
          onClick={() => navigate(item.path)}
        >
          <ListItemIcon
            sx={{
              minWidth: 0,
              mr: open ? 3 : 'auto',
              justifyContent: 'center',
              color: item.active ? 'primary.contrastText' : 'inherit'
            }}
          >
            {item.icon}
          </ListItemIcon>
          {open && <ListItemText primary={item.text} />}
        </ListItemButton>
      </ListItem>
    );
  };

  return (
    <Drawer
      variant='permanent'
      open={open}
      sx={{
        width: open ? 280 : 64,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: open ? 280 : 64,
          boxSizing: 'border-box',
          transition: 'width 0.3s',
          overflowX: 'hidden',
          mt: 8, // Hauteur de l'AppBar
          height: 'calc(100vh - 64px)'
        }
      }}
    >
      {/* En-tête avec bouton toggle */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: open ? 'space-between' : 'center',
          px: 1,
          py: 1,
          borderBottom: '1px solid',
          borderColor: 'divider'
        }}
      >
        {open && (
          <Typography variant='h6' noWrap component='div' sx={{ml: 1}}>
            Menu
          </Typography>
        )}
        <IconButton onClick={onToggle}>
          {open ? <ChevronLeft /> : <ChevronRight />}
        </IconButton>
      </Box>

      {/* Menu principal */}
      <List sx={{pt: 1}}>
        {menuItems.map((item, index) => renderMenuItem(item, index))}
      </List>

      <Divider sx={{my: 1}} />

      {/* Menu paramètres */}
      <List>
        {settingsItems.map((item, index) => renderMenuItem(item, index))}
      </List>
    </Drawer>
  );
};

export default AdminSidebar;
