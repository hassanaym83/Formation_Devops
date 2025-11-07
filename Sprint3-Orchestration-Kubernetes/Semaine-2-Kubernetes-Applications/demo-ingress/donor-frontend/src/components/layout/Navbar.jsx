import React, {useState} from 'react';
import {Link, useNavigate, useLocation} from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Box,
  useMediaQuery,
  useTheme,
  Drawer,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
// Icons removed

import {useAuth} from '../../contexts/AuthContext';

const Navbar = () => {
  const {user, isAuthenticated, logout} = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const [anchorEl, setAnchorEl] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleProfileMenuClose();
    navigate('/');
  };

  const handleMobileMenuToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const isActivePath = (path) => location.pathname === path;

  const navigationItems = [
    {label: 'Accueil', path: '/'},
    {label: 'Campagnes', path: '/campaigns'}
  ];

  const authenticatedItems = [
    {label: 'Mes RDV', path: '/my-appointments'},
    {label: 'Mon Profil', path: '/profile'}
  ];

  const renderMobileMenu = (
    <Drawer
      variant='temporary'
      anchor='left'
      open={mobileOpen}
      onClose={handleMobileMenuToggle}
      ModalProps={{keepMounted: true}}
      sx={{
        '& .MuiDrawer-paper': {
          boxSizing: 'border-box',
          width: 250,
          backgroundColor: '#fafafa'
        }
      }}
    >
      <Box sx={{p: 2}}>
        <Typography
          variant='h6'
          sx={{color: 'primary.main', fontWeight: 'bold'}}
        >
          🩸 DonDeSang
        </Typography>
      </Box>

      <List>
        {navigationItems.map((item) => (
          <ListItem
            key={item.path}
            button
            component={Link}
            to={item.path}
            onClick={handleMobileMenuToggle}
            sx={{
              backgroundColor: isActivePath(item.path)
                ? 'primary.light'
                : 'transparent',
              '&:hover': {backgroundColor: 'primary.light'}
            }}
          >
            <ListItemText primary={item.label} />
          </ListItem>
        ))}

        {isAuthenticated &&
          authenticatedItems.map((item) => (
            <ListItem
              key={item.path}
              button
              component={Link}
              to={item.path}
              onClick={handleMobileMenuToggle}
              sx={{
                backgroundColor: isActivePath(item.path)
                  ? 'primary.light'
                  : 'transparent',
                '&:hover': {backgroundColor: 'primary.light'}
              }}
            >
              <ListItemText primary={item.label} />
            </ListItem>
          ))}

        {!isAuthenticated ? (
          <>
            <ListItem
              button
              component={Link}
              to='/login'
              onClick={handleMobileMenuToggle}
            >
              <ListItemText primary='Connexion' />
            </ListItem>
            <ListItem
              button
              component={Link}
              to='/register'
              onClick={handleMobileMenuToggle}
            >
              <ListItemText primary='Inscription' />
            </ListItem>
          </>
        ) : (
          <ListItem button onClick={handleLogout}>
            <ListItemText primary='Déconnexion' />
          </ListItem>
        )}
      </List>
    </Drawer>
  );

  const renderProfileMenu = (
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{vertical: 'top', horizontal: 'right'}}
      keepMounted
      transformOrigin={{vertical: 'top', horizontal: 'right'}}
      open={Boolean(anchorEl)}
      onClose={handleProfileMenuClose}
    >
      <MenuItem
        onClick={() => {
          navigate('/profile');
          handleProfileMenuClose();
        }}
      >
        Mon Profil
      </MenuItem>
      <MenuItem
        onClick={() => {
          navigate('/my-appointments');
          handleProfileMenuClose();
        }}
      >
        Mes Rendez-vous
      </MenuItem>
      <MenuItem onClick={handleLogout}>Déconnexion</MenuItem>
    </Menu>
  );

  return (
    <>
      <AppBar position='sticky' elevation={1}>
        <Toolbar>
          {isMobile && (
            <IconButton
              color='inherit'
              aria-label='open drawer'
              edge='start'
              onClick={handleMobileMenuToggle}
              sx={{mr: 2}}
            >
              ☰
            </IconButton>
          )}

          {/* Logo */}
          <Typography
            variant='h6'
            component={Link}
            to='/'
            sx={{
              flexGrow: isMobile ? 1 : 0,
              textDecoration: 'none',
              color: 'inherit',
              fontWeight: 'bold',
              mr: 4
            }}
          >
            🩸 DonDeSang
          </Typography>

          {/* Navigation desktop */}
          {!isMobile && (
            <Box sx={{flexGrow: 1, display: 'flex'}}>
              {navigationItems.map((item) => (
                <Button
                  key={item.path}
                  color='inherit'
                  component={Link}
                  to={item.path}
                  sx={{
                    mx: 1,
                    backgroundColor: isActivePath(item.path)
                      ? 'rgba(255,255,255,0.1)'
                      : 'transparent'
                  }}
                >
                  {item.label}
                </Button>
              ))}
            </Box>
          )}

          {/* Actions utilisateur */}
          {!isMobile && (
            <Box sx={{display: 'flex', alignItems: 'center'}}>
              {isAuthenticated ? (
                <>
                  <Button
                    color='inherit'
                    component={Link}
                    to='/my-appointments'
                    sx={{mx: 1}}
                  >
                    Mes RDV
                  </Button>

                  <IconButton
                    size='large'
                    edge='end'
                    aria-label='account of current user'
                    aria-controls='profile-menu'
                    aria-haspopup='true'
                    onClick={handleProfileMenuOpen}
                    color='inherit'
                  >
                    <Avatar
                      sx={{width: 32, height: 32, bgcolor: 'secondary.main'}}
                    >
                      {user?.first_name?.[0]?.toUpperCase() || 'U'}
                    </Avatar>
                  </IconButton>
                </>
              ) : (
                <>
                  <Button
                    color='inherit'
                    component={Link}
                    to='/login'
                    sx={{mx: 1}}
                  >
                    Connexion
                  </Button>
                  <Button
                    variant='outlined'
                    color='inherit'
                    component={Link}
                    to='/register'
                    sx={{mx: 1}}
                  >
                    Inscription
                  </Button>
                </>
              )}
            </Box>
          )}
        </Toolbar>
      </AppBar>

      {renderMobileMenu}
      {renderProfileMenu}
    </>
  );
};

export default Navbar;
