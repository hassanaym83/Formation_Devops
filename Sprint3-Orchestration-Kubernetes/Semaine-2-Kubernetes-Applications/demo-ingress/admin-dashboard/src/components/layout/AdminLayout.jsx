import React from 'react';
import {Outlet} from 'react-router-dom';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Divider,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  AdminPanelSettings,
  AccountCircle,
  Logout,
  Settings,
  Notifications
} from '@mui/icons-material';
import {useState} from 'react';
import {useAdminAuth} from '../../contexts/AdminAuthContext';
import AdminSidebar from './AdminSidebar';

const AdminLayout = () => {
  const {admin, logout} = useAdminAuth();
  const [anchorEl, setAnchorEl] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleMenuClose();
    logout();
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Box sx={{display: 'flex', minHeight: '100vh'}}>
      {/* AppBar principale */}
      <AppBar
        position='fixed'
        sx={{
          zIndex: (theme) => theme.zIndex.drawer + 1,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}
      >
        <Toolbar>
          <AdminPanelSettings sx={{mr: 2}} />
          <Typography variant='h6' component='div' sx={{flexGrow: 1}}>
            Administration - Don de Sang
          </Typography>

          {/* Notifications */}
          <IconButton color='inherit' sx={{mr: 1}}>
            <Notifications />
          </IconButton>

          {/* Menu utilisateur */}
          <Box sx={{display: 'flex', alignItems: 'center'}}>
            <Typography
              variant='body2'
              sx={{mr: 1, display: {xs: 'none', sm: 'block'}}}
            >
              {admin?.username}
            </Typography>
            <IconButton
              size='large'
              aria-label='menu utilisateur'
              aria-controls='menu-appbar'
              aria-haspopup='true'
              onClick={handleMenuOpen}
              color='inherit'
            >
              <Avatar sx={{width: 32, height: 32, bgcolor: 'primary.dark'}}>
                {admin?.username?.charAt(0).toUpperCase()}
              </Avatar>
            </IconButton>
          </Box>

          {/* Menu déroulant utilisateur */}
          <Menu
            id='menu-appbar'
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'right'
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right'
            }}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={handleMenuClose}>
              <ListItemIcon>
                <AccountCircle fontSize='small' />
              </ListItemIcon>
              <ListItemText>Mon profil</ListItemText>
            </MenuItem>
            <MenuItem onClick={handleMenuClose}>
              <ListItemIcon>
                <Settings fontSize='small' />
              </ListItemIcon>
              <ListItemText>Paramètres</ListItemText>
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <Logout fontSize='small' />
              </ListItemIcon>
              <ListItemText>Déconnexion</ListItemText>
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      {/* Sidebar */}
      <AdminSidebar open={sidebarOpen} onToggle={toggleSidebar} />

      {/* Contenu principal */}
      <Box
        component='main'
        sx={{
          flexGrow: 1,
          mt: 8, // Hauteur de l'AppBar
          ml: sidebarOpen ? '280px' : '64px',
          transition: 'margin-left 0.3s',
          minHeight: 'calc(100vh - 64px)',
          backgroundColor: 'grey.50'
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default AdminLayout;
