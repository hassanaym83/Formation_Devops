import React, {useState} from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  InputAdornment,
  IconButton,
  CircularProgress
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  AdminPanelSettings
} from '@mui/icons-material';
import {useAdminAuth} from '../../contexts/AdminAuthContext';

const LoginPage = () => {
  const {login} = useAdminAuth();
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Effacer l'erreur quand l'utilisateur tape
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(formData.username, formData.password);
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: 2
      }}
    >
      <Paper
        elevation={10}
        sx={{
          width: '100%',
          maxWidth: 400,
          p: 4,
          borderRadius: 3,
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)'
        }}
      >
        {/* En-tête */}
        <Box sx={{textAlign: 'center', mb: 4}}>
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              mb: 2
            }}
          >
            <Box
              sx={{
                backgroundColor: 'primary.main',
                borderRadius: '50%',
                p: 2,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <AdminPanelSettings sx={{fontSize: 40, color: 'white'}} />
            </Box>
          </Box>
          <Typography
            variant='h4'
            gutterBottom
            fontWeight='bold'
            color='primary'
          >
            Administration
          </Typography>
          <Typography variant='body2' color='text.secondary'>
            Gestion des campagnes de don de sang
          </Typography>
        </Box>

        {/* Formulaire de connexion */}
        <form onSubmit={handleSubmit}>
          <Box sx={{mb: 3}}>
            <TextField
              fullWidth
              name='username'
              label="Nom d'utilisateur"
              type='text'
              value={formData.username}
              onChange={handleChange}
              required
              variant='outlined'
              autoComplete='username'
              disabled={loading}
            />
          </Box>

          <Box sx={{mb: 3}}>
            <TextField
              fullWidth
              name='password'
              label='Mot de passe'
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleChange}
              required
              variant='outlined'
              autoComplete='current-password'
              disabled={loading}
              InputProps={{
                endAdornment: (
                  <InputAdornment position='end'>
                    <IconButton
                      aria-label='toggle password visibility'
                      onClick={togglePasswordVisibility}
                      edge='end'
                      disabled={loading}
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                )
              }}
            />
          </Box>

          {error && (
            <Alert severity='error' sx={{mb: 3}}>
              {error}
            </Alert>
          )}

          <Button
            type='submit'
            fullWidth
            variant='contained'
            size='large'
            disabled={loading || !formData.username || !formData.password}
            sx={{
              py: 1.5,
              fontSize: '1.1rem',
              fontWeight: 'bold',
              borderRadius: 2,
              textTransform: 'none',
              background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #FE8B9B 30%, #FFAE73 90%)'
              }
            }}
          >
            {loading ? (
              <>
                <CircularProgress size={20} sx={{mr: 1, color: 'white'}} />
                Connexion...
              </>
            ) : (
              'Se connecter'
            )}
          </Button>
        </form>

        {/* Informations de test */}
        <Box sx={{mt: 4, p: 2, bgcolor: 'grey.50', borderRadius: 1}}>
          <Typography
            variant='caption'
            color='text.secondary'
            align='center'
            display='block'
          >
            <strong>Comptes de test :</strong>
            <br />
            Admin principal : admin / admin123
            <br />
            Super admin : superadmin / superadmin123
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
};

export default LoginPage;
